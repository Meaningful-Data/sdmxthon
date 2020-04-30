from model.base import NameableArtefact, MaintainableArtefact, Annotation, InternationalString 
from typing import List, Dict
from datetime import datetime

class Item(NameableArtefact):
    #TODO Make sure that an item scheme doesn't contain twice the same object (identified by urn) and that an item does not have twice the same item as child
    
    _schemeType = None
    _urnType = None
    _qName = None

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                    name: InternationalString = None, description: InternationalString = None,
                    isPartial: bool = None, scheme = None, parent = None, childs: List = []):
        
        super(Item, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                                name = name, description = description)


        self.isPartial = isPartial
        
        self.scheme = scheme
        self.parent = parent
        
        self._childs = []
        for c in childs:
            self.addChild(c)
    
    @property
    def isPartial(self):
        return self._isPartial
  
    @property
    def scheme(self):
        return self._scheme
    
    @property
    def parent(self):
        return self._parent

    @property
    def childs(self):
        return self._childs

    @isPartial.setter
    def isPartial(self, value):
        if isinstance(value, bool) or value is None:
            self._isPartial = value
        else:
            raise TypeError("isPartial attribute has to be of the type bool")

    @scheme.setter
    def scheme(self,value): #TODO unappend item from the scheme if the item is already appended to one.
        if value is None:
            self._scheme = value
        elif value.__class__.__name__ == self._schemeType:
            self._scheme = value
            value.append(self)
        else:
            raise TypeError(f"The scheme object has to be of the type {self._schemeType}")

    @parent.setter 
    def parent(self, value):
        if value is None:
            self._parent = value
        elif value.__class__ == self.__class__ :
            value.addChild(self)
            self._parent = value
        else:
            raise TypeError(f"The parent of a {self._schemeType} has to be another {self._schemeType}  object")

    def addChild(self, value):
        if value.__class__ == self.__class__:
            if value not in self._childs:
                self._childs.append(value)
                value.parent = self
        else:
            raise TypeError(f"The parent of a {self._schemeType} has to be another {self._schemeType}  object")

    @property
    def urn(self):
        return f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self._qName.split('}')[1]}={self.parent.urn.split('=')[1]}.{self.id}" 

class ItemScheme(MaintainableArtefact):
    _itemType = None
    _urnType = None
    _qName = None

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                name: InternationalString = None, description: InternationalString = None,
                version: str = None, validFrom: datetime = None, validTo: datetime= None,
                isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None, 
                    structureUrl: str = None, maintainer = None,
                items: List[Item] = []):

        super(ItemScheme, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                        name = name, description = description,
                                        version = version, validFrom = validFrom, validTo = validTo,
                                        isFinal = isFinal, isExternalReference = isExternalReference, 
                                            serviceUrl = serviceUrl, structureUrl = structureUrl, maintainer = maintainer)
        self._items = []
        for i in items:
            self.append(i)
        
    @property
    def items(self):
        return self._items
   
    def append(self, value):
        if isinstance(value, globals()[self._itemType]):
            if value not in self._items:
                self._items.append(value)
                value.scheme = self
        else:
            raise TypeError(f"The object has to be of the type {self._itemType}")

    def toXml(self):
        xml=super().toXml()
        for i in self.items:
            xml.append(i.toXml())
        return xml

class ConceptScheme(ItemScheme):    
    _itemType = "Concept"
    _urnType="conceptscheme"
    _qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptScheme"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                name: InternationalString = None, description: InternationalString = None,
                version: str = None, validFrom: datetime = None, validTo: datetime= None,
                isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None, 
                    structureUrl: str = None, maintainer = None,
                items: List[Item] = []):

        super(ConceptScheme, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                        name = name, description = description,
                                        version = version, validFrom = validFrom, validTo = validTo,
                                        isFinal = isFinal, isExternalReference = isExternalReference, 
                                            serviceUrl = serviceUrl, structureUrl = structureUrl, maintainer = maintainer,
                                        items = items)

class CodeList(ItemScheme):

    _itemType = "Code"
    _urnType="codelist"
    _qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Codelist"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                name: InternationalString = None, description: InternationalString = None,
                version: str = None, validFrom: datetime = None, validTo: datetime= None,
                isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None, 
                    structureUrl: str = None, maintainer = None,
                items: List[Item] = []):

        super(CodeList, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                        name = name, description = description,
                                        version = version, validFrom = validFrom, validTo = validTo,
                                        isFinal = isFinal, isExternalReference = isExternalReference, 
                                            serviceUrl = serviceUrl, structureUrl = structureUrl, maintainer = maintainer,
                                        items = items)

class AgencyList(ItemScheme):
    _itemType = "Agency"
    _urnType="base"
    _qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}AgencyScheme"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                name: InternationalString = None, description: InternationalString = None,
                version: str = None, validFrom: datetime = None, validTo: datetime= None,
                isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None, 
                    structureUrl: str = None, maintainer = None,
                items: List[Item] = []):

        super(AgencyList, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                        name = name, description = description,
                                        version = version, validFrom = validFrom, validTo = validTo,
                                        isFinal = isFinal, isExternalReference = isExternalReference, 
                                            serviceUrl = serviceUrl, structureUrl = structureUrl, maintainer = maintainer,
                                        items = items)

class Concept(Item):
    _schemeType = "ConceptScheme"
    _urnType="conceptscheme"
    _qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Concept"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                    name: InternationalString = None, description: InternationalString = None,
                    isPartial: bool = None, scheme: ItemScheme = None, parent: Item = None, childs: List[Item] = []):
        
        super(Concept, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                    name = name, description = description,
                                    isPartial = isPartial, scheme = scheme, parent = parent, childs = childs)

class Code(Item):
    _schemeType = "CodeList"
    _urnType="codelist"
    _qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Code"
    
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                    name: InternationalString = None, description: InternationalString = None,
                    isPartial: bool = None, scheme: ItemScheme = None, parent: Item = None, childs: List[Item] = []):
        
        super(Code, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                    name = name, description = description,
                                    isPartial = isPartial, scheme = scheme, parent = parent, childs = childs)

class Agency(Item):
    _schemeType = "AgencyList"
    _urnType="base"
    _qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Agency"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                    name: InternationalString = None, description: InternationalString = None,
                    isPartial: bool = None, scheme: ItemScheme = None):
        
        super(Agency, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                    name = name, description = description,
                                    isPartial = isPartial, scheme = scheme)

    @property
    def parent(self):
        return self._parent

    @parent.setter 
    def parent(self, value):
        pass
    def addChild(self, value):
        pass