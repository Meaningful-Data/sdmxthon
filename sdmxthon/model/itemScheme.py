"""
    itemScheme file contains the classes for Item and ItemScheme and its derivatives
"""

import warnings
from datetime import datetime

from .base import NameableArtefact, MaintainableArtefact, InternationalString
from .references import RelationshipRefType, RefBaseType
from .utils import stringSetter, genericSetter, FacetValueType, FacetType
from ..model.header import Contact
from ..parsers.data_parser import DataParser
from ..utils.handlers import export_intern_data, add_indent
from ..utils.mappings import *
from ..utils.xml_base import find_attr_value_


class Item(NameableArtefact):
    """ Item class.

           The Item is an item of content in an Item Scheme. This may be a node in
           a taxonomy or ontology, a code in a code list etc.

            Attributes:
                scheme: Reference to the ItemScheme
                parent: Reference to the parent Item
                childs: Reference to the child Items
    """

    _schemeType = None

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None, scheme=None, parent=None,
                 childs=None):

        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Item, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations, name=name,
                                   description=description)

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
            return super(Item, self).__eq__(other)
        else:
            return False

    @property
    def scheme(self):
        """Reference to the ItemScheme"""
        return self._scheme

    @property
    def parent(self):
        """Reference to the parent Item"""
        return self._parent

    @property
    def childs(self):
        """Reference to the child Items"""
        return self._childs

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
        """
        if value is None:
            self._parent = value
        elif value.__class__ == self.__class__:
            value.addChild(self)
            self._parent = value
        else:
            raise TypeError(f"The parent of a {self._schemeType} has to be another {self._schemeType}  object")
        """
        self._parent = value

    def addChild(self, value):
        """Adds a child to the Item"""
        self._childs.append(value)

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Item, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Item, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'Parent':
            obj_ = RelationshipRefType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parent = obj_.ref

    def parse_XML(self, indent, head):
        head = f'{structureAbbr}:' + head

        prettyprint = indent != ''

        data = super(Item, self).to_XML(prettyprint)
        indent = add_indent(indent)
        outfile = f'{indent}<{head} {data["Attributes"]}>'
        outfile += export_intern_data(data, indent)
        return outfile


class ItemScheme(MaintainableArtefact):
    """ ItemScheme class.

           The descriptive information for an arrangement or division of objects into groups based
           on characteristics, which the objects have in common.

            Attributes:
                isPartial: Denotes whether the Item Scheme contains a sub set
                of the full set of Items in the maintained scheme.

                items: Association to the Items in the scheme
    """

    _itemType = None

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None, isPartial: bool = None):

        super(ItemScheme, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                         name=name, description=description,
                                         version=version, validFrom=validFrom, validTo=validTo,
                                         isFinal=isFinal, isExternalReference=isExternalReference,
                                         serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer)

        self._isPartial = isPartial

        self._items = {}
        if items is not None:
            urn_list = []
            for i in items:
                if i.urn not in urn_list:
                    urn_list.append(i.urn)
                    self.append(i)
                else:
                    raise ValueError('Item Scheme cannot have two items with same URN')

    def __eq__(self, other):
        if isinstance(other, ItemScheme):
            return super(ItemScheme, self).__eq__(other) and self._items == other._items
        else:
            return False

    @property
    def items(self):
        """Association to the Items in the scheme"""
        return self._items

    @property
    def isPartial(self):
        """Denotes whether the Item Scheme contains a sub set of the 
        full set of Items in the maintained scheme."""
        return self._isPartial

    @isPartial.setter
    def isPartial(self, value):
        self._isPartial = value

    def append(self, value):

        """Adds an Item to the ItemScheme"""

        if isinstance(value, globals()[self._itemType]):
            if value.id is None:
                warnings.warn("Item not added because it did not have id_")
            if value.id not in self._items.keys():
                self._items[value.id] = value
                value.scheme = self
                if value.parent is not None and value.parent in self._items.keys():
                    self._items[value.parent].addChild(value.id)
                    value.parent = self._items[value.parent]
        else:
            raise TypeError(f"The object has to be of the type {self._itemType}")

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ItemScheme, self).build_attributes(node, attrs, already_processed)

        value = find_attr_value_('isPartial', node)
        if value is not None and 'isPartial' not in already_processed:
            already_processed.add('isPartial')
            value = self.gds_parse_boolean(value)
            self.isPartial = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(ItemScheme, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(ItemScheme, self).to_XML(prettyprint)

        if self.isPartial is not None:
            data['Attributes'] += f' isPartial="{str(self.isPartial).lower()}"'

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes}>'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        for i in self.items.values():
            outfile += i.parse_XML(indent, self._itemType)

        outfile += f'{indent}</{label}>'

        return outfile


