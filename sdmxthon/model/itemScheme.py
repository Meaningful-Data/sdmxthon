import warnings
from datetime import datetime

from .base import NameableArtefact, MaintainableArtefact, InternationalString
from .dataTypes import FacetType, FacetValueType
from .utils import boolSetter, qName, stringSetter, genericSetter
from ..common.refs import RefBaseType
from ..utils.data_parser import DataParser
from ..utils.xml_base import find_attr_value_


class Item(NameableArtefact):
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
        urn_list = []
        for c in childs:
            if c.urn not in urn_list:
                urn_list.append(c.urn)
                self.addChild(c)
            else:
                raise ValueError('Item cannot have two childs with same URN')

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
    def scheme(self, value):
        if value is None:
            self._scheme = value
        elif value.__class__.__name__ == self._schemeType:
            value.append(self)
            self._scheme = value
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
            urn_list = []
            for i in items:
                # self.append(i)
                if i.urn not in urn_list:
                    urn_list.append(i.urn)
                    self.append(i)
                else:
                    raise ValueError('Item Scheme cannot have two items with same URN')

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
                warnings.warn("Item not added because it did not have id_")
            if value.id not in self._items:
                self._items[value.id] = value
                value.scheme = self
        else:
            raise TypeError(f"The object has to be of the type {self._itemType}")


