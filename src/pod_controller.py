import json
from typing import Any
from datetime import datetime, timezone

import kopf

from box import Box, BoxList

import kr8s
from kr8s.objects import Job, Pod, Event

from utilities.constants import NIP_CONSTS
from utilities.resource_nip import ResourceNip

@kopf.index('namespaces') # type: ignore
async def tps_namespaces(annotations: kopf.Annotations, name: str, logger, **_: Any) -> Any:
    if (annotations.get(ResourceNip.RESOURCE_NIP_ANNOTATION)) == 'true':
        logger.info(f'MONITORING namespace {name}')
        return {name: True}

def is_monitored_namespace(tps_namespaces: kopf.Index, namespace, logger, **_: Any):
    return namespace in tps_namespaces

@kopf.on.field(
    Pod.version,
    Pod.plural,
    param='containerRestarted',
    field='status.containerStatuses',
    when=kopf.all_([is_monitored_namespace])
)
@kopf.on.field(
    Pod.version,
    Pod.plural,
    param='initContainerRestarted',
    field='status.initContainerStatuses',
    when=kopf.all_([is_monitored_namespace])
)
def on_pod_update(namespace: str,
                  name: str,
                  old: dict[str| Any],
                  new: dict[str| Any],
                  body: kopf.Body,
                  status: kopf.Status,
                  param,
                  logger,
                  **_):
    if (old and new):
        old_statuses = { c[NIP_CONSTS.NAME]: c[NIP_CONSTS.RESTART_COUNT] for c in old }
        new_statuses = { c[NIP_CONSTS.NAME]: c[NIP_CONSTS.RESTART_COUNT] for c in new }

        for cont_name, restart_count in new_statuses.items():
            if restart_count > old_statuses.get(cont_name, 0):
                create_pod_nip(namespace, name, body, param, logger, cont_name)
                break

@kopf.on.delete(
    Pod.version,
    Pod.plural,
    param='resourceDeleted',
    when=is_monitored_namespace
)
def on_pod_delete(namespace: str,
                  name: str,
                  body: kopf.Body,
                  param,
                  logger,
                   **_):
    create_pod_nip(namespace, name, body, param, logger)

def create_pod_nip(namespace: str, name: str, body: kopf.body, param: str, logger: kopf.Logger, container_name: str = None):
    pod_nip = ResourceNip(name, namespace=namespace)
    pod_nip.metadata.name = None
    pod_nip.metadata.generateName = name + '-'

    pod_nip.involvedObject.update(body)
    del pod_nip.involvedObject.metadata.managedFields

    event_list = Event.list(namespace=namespace,
                            field_selector=f'involvedObject.name={name},involvedObject.kind=Pod',
                            raw=True)
    pod_events = BoxList(event_list)
    pod_events.sort(key=lambda event: (event.lastTimestamp is None, event.lastTimestamp))
    pod_nip.involvedObjectEvents.extend(pod_events)

    container_logs = get_container_logs(pod_nip, body, container_name)
    pod_nip.containerLogs.extend(container_logs)

    pod_nip.source = param
    logger.error(f'pod_nip.source {pod_nip.source}')

    logger.info(f'creating ResourceNip {namespace}/{name}')
    pod_nip.create()

def get_container_logs(pod_nip: ResourceNip, body: kopf.Body, container_name: str = None):
    body = Box(body, default_box=True, default_box_attr=None)
    cont_names = BoxList()
    container_logs = []

    init_cont_names = BoxList()
    if body.spec.initContainers:
        init_cont_names.extend([c.name for c in body.spec.initContainers])

    if container_name:
        cont_names.append(container_name)
    else:
        cont_names.extend([c.name for c in body.spec.containers])

    pod = Pod(body.metadata.name, body.metadata.namespace)
    for cont_name in cont_names:
        container_logs.append({
            'container': cont_name,
            'init': cont_name in init_cont_names,
            'logs': '\n'.join(pod.logs(container=cont_name, previous=(container_name != None), tail_lines=300))
        })

    return container_logs
