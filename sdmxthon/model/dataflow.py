from datetime import datetime

from .base import MaintainableArtefact, InternationalString
from .component import DataStructureDefinition
from .utils import qName, genericSetter


class DataFlowDefinition(MaintainableArtefact):
    _urnType = "datastructure"
    _qName = qName("str", "Dataflow")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None, structure: DataStructureDefinition = None):
        if annotations is None:
            annotations = []
        super(DataFlowDefinition, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                 name=name, description=description,
                                                 version=version, validFrom=validFrom, validTo=validTo,
                                                 isFinal=isFinal, isExternalReference=isExternalReference,
                                                 serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                 maintainer=maintainer)
        self.structure = structure

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        self._structure = genericSetter(value, DataStructureDefinition)
