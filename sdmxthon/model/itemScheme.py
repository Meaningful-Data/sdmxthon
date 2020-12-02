import warnings
from datetime import datetime

from .base import NameableArtefact, MaintainableArtefact, InternationalString
from .utils import boolSetter, qName, stringSetter, genericSetter


class Item(NameableArtefact):
    # TODO Make sure that an item scheme doesn't contain twice the same object (identified by urn)
    #  and that an item does not have twice the same item as child

    _schemeType = None
    _urnType = None
    _qName = None

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme=None, parent=None, childs=None):

        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Item, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                   name=name, description=description)
        self.isPartial = isPartial

        self.scheme = scheme
        self.parent = parent

        self._childs = []
        for c in childs:
            self.addChild(c)

    def __eq__(self, other):
        if isinstance(other, Item):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self.name == other.name and
                    self._description == other._description and
                    self._isPartial == other._isPartial)
        else:
            return False

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
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self.__class__.__name__}=" \
                  f"{self.scheme.maintainer.id}:{self.scheme.id}({self.scheme.version}).{self.id}"
        except:
            urn = ""
        return urn


class ItemScheme(MaintainableArtefact):
    _itemType = None
    _urnType = None
    _qName = None

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        if annotations is None:
            annotations = []
        super(ItemScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                         name=name, description=description,
                                         version=version, validFrom=validFrom, validTo=validTo,
                                         isFinal=isFinal, isExternalReference=isExternalReference,
                                         serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer)
        if items is not None:
            self._items = {}
            for i in items:
                self.append(i)

    def __eq__(self, other):
        if isinstance(other, ItemScheme):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self.name == other.name and
                    self._description == other._description and
                    self._version == other._version and
                    self._validFrom == other._validFrom and
                    self._validTo == other._validTo and
                    self._isFinal == other._isFinal and
                    self._isExternalReference == other._isExternalReference and
                    self._serviceUrl == other._serviceUrl and
                    self._structureUrl == other._structureUrl and
                    self._maintainer == other._maintainer and
                    self._items == other._items)
        else:
            return False

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


class Code(Item):
    _schemeType = "CodeList"
    _urnType = "codelist"
    _qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Code"

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme: ItemScheme = None, parent: Item = None, childs=None):
        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Code, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                   name=name, description=description,
                                   isPartial=isPartial, scheme=scheme, parent=parent, childs=childs)

    def __eq__(self, other):
        if isinstance(other, Code):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self.name == other.name and
                    self._description == other._description and
                    self._isPartial == other._isPartial)
        else:
            return False


class Agency(Item):
    _schemeType = "AgencyList"
    _urnType = "base"
    _qName = qName("str", "Agency")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme: ItemScheme = None):
        if annotations is None:
            annotations = []
        super(Agency, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                     name=name, description=description,
                                     isPartial=isPartial, scheme=scheme)

    def __eq__(self, other):
        if isinstance(other, Agency):
            return (self._id == other._id and
                    self._uri == other._uri and
                    self._name == other._name and
                    self._description == other._description and
                    self._isPartial == other._isPartial)
        else:
            return False

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

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        if items is None:
            items = []
        if annotations is None:
            annotations = []
        super(ConceptScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                            name=name, description=description,
                                            version=version, validFrom=validFrom, validTo=validTo,
                                            isFinal=isFinal, isExternalReference=isExternalReference,
                                            serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                            items=items)

        self._checked = False

    def __eq__(self, other):
        if isinstance(other, ConceptScheme):
            if not self._checked:
                self._checked = True
                return (self._id == other._id and
                        self.uri == other.uri and
                        self.name == other.name and
                        self._description == other._description and
                        self._version == other._version and
                        self._validFrom == other._validFrom and
                        self._validTo == other._validTo and
                        self._isFinal == other._isFinal and
                        self._isExternalReference == other._isExternalReference and
                        self._serviceUrl == other._serviceUrl and
                        self._structureUrl == other._structureUrl and
                        self._maintainer == other._maintainer and
                        self._items == other._items)
            else:
                return True
        else:
            return False