class Code(Item, DataParser):
    _schemeType = "Codelist"
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

    @staticmethod
    def factory(*args_, **kwargs_):
        return Code(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

    def build_children(self, child_, node, nodeName_, gds_collector_=None):
        pass
        # TODO Parse Name and Description


class Agency(Item, DataParser):
    _schemeType = "AgencyScheme"
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

    @staticmethod
    def factory(*args_, **kwargs_):
        return Agency(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        # TODO Parse Name and Description and Contact
        pass


class ConceptScheme(ItemScheme, DataParser):
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
        self._cl_references = {}
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

    @staticmethod
    def factory(*args_, **kwargs_):
        return ConceptScheme(*args_, **kwargs_)

    @property
    def cl_references(self):
        return self._cl_references

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

        value = find_attr_value_('agencyID', node)
        if value is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            self.maintainer = Agency(id_=value)

        value = find_attr_value_('isExternalReference', node)
        if value is not None and 'isExternalReference' not in already_processed:
            already_processed.add('isExternalReference')
            value = self.gds_parse_boolean(value)
            self.isExternalReference = value

        value = find_attr_value_('isFinal', node)
        if value is not None and 'isFinal' not in already_processed:
            already_processed.add('isFinal')
            value = self.gds_parse_boolean(value)
            self.isFinal = value

        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            # TODO Validate version
            self.version = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):

        if nodeName_ == 'Concept':
            obj_ = Concept.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.coreRepresentation is not None and obj_.coreRepresentation.codelist is not None:
                self._cl_references[obj_.id] = obj_.coreRepresentation.codelist
            self.append(obj_)

        # TODO Parse Name and Description


class Codelist(ItemScheme, DataParser):
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
        super(Codelist, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                       name=name, description=description,
                                       version=version, validFrom=validFrom, validTo=validTo,
                                       isFinal=isFinal, isExternalReference=isExternalReference,
                                       serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                       items=items)
        self._checked = False

    def __eq__(self, other):
        if isinstance(other, Codelist):
            if not self._checked:
                self._checked = True
                return (self.id == other.id and
                        self.uri == other.uri and
                        self.name == other.name and
                        self.description == other.description and
                        self.version == other.version and
                        self.validFrom == other.validFrom and
                        self.validTo == other.validTo and
                        self.isFinal == other.isFinal and
                        self.isExternalReference == other.isExternalReference and
                        self.serviceUrl == other._serviceUrl and
                        self.structureUrl == other.structureUrl and
                        self.maintainer == other.maintainer and
                        self.items == other._items)
            else:
                return True
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        return Codelist(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

        value = find_attr_value_('agencyID', node)
        if value is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            self.maintainer = Agency(id_=value)

        value = find_attr_value_('isExternalReference', node)
        if value is not None and 'isExternalReference' not in already_processed:
            already_processed.add('isExternalReference')
            value = self.gds_parse_boolean(value)
            self.isExternalReference = value

        value = find_attr_value_('isFinal', node)
        if value is not None and 'isFinal' not in already_processed:
            already_processed.add('isFinal')
            value = self.gds_parse_boolean(value)
            self.isFinal = value

        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            # TODO Validate version
            self.version = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            obj_ = Code.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.append(obj_)

        # TODO Parse Name and Description


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


class AgencyScheme(OrganisationScheme, DataParser):
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
        super(AgencyScheme, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                           name=name, description=description,
                                           version=version, validFrom=validFrom, validTo=validTo,
                                           isFinal=isFinal, isExternalReference=isExternalReference,
                                           serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                           items=items)

    def __eq__(self, other):
        if isinstance(other, AgencyScheme):
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
        self._id = stringSetter(value, '[A-Za-z][A-Za-z0-9_\\-]*(\\.[A-Za-z][A-Za-z0-9_\\-]*)*')

    @staticmethod
    def factory(*args_, **kwargs_):
        return AgencyScheme(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

        value = find_attr_value_('agencyID', node)
        if value is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            self.maintainer = Agency(id_=value)

        value = find_attr_value_('isExternalReference', node)
        if value is not None and 'isExternalReference' not in already_processed:
            already_processed.add('isExternalReference')
            value = self.gds_parse_boolean(value)
            self.isExternalReference = value

        value = find_attr_value_('isFinal', node)
        if value is not None and 'isFinal' not in already_processed:
            already_processed.add('isFinal')
            value = self.gds_parse_boolean(value)
            self.isFinal = value

        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            # TODO Validate version
            self.version = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):

        if nodeName_ == 'Agency':
            obj_ = Agency.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.append(obj_)

        # TODO Parse Name and Description


class Concept(Item, DataParser):
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

    @staticmethod
    def factory(*args_, **kwargs_):
        return Concept(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

    def build_children(self, child_, node, nodeName_, gds_collector_=None):
        if nodeName_ == 'CoreRepresentation':
            obj_ = Representation.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.coreRepresentation = obj_
        # TODO Parse Name and Description


class Facet:
    def __init__(self, facetType: str = None, facetValue: str = None, facetValueType: str = None):
        self.facetType = facetType
        self.facetValue = facetValue
        self.facetValueType = facetValueType

    @property
    def facetType(self):
        return self._facetType

    @property
    def facetValue(self):
        return self._facetValue

    @property
    def facetValueType(self):
        return self._facetValueType

    @facetType.setter
    def facetType(self, value):
        if isinstance(value, str) or value is None:
            if value in FacetType or value is None:
                self._facetType = value
            else:
                raise ValueError(f"The facet {value} is not recognised")
        else:
            raise ValueError("Facet dim_type should be of the str dim_type")

    @facetValue.setter
    def facetValue(self, value):
        self._facetValue = stringSetter(value)

    @facetValueType.setter
    def facetValueType(self, value):
        if isinstance(value, str) or value is None:
            if value in FacetValueType or value is None:
                self._facetValueType = value
            else:
                raise ValueError(f"The facet value dim_type {value} is not recognised")
        else:
            raise ValueError("Facet value dim_type should be of the str dim_type")


class EnumerationType(DataParser):
    def __init__(self, codelist=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)
        self._codelist = codelist

    @staticmethod
    def factory(*args_, **kwargs_):
        return EnumerationType(*args_, **kwargs_)

    @property
    def codelist(self):
        return self._codelist

    @codelist.setter
    def codelist(self, value):
        self._codelist = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = RefBaseType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.package is not None and obj_.package == 'codelist':
                self.codelist = f'{obj_.agencyID}:{obj_.id_}({obj_.version})'

    pass


class FormatType(DataParser):
    def __init__(self, facets=None, type_=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)

        if facets is None:
            self._facets = []
        else:
            self._facets = facets

        self._type = type_

    @staticmethod
    def factory(*args_, **kwargs_):
        return FormatType(**kwargs_)

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, value):
        self._type = value

    @property
    def facets(self):
        return self._facets

    @facets.setter
    def facets(self, value):
        if value is None:
            self._facets = []
        elif isinstance(value, list):
            self._facets = value
        else:
            raise TypeError('Value must be a list')

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('isSequence', node)
        if value is not None and 'isSequence' not in already_processed:
            already_processed.add('isSequence')
            value = self.gds_validate_boolean(value)
            self.facets.append(Facet(facetType='isSequence', facetValue=value))

        value = find_attr_value_('minLength', node)
        if value is not None and 'minLength' not in already_processed:
            already_processed.add('minLength')
            self.facets.append(Facet(facetType='minLength', facetValue=value))

        value = find_attr_value_('maxLength', node)
        if value is not None and 'maxLength' not in already_processed:
            already_processed.add('maxLength')
            self.facets.append(Facet(facetType='maxLength', facetValue=value))

        value = find_attr_value_('minValue', node)
        if value is not None and 'minValue' not in already_processed:
            already_processed.add('minValue')
            value = self.gds_validate_decimal(value)
            self.facets.append(Facet(facetType='minValue', facetValue=value))

        value = find_attr_value_('maxValue', node)
        if value is not None and 'maxValue' not in already_processed:
            already_processed.add('maxValue')
            value = self.gds_validate_decimal(value)
            self.facets.append(Facet(facetType='maxValue', facetValue=value))

        value = find_attr_value_('startValue', node)
        if value is not None and 'startValue' not in already_processed:
            already_processed.add('startValue')
            value = self.gds_validate_decimal(value)
            self.facets.append(Facet(facetType='startValue', facetValue=value))

        value = find_attr_value_('endValue', node)
        if value is not None and 'endValue' not in already_processed:
            already_processed.add('endValue')
            value = self.gds_validate_decimal(value)
            self.facets.append(Facet(facetType='endValue', facetValue=value))

        value = find_attr_value_('interval', node)
        if value is not None and 'interval' not in already_processed:
            already_processed.add('interval')
            value = self.gds_validate_double(value)
            self.facets.append(Facet(facetType='interval', facetValue=value))

        value = find_attr_value_('timeInterval', node)
        if value is not None and 'timeInterval' not in already_processed:
            already_processed.add('timeInterval')
            value = self.gds_validate_duration(value)
            self.facets.append(Facet(facetType='timeInterval', facetValue=value))

        value = find_attr_value_('decimals', node)
        if value is not None and 'decimals' not in already_processed:
            already_processed.add('decimals')
            value = self.gds_validate_integer(value)
            self.facets.append(Facet(facetType='decimals', facetValue=value))

        value = find_attr_value_('pattern', node)
        if value is not None and 'pattern' not in already_processed:
            already_processed.add('pattern')
            self.facets.append(Facet(facetType='pattern', facetValue=value))

        value = find_attr_value_('startTime', node)
        if value is not None and 'startTime' not in already_processed:
            already_processed.add('startTime')
            value = self.gds_validate_date(value)
            self.facets.append(Facet(facetType='startTime', facetValue=value))

        value = find_attr_value_('endTime', node)
        if value is not None and 'endTime' not in already_processed:
            already_processed.add('endTime')
            value = self.gds_validate_date(value)
            self.facets.append(Facet(facetType='endTime', facetValue=value))

        value = find_attr_value_('textType', node)
        if value is not None and 'textType' not in already_processed:
            already_processed.add('textType')
            self._type = value


class Representation(DataParser):
    def __init__(self, facets=None, codelist=None, conceptScheme=None, gdscollector_=None,
                 **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)
        self._components = []
        if facets is None:
            facets = []
        for f in facets:
            self.addFacet(f)
        self.codelist = codelist
        self.conceptScheme = conceptScheme
        self._type = None

    def __eq__(self, other):
        if isinstance(other, Representation):
            return (self._codelist == other._codelist and
                    self._conceptScheme == other._conceptScheme)
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        return Representation(*args_, **kwargs_)

    @property
    def facets(self):
        facets = []
        for e in self._components:
            facets.append(e)
        return facets

    @property
    def codelist(self):
        return self._codelist

    @property
    def conceptScheme(self):
        return self._conceptScheme

    @codelist.setter
    def codelist(self, value):
        self._codelist = value

    @conceptScheme.setter
    def conceptScheme(self, value):
        self._conceptScheme = value

    def addFacet(self, value):
        self._components.append(value)

    @property
    def type_(self):
        return self._type

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Enumeration':
            obj_ = EnumerationType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.codelist = obj_.codelist
        elif nodeName_ == 'TextFormat' or nodeName_ == 'EnumerationFormat':
            obj_ = FormatType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._type = obj_.type_
            self._components = obj_.facets
