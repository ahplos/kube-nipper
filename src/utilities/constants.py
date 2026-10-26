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
    def DATA(self) -> str:
        return 'data'

    @property
    def SPEC(self) -> str:
        return 'spec'

    @property
    def STATUS(self) -> str:
        return 'status'

    @property
    def EVENTS(self) -> str:
        return 'events'

    @property
    def ON_DELETE_LOGS(self) -> str:
        return 'onDeleteLogs'

    @property
    def ON_RESTART_LOGS(self) -> str:
        return 'onRestartLogs'

class NIP_CONSTS(object, metaclass=_CONSTS):
    pass
