from kopf import Operation

from box import Box


class _CONSTS(type):

    GLOBAL_REGISTRY = Box()

    @property
    def V1_BETA1(self) -> str:
        return 'v1beta1'

    @property
    def METADATA(self) -> str:
        return 'metadata'

    @property
    def ANNOTATIONS(self) -> str:
        return 'annotations'

    @property
    def LABELS(self) -> str:
        return 'labels'

    @property
    def NAME(self) -> str:
        return 'name'

    @property
    def NAMESPACE(self) -> str:
        return 'namespace'

    @property
    def INVOLVED_OBJECT(self) -> str:
        return 'involvedObject'

    @property
    def SPEC(self) -> str:
        return 'spec'

    @property
    def STATUS(self) -> str:
        return 'status'

    @property
    def INVOLVED_OBJECT_EVENTS(self) -> str:
        return 'involvedObjectEvents'

    @property
    def RESTART_COUNT(self) -> str:
        return 'restartCount'

    @property
    def CONTAINER_LOGS(self) -> str:
        return 'containerLogs'

    @property
    def CONTAINERS(self) -> str:
        return 'containers'

    @property
    def INIT_CONTAINERS(self) -> str:
        return 'initContainers'

class NIP_CONSTS(object, metaclass=_CONSTS):
    pass