class CodeList(ItemScheme):
    _itemType = "Code"
    _urnType = "codelist"
    _qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Codelist"

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        if items is None:
            items = []
        if annotations is None:
            annotations = []
        super(CodeList, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                       name=name, description=description,
                                       version=version, validFrom=validFrom, validTo=validTo,
                                       isFinal=isFinal, isExternalReference=isExternalReference,
                                       serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                       items=items)
        self._checked = False

    def __eq__(self, other):
        if isinstance(other, CodeList):
            if not self._checked:
                self._checked = True
                return (self._id == other._id and
                        self.uri == other.uri and
                        self.name == other.name and
                        self._description == other._description and
                        self._version == other._version and
                        self._validFrom == other._validFrom and
                        self._validTo == other._validTo and
                        self._isFinal == other._isFinal and
                        self._isExternalReference == other._isExternalReference and
                        self._serviceUrl == other._serviceUrl and
                        self._structureUrl == other._structureUrl and
                        self._maintainer == other._maintainer and
                        self._items == other._items)
            else:
                return True
        else:
            return False


class OrganisationScheme(ItemScheme):
    """Abstract class. Used for structure messages"""

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        if annotations is None:
            annotations = []
        if items is None:
            items = []
        super(OrganisationScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                 name=name, description=description,
                                                 version=version, validFrom=validFrom, validTo=validTo,
                                                 isFinal=isFinal, isExternalReference=isExternalReference,
                                                 serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                 maintainer=maintainer,
                                                 items=items)

    def __eq__(self, other):
        if isinstance(other, OrganisationScheme):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self.name == other.name and
                    self._description == other._description and
                    self._version == other._version and
                    self._validFrom == other._validFrom and
                    self._validTo == other._validTo and
                    self._isFinal == other._isFinal and
                    self._isExternalReference == other._isExternalReference and
                    self._serviceUrl == other._serviceUrl and
                    self._structureUrl == other._structureUrl and
                    self._maintainer == other._maintainer and
                    self._items == other._items)
        else:
            return False


class AgencyList(OrganisationScheme):
    _itemType = "Agency"
    _urnType = "base"
    _qName = qName("str", "AgencyScheme")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        if items is None:
            items = []
        if annotations is None:
            annotations = []
        super(AgencyList, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                         name=name, description=description,
                                         version=version, validFrom=validFrom, validTo=validTo,
                                         isFinal=isFinal, isExternalReference=isExternalReference,
                                         serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                         items=items)

    def __eq__(self, other):
        if isinstance(other, AgencyList):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self.name == other.name and
                    self._description == other._description and
                    self._version == other._version and
                    self._validFrom == other._validFrom and
                    self._validTo == other._validTo and
                    self._isFinal == other._isFinal and
                    self._isExternalReference == other._isExternalReference and
                    self._serviceUrl == other._serviceUrl and
                    self._structureUrl == other._structureUrl and
                    self._maintainer == other._maintainer and
                    self._items == other._items)
        else:
            return False

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

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 isPartial: bool = None, scheme: ItemScheme = None, parent: Item = None, childs=None,
                 coreRepresentation=None):
        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Concept, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                      name=name, description=description,
                                      isPartial=isPartial, scheme=scheme, parent=parent, childs=childs)

        self.coreRepresentation = coreRepresentation
        self._ref = None  # Attribute for storing the references to codelists.

    def __eq__(self, other):
        if isinstance(other, Concept):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self.name == other.name and
                    self._description == other._description and
                    self._isPartial == other._isPartial and
                    self._coreRepresentation == other._coreRepresentation)
        else:
            return False

    @property
    def coreRepresentation(self):
        return self._coreRepresentation

    @coreRepresentation.setter
    def coreRepresentation(self, value):
        from .structure import Representation
        self._coreRepresentation = genericSetter(value, Representation)