class Code(Item):
    """ Code class.

           A language independent set of letters, numbers or symbols that represent
           a concept whose meaning is described in a natural language
    """

    _schemeType = "Codelist"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 scheme: ItemScheme = None, parent: Item = None, childs=None):
        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Code, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                   name=name, description=description,
                                   scheme=scheme, parent=parent, childs=childs)

    def __eq__(self, other):
        if isinstance(other, Code):
            return super(Code, self).__eq__(other)
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of Code"""
        return Code(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Code, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Code, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def parse_XML(self, indent, head):
        outfile = super(Code, self).parse_XML(indent, head)

        indent = add_indent(indent)
        outfile += f'{indent}</{structureAbbr}:{head}>'

        return outfile


class Agency(Item):
    """ Agency class.

           Provides identity to all derived classes. It also provides annotations to derived classes
           because it is a subclass of AnnotableArtefact.

            Attributes:
                contacts: list of associations to the Contact Information

    """
    _schemeType = "AgencyScheme"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 scheme: ItemScheme = None, contacts=None):
        if annotations is None:
            annotations = []
        super(Agency, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                     name=name, description=description,
                                     scheme=scheme)

        self._contacts = contacts

    def __eq__(self, other):
        if isinstance(other, Agency):
            return super(Agency, self).__eq__(other) and self._contacts == other._contacts
        else:
            return False

    @property
    def contacts(self):
        """list of associations to the Contact Information"""
        return self._contacts

    @contacts.setter
    def contacts(self, value):
        self._contacts = value

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of Agency"""
        return Agency(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Agency, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Agency, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'Contact':
            obj_ = Contact.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if self._contacts is None:
                self._contacts = []
            self._contacts.append(obj_)

    def parse_XML(self, indent, head):
        outfile = super(Agency, self).parse_XML(indent, head)

        indent = add_indent(indent)

        if self.contacts is not None:
            indent_child = add_indent(indent)
            for e in self.contacts:
                outfile += f'{indent_child}<{structureAbbr}:Contact>'
                outfile += e.to_XML(indent_child)
                outfile += f'{indent_child}</{structureAbbr}:Contact>'

        outfile += f'{indent}</{structureAbbr}:{head}>'

        return outfile


class ConceptScheme(ItemScheme):
    """ ConceptScheme class.

           The descriptive information for an arrangement or division of concepts into groups based
           on characteristics, which the objects have in common.
    """

    _itemType = "Concept"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        if annotations is None:
            annotations = []
        self._cl_references = {}
        super(ConceptScheme, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
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
                return super(ConceptScheme, self).__eq__(other)
            else:
                return True
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of ConceptScheme"""
        return ConceptScheme(*args_, **kwargs_)

    @property
    def cl_references(self):
        """For parsing purposes, makes a dict of all the Codelist references"""
        return self._cl_references

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ConceptScheme, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(ConceptScheme, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'Concept':
            obj_ = Concept.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.coreRepresentation is not None and obj_.coreRepresentation.codelist is not None:
                self._cl_references[obj_.id] = obj_.coreRepresentation.codelist
            self.append(obj_)


class Codelist(ItemScheme):
    """ Codelist class.
           A list from which some statistical concepts (coded concepts) take their values.
    """

    _itemType = "Code"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):
        super(Codelist, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
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
                return super(Codelist, self).__eq__(other)
            else:
                return True
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of Codelist"""
        return Codelist(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Codelist, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Codelist, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'Code':
            obj_ = Code.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.append(obj_)


class OrganisationScheme(ItemScheme):
    """Abstract class. Used for structure messages"""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):

        super(OrganisationScheme, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                 name=name, description=description,
                                                 version=version, validFrom=validFrom, validTo=validTo,
                                                 isFinal=isFinal, isExternalReference=isExternalReference,
                                                 serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                 maintainer=maintainer,
                                                 items=items)

    def __eq__(self, other):
        if isinstance(other, OrganisationScheme):
            return super(OrganisationScheme, self).__eq__(other)
        else:
            return False


class AgencyScheme(OrganisationScheme):
    """ AgencyScheme class.

           A maintained collection of Maintenance Agencies.
    """

    _itemType = "Agency"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 items=None):

        super(AgencyScheme, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                           name=name, description=description,
                                           version=version, validFrom=validFrom, validTo=validTo,
                                           isFinal=isFinal, isExternalReference=isExternalReference,
                                           serviceUrl=serviceUrl, structureUrl=structureUrl, maintainer=maintainer,
                                           items=items)

    def __eq__(self, other):
        if isinstance(other, AgencyScheme):
            return super(AgencyScheme, self).__eq__(other)
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of AgencyScheme"""
        return AgencyScheme(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(AgencyScheme, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(AgencyScheme, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'Agency':
            obj_ = Agency.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.append(obj_)


class Concept(Item):
    """ Concept class.

           A concept is a unit of knowledge created by a unique combination of characteristics.

           Attributes:
               coreRepresentation: associates a Representation

    """

    _schemeType = "ConceptScheme"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 scheme: ItemScheme = None, parent: Item = None, childs=None,
                 coreRepresentation=None):
        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Concept, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                      name=name, description=description,
                                      scheme=scheme, parent=parent, childs=childs)

        self.coreRepresentation = coreRepresentation
        self._ref = None  # Attribute for storing the references to codelists.

    def __eq__(self, other):
        if isinstance(other, Concept):
            return super(Concept, self).__eq__(other) and self._coreRepresentation == other._coreRepresentation
        else:
            return False

    @property
    def coreRepresentation(self):
        """Associates a Representation"""
        return self._coreRepresentation

    @coreRepresentation.setter
    def coreRepresentation(self, value):
        from .component import Representation
        self._coreRepresentation = genericSetter(value, Representation)

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of Concept"""
        return Concept(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Concept, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Concept, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'CoreRepresentation':
            obj_ = Representation.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.coreRepresentation = obj_

    def parse_XML(self, indent, head):
        outfile = super(Concept, self).parse_XML(indent, head)

        indent = add_indent(indent)
        indent_child = add_indent(indent)
        if self.coreRepresentation is not None:
            indent_enum = add_indent(indent_child)
            indent_ref = add_indent(indent_enum)
            outfile += f'{indent_child}<{structureAbbr}:CoreRepresentation>'
            if self.coreRepresentation.codelist is not None:
                outfile += f'{indent_enum}<{structureAbbr}:Enumeration>'
                outfile += f'{indent_ref}<Ref package="codelist" agencyID="{self.coreRepresentation.codelist.agencyID}" ' \
                           f'id="{self.coreRepresentation.codelist.id}" ' \
                           f'version="{self.coreRepresentation.codelist.version}" class="Codelist"/>'
                outfile += f'{indent_enum}</{structureAbbr}:Enumeration>'

            outfile += f'{indent_child}</{structureAbbr}:CoreRepresentation>'

        outfile += f'{indent}</{structureAbbr}:{head}>'

        return outfile


class Facet:
    """ Facet class.
           Defines the format for the content of the Component when reported in a data
           or metadata set.

           Attributes:
               facetType: A specific content type which is constrained by the FacetType enumeration
               facetValueType: The format of the value of a Component when reported in a data or metadata set.
            This is constrained by the FacetValueType enumeration.
               facetValue: The value of the Facet
    """

    def __init__(self, facetType: str = None, facetValue: str = None, facetValueType: str = None):
        self.facetType = facetType
        self.facetValue = facetValue
        self.facetValueType = facetValueType

    @property
    def facetType(self):
        """A specific content type which is constrained by the FacetType enumeration"""
        return self._facetType

    @property
    def facetValue(self):
        """The value of the Facet"""
        return self._facetValue

    @property
    def facetValueType(self):
        """The format of the value of a Component when reported in a data or metadata set.
            This is constrained by the FacetValueType enumeration."""
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
    """Parser of the XML element Enumeration"""

    def __init__(self, codelist=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)
        self._codelist = codelist

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of EnumerationType"""
        return EnumerationType(*args_, **kwargs_)

    @property
    def codelist(self):
        """Reference to the Codelist by its unique ID"""
        return self._codelist

    @codelist.setter
    def codelist(self, value):
        self._codelist = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.package is not None and obj_.package == 'codelist':
                self.codelist = f'{obj_.agencyID}:{obj_.id_}({obj_.version})'


class FormatType(DataParser):
    """Parser of the EnumerationFormat or TextFormat XML element"""

    def __init__(self, facets=None, type_=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)

        if facets is None:
            self._facets = []
        else:
            self._facets = facets

        self._type = type_

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of FormatType"""
        return FormatType(**kwargs_)

    @property
    def type_(self):
        """Specifies the basic type of the component (String, BigInteger...)"""
        return self._type

    @type_.setter
    def type_(self, value):
        self._type = value

    @property
    def facets(self):
        """List of Facet"""
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
        """Builds the attributes present in the XML element"""
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
    """ Representation class.

           The allowable value or format for Component or Concept

           Attributes:
               facets: list of Facets found
               codelist: reference to the codelist
               conceptScheme: reference to the ConceptScheme (only in MeasureDimension)
               type: Specifies the basic type of the component (String, BigInteger...)

    """

    def __init__(self, facets=None, codelist=None, conceptScheme=None, gdscollector_=None,
                 **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)
        self.codelist = codelist
        self.conceptScheme = conceptScheme
        self._type = None
        self._facets = []
        if facets is not None:
            for f in facets:
                self.addFacet(f)

    def __eq__(self, other):
        if isinstance(other, Representation):
            return self._codelist == other._codelist and self._conceptScheme == other._conceptScheme \
                   and self._type == other._type
        else:
            return False

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of Representation"""
        return Representation(*args_, **kwargs_)

    @property
    def facets(self):
        """list of Facets found"""
        return self._facets

    @property
    def codelist(self):
        """Reference to the codelist"""
        return self._codelist

    @property
    def conceptScheme(self):
        """Reference to the ConceptScheme (only in MeasureDimension)"""
        return self._conceptScheme

    @codelist.setter
    def codelist(self, value):
        self._codelist = value

    @conceptScheme.setter
    def conceptScheme(self, value):
        self._conceptScheme = value

    @facets.setter
    def facets(self, value):
        self._facets = value

    def addFacet(self, value):
        """Add a facet to the list"""
        self._facets.append(value)

    @property
    def type_(self):
        """Specifies the basic type of the component (String, BigInteger...)"""
        return self._type

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Enumeration':
            obj_ = EnumerationType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.codelist = obj_.codelist
        elif nodeName_ == 'TextFormat' or nodeName_ == 'EnumerationFormat':
            obj_ = FormatType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._type = obj_.type_
            self._facets = obj_.facets
