from enum import StrEnum
from typing import Any

from box import Box, BoxList

from kr8s._api import Api
from kr8s._types import SpecType
from kr8s.objects import new_class, APIObject

from utilities.constants import TPS_CONSTS

GROUP = 'monitoring.ahplos.org'

class TerminatedPodSnapshot(new_class('TerminatedPodSnapshot', version=f'{GROUP}/{TPS_CONSTS.V1_BETA1}', namespaced=True)):

    TERMINATED_POD_SNAPSHOT_ANNOTATION: str = f'{GROUP}/terminated-pod-snapshot'

    def __create_box(self, value: Any = {}):
        return Box(value, default_box=True, default_box_attr=None)

    def __init__(self, resource: SpecType, namespace: str | None = None, api: Api | None = None) -> None:
        super().__init__(resource, namespace, api)
        self.raw.setdefault(TPS_CONSTS.METADATA, self.__create_box()).setdefault(TPS_CONSTS.LABELS, self.__create_box())
        self.raw.metadata.setdefault(TPS_CONSTS.ANNOTATIONS, self.__create_box())

        self.raw.setdefault(TPS_CONSTS.DATA, self.__create_box())
        self.raw.data.setdefault(TPS_CONSTS.EVENTS, BoxList())
        self.raw.data.setdefault(TPS_CONSTS.METADATA, Box())
        self.raw.data.setdefault(TPS_CONSTS.ON_DELETE_LOGS, BoxList())
        self.raw.data.setdefault(TPS_CONSTS.ON_RESTART_LOGS, BoxList())
        self.raw.data.setdefault(TPS_CONSTS.SPEC, Box())
        self.raw.data.setdefault(TPS_CONSTS.STATUS, Box())

    @property
    def data(self):
        return self.raw.data

    @APIObject.raw.setter
    def raw(self, value: Any) -> None:
        self._raw = Box(value, default_box=True, default_box_attr=None)

