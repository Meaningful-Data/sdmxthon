import warnings
from datetime import datetime
from typing import List

from lxml.etree import QName, Element

from .base import NameableArtefact, MaintainableArtefact, Annotation, InternationalString
from .utils import boolSetter, getNameAndDescription, qName, stringSetter, genericSetter, getReferences


class Item(NameableArtefact):
    # TODO Make sure that an item scheme doesn't contain twice the same object (identified by urn) and that an item does not have twice the same item as child

    _schemeType = None
    _urnType = None
    _qName = None

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme=None, parent=None, childs: List = []):

        super(Item, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                   name=name, description=description)

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
        self._isPartial = boolSetter(value)

    @scheme.setter
    def scheme(self, value):  # TODO unappend item from the scheme if the item is already appended to one.
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
        elif value.__class__ == self.__class__:
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
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self.__class__.__name__}={self.scheme.maintainer.id}:{self.scheme.id}({self.scheme.version}).{self.id}"
        except:
            urn = ""
        return urn

    @classmethod
    def fromXml(cls, elem: Element, classType):

        item = classType()
        item.id = elem.get("id")
        item.uri = elem.get("uri")

        name, description = getNameAndDescription(elem)
        item.name = name
        item.description = description

        return item


class ItemScheme(MaintainableArtefact):
    _itemType = None
    _urnType = None
    _qName = None

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items: List[Item] = []):

        super(ItemScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                         name=name, description=description,
                                         version=version, validFrom=validFrom, validTo=validTo,
                                         isFinal=isFinal, isExternalReference=isExternalReference,
                                         serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer)
        self._items = {}
        for i in items:
            self.append(i)

    @property
    def items(self):
        return self._items

    def append(self, value):
        if isinstance(value, globals()[self._itemType]):
            if value.id is None:
                warnings.warn("Item not added because it did not have id")
            if value.id not in self._items:
                self._items[value.id] = value
                value.scheme = self
        else:
            raise TypeError(f"The object has to be of the type {self._itemType}")

    def toXml(self):
        xml = super().toXml()
        for i in self.items:
            xml.append(i.toXml())
        return xml

    @classmethod
    def fromXml(cls, elem):
        classMapping = {
            "AgencyScheme": AgencyList,
            "Codelist": CodeList,
            "ConceptScheme": ConceptScheme
        }

        # 1. Instantiate correct class
        itemSchemeTag = QName(elem.tag).localname
        itemScheme = classMapping[itemSchemeTag]()

        # 2. Get and instantiate maintainer
        maintainerId = elem.get("agencyID")
        maintainer = Agency(id_=maintainerId)
        itemScheme.maintainer = maintainer

        # 3. Get other attributes
        itemScheme.isExternalRefernce = elem.get("isExternalReference")
        itemScheme.id = elem.get("id")
        itemScheme.isFinal = elem.get("isFinal")
        itemScheme.version = elem.get("version")

        # 4. Get Name and description
        name, description = getNameAndDescription(elem)
        itemScheme.name = name
        itemScheme.description = description

        # 5. Get items
        items = elem.findall(qName("str", itemScheme._itemType))

        if itemSchemeTag == "ConceptScheme":
            for i in items:
                itemScheme.append(Concept.fromXml(i, globals()[itemScheme._itemType]))
        else:
            for i in items:
                itemScheme.append(Item.fromXml(i, globals()[itemScheme._itemType]))

        return itemScheme


class Code(Item):
    _schemeType = "CodeList"
    _urnType = "codelist"
    _qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Code"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme: ItemScheme = None, parent: Item = None, childs: List[Item] = []):
        super(Code, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                   name=name, description=description,
                                   isPartial=isPartial, scheme=scheme, parent=parent, childs=childs)


class Agency(Item):
    _schemeType = "AgencyList"
    _urnType = "base"
    _qName = qName("str", "Agency")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme: ItemScheme = None):

        super(Agency, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                     name=name, description=description,
                                     isPartial=isPartial, scheme=scheme)

    @property
    def urn(self):  # TOBECHECKED: What is the logic behind?
        try:
            if self.scheme.maintainer.id == "SDMX":
                urn = f"urn:sdmx:org.sdmx.infomodel.base.Agency={self.id}"
            else:
                urn = f"urn:sdmx:org.sdmx.infomodel.base.Agency={self.scheme.maintainer.id}.{self.id}"
        except:
            urn = ""
        return urn


class ConceptScheme(ItemScheme):
    _itemType = "Concept"
    _urnType = "conceptscheme"
    _qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptScheme"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items: List[Item] = []):
        super(ConceptScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                            name=name, description=description,
                                            version=version, validFrom=validFrom, validTo=validTo,
                                            isFinal=isFinal, isExternalReference=isExternalReference,
                                            serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                            items=items)


class CodeList(ItemScheme):
    _itemType = "Code"
    _urnType = "codelist"
    _qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Codelist"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items: List[Code] = []):
        super(CodeList, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                       name=name, description=description,
                                       version=version, validFrom=validFrom, validTo=validTo,
                                       isFinal=isFinal, isExternalReference=isExternalReference,
                                       serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                       items=items)


class OrganisationScheme(ItemScheme):
    """Abstract class. Used for structure messages"""

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items: List[Item] = []):
        super(OrganisationScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                 name=name, description=description,
                                                 version=version, validFrom=validFrom, validTo=validTo,
                                                 isFinal=isFinal, isExternalReference=isExternalReference,
                                                 serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                 maintainer=maintainer,
                                                 items=items)


class AgencyList(OrganisationScheme):
    _itemType = "Agency"
    _urnType = "base"
    _qName = qName("str", "AgencyScheme")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items: List[Item] = []):
        super(AgencyList, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                         name=name, description=description,
                                         version=version, validFrom=validFrom, validTo=validTo,
                                         isFinal=isFinal, isExternalReference=isExternalReference,
                                         serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                         items=items)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = stringSetter(value, "[A-Za-z][A-Za-z0-9_\-]*(\.[A-Za-z][A-Za-z0-9_\-]*)*")


class Concept(Item):
    _schemeType = "ConceptScheme"
    _urnType = "conceptscheme"
    _qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Concept"

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme: ItemScheme = None, parent: Item = None, childs: List[Item] = [],
                 coreRepresentation=None):

        super(Concept, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                      name=name, description=description,
                                      isPartial=isPartial, scheme=scheme, parent=parent, childs=childs)

        self.coreRepresentation = coreRepresentation
        self._ref = None  # Attribute for storing the references to codelists.

    @property
    def coreRepresentation(self):
        return self._coreRepresentation

    @coreRepresentation.setter
    def coreRepresentation(self, value):
        from .structure import Representation
        self._coreRepresentation = genericSetter(value, Representation)

    @classmethod
    def fromXml(cls, elem: Element, classType):
        from .structure import Representation

        # TODO implement extended facets

        # 1. Initialize the generic fromXml applicable to all items
        concept = Item.fromXml(elem, classType)
        # 2. Add core representation
        representation = elem.find(qName("str", "CoreRepresentation"))

        if representation is not None:
            lr = Representation()
            enumeration = representation.find(qName("str", "Enumeration"))

            if enumeration is not None:
                lr._codeListReference = getReferences(enumeration)
                concept.coreRepresentation = lr

        return concept
