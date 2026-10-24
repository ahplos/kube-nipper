from enum import StrEnum
from typing import Any

from box import Box, BoxList

from kr8s._api import Api
from kr8s._types import SpecType
from kr8s.objects import new_class, APIObject

from utilities.constants import NIP_CONSTS

GROUP = 'nipper.ahplos.org'

class ResourceNip(new_class('ResourceNip', version=f'{GROUP}/{NIP_CONSTS.V1_BETA1}', namespaced=True)):

    RESOURCE_NIP_ANNOTATION: str = f'{GROUP}/resource-nip'

    def __create_box(self, value: Any = {}):
        return Box(value, default_box=True, default_box_attr=None)

    def __init__(self, resource: SpecType, namespace: str | None = None, api: Api | None = None) -> None:
        super().__init__(resource, namespace, api)
        self.raw.setdefault(NIP_CONSTS.METADATA, self.__create_box()).setdefault(NIP_CONSTS.LABELS, self.__create_box())
        self.raw.metadata.setdefault(NIP_CONSTS.ANNOTATIONS, self.__create_box())

        self.raw.setdefault(NIP_CONSTS.DATA, self.__create_box())
        self.raw.data.setdefault(NIP_CONSTS.EVENTS, BoxList())
        self.raw.data.setdefault(NIP_CONSTS.METADATA, Box())
        self.raw.data.setdefault(NIP_CONSTS.ON_DELETE_LOGS, BoxList())
        self.raw.data.setdefault(NIP_CONSTS.ON_RESTART_LOGS, BoxList())
        self.raw.data.setdefault(NIP_CONSTS.SPEC, Box())
        self.raw.data.setdefault(NIP_CONSTS.STATUS, Box())

    @property
    def data(self):
        return self.raw.data

    @APIObject.raw.setter
    def raw(self, value: Any) -> None:
        self._raw = Box(value, default_box=True, default_box_attr=None)

