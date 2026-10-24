import json
from typing import Any
from datetime import datetime, timezone

import kopf

from box import Box, BoxList

import kr8s
from kr8s.objects import Job, Pod, Event

from utilities.constants import NIP_CONSTS
from utilities.resource_nip import ResourceNip

RESTART_COUNT = 'restartCount'

@kopf.index('namespaces')
async def tps_namespaces(annotations: kopf.Annotations, name: str, logger, **_: Any) -> Any:
    if (annotations.get(ResourceNip.RESOURCE_NIP_ANNOTATION)) == 'true':
        logger.info(f'MONITORING namespace {name}')
        return {name: True}

def is_monitored_namespace(tps_namespaces: kopf.Index, namespace, logger, **_: Any):
    return namespace in tps_namespaces

def is_pod_container_restarted(tps_namespaces: kopf.Index, status: kopf.Status, namespace, name, logger, **_: Any):
    firstRestart = any(cs.get(RESTART_COUNT) > 0 for cs in status['containerStatuses'])
    pod_snapshot = ResourceNip(name, namespace)
    logger.debug(f'checking restart count for Pod {name} in namespace {namespace}: {firstRestart}')
    return firstRestart and not pod_snapshot.exists()

def remove_managed_fields(event):
    event.metadata.pop('managedFields', None)
    return event

@kopf.on.update(
    Pod.version,
    Pod.plural,
    param='onRestart',
    field='status',
    when=kopf.all_([is_monitored_namespace, is_pod_container_restarted])
)
@kopf.on.delete(
    Pod.version,
    Pod.plural,
    param='onDelete',
    when=is_monitored_namespace
)
def create_or_update_tps(meta: kopf.Meta, spec: kopf.Spec, status: kopf.Status, namespace: str, name: str, param: str, logger, **_):
    status = Box(status)
    meta = Box(meta)

    pod = Pod(name, namespace)
    pod_snapshot = ResourceNip(name, namespace)

    pod_events = BoxList(pod_snapshot.data.events)
    pod_events.extend(Event.list(namespace=namespace, field_selector=f'involvedObject.name={name},involvedObject.kind=Pod', raw=True))
    pod_events = BoxList({event.metadata.name: remove_managed_fields(event) for event in pod_events}.values())
    pod_events.sort(key=lambda event: (event.lastTimestamp is None, event.lastTimestamp))

    containerLogs = get_container_logs(pod, pod_snapshot, status, param)

    pod_sum_patch = generate_patch(meta, spec, status, pod_events, param, containerLogs)

    if (not pod_snapshot.exists()):
        logger.info(f'creating ResourceNip {namespace}{name}')
        pod_snapshot.raw |= pod_sum_patch
        pod_snapshot.create()
    else:
        logger.info(f'patching ResourceNip {namespace}{name}')
        pod_snapshot.patch(pod_sum_patch, type='merge')

    log_tps_creation(meta, status, pod_sum_patch, logger)

def get_container_logs(pod: Pod, pod_snapshot: ResourceNip, status: kopf.Status, param: str):
    isRestart = param == 'onRestart'

    contNames = [cont.name for cont in status.containerStatuses if not isRestart or cont.get(RESTART_COUNT)]
    containerLogs = BoxList(pod_snapshot.data.onRestartLogs if isRestart else [])
    for contName in contNames:
        if not any(log.containerName == contName for log in containerLogs):
            containerLogs.append({
                'container': contName,
                'timeCollected': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'logs': '\n'.join(pod.logs(container=contName, previous=isRestart, tail_lines=200))
            })

    return containerLogs

def generate_patch(meta: kopf.Meta, spec: kopf.Spec, status: kopf.Status, pod_events: BoxList, param: str, containerLogs: BoxList):
    meta = Box(meta)
    del meta['managedFields']

    return Box({
        NIP_CONSTS.DATA: {
            f'{param}Logs': containerLogs,
            NIP_CONSTS.METADATA: meta,
            NIP_CONSTS.SPEC: Box(spec),
            NIP_CONSTS.STATUS: status,
            NIP_CONSTS.EVENTS: pod_events
        }
    })

def log_tps_creation(meta: kopf.Meta, status: kopf.Status, pod_sum_patch: dict, logger):
    hasRestartLogs = 'onRestartLogs' in pod_sum_patch.data
    hasDeleteLogs = 'onDeleteLogs' in pod_sum_patch.data
    log_data = {
        'name': meta.name,
        'namespace': meta.namespace,
        'restarts': True if hasRestartLogs else False,
        'deleted': True if hasDeleteLogs else False,
        'phase': status.phase,
        'error': True if (hasRestartLogs or pod_sum_patch.data.status.phase != 'Succeeded') else False,
        'created': meta.creationTimestamp
    }
    logger.info(json.dumps(log_data))