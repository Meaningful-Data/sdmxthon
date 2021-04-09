"""
    itemScheme file contains the classes for Item and ItemScheme and its derivatives
"""

import warnings
from datetime import datetime
from typing import List

from SDMXThon.parsers.references import RelationshipRefType
from SDMXThon.utils.handlers import add_indent, export_intern_data, split_unique_id
from SDMXThon.utils.mappings import structureAbbr
from SDMXThon.utils.xml_base import find_attr_value_
from .base import MaintainableArtefact, NameableArtefact, InternationalString
from .header import Contact
from .representation import Representation
from .utils import generic_setter, bool_setter


class ItemScheme(MaintainableArtefact):
    """The descriptive information for an arrangement or division of objects into groups based
        on characteristics, which the objects have in common.
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

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.unique_id}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.unique_id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.unique_id}>'

    @property
    def items(self):
        """Association to the Items in the scheme"""
        return self._items

    @property
    def is_partial(self):
        """Denotes whether the Item Scheme contains a sub set of the 
        full set of Items in the maintained scheme."""
        return self._isPartial

    @is_partial.setter
    def is_partial(self, value):
        self._isPartial = bool_setter(value)

    def append(self, value):

        """Adds an Item to the ItemScheme"""

        if isinstance(value, globals()[self._itemType]):
            if value.id is None:
                warnings.warn("Item not added because it did not have id_")
            if value.id not in self._items.keys():
                self._items[value.id] = value
                value.scheme = self
                if value.parent is not None and value.parent in self._items.keys():
                    self._items[value.parent].add_child(value.id)
                    value.parent = self._items[value.parent]
        else:
            raise TypeError(f"The object has to be of the type {self._itemType}")

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ItemScheme, self)._build_attributes(node, attrs, already_processed)

        value = find_attr_value_('isPartial', node)
        if value is not None and 'isPartial' not in already_processed:
            already_processed.add('isPartial')
            value = self._gds_parse_boolean(value)
            self.is_partial = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(ItemScheme, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def _parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(ItemScheme, self)._to_XML(prettyprint)

        if self.is_partial is not None:
            data['Attributes'] += f' isPartial="{str(self.is_partial).lower()}"'

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes}>'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        for i in self.items.values():
            outfile += i._parse_XML(indent, self._itemType)

        outfile += f'{indent}</{label}>'

        return outfile


class ConceptScheme(ItemScheme):
    """ The descriptive information for an arrangement or division of concepts into groups based
        on characteristics, which the objects have in common.

        ItemType:
            :obj:`Concept`

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
    def _factory(*args_, **kwargs_):
        """Factory Method of ConceptScheme"""
        return ConceptScheme(*args_, **kwargs_)

    @property
    def cl_references(self):
        """For parsing purposes, makes a dict of all the Codelist references"""
        return self._cl_references

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ConceptScheme, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(ConceptScheme, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'Concept':
            obj_ = Concept._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if obj_.core_representation is not None and obj_.core_representation.codelist is not None:
                self._cl_references[obj_.id] = obj_.core_representation.codelist
            self.append(obj_)


class Codelist(ItemScheme):
    """ A list from which some statistical concepts (coded concepts) take their values.

        ItemType:
            :obj:`Code`
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

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Codelist"""
        return Codelist(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Codelist, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Codelist, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'Code':
            obj_ = Code._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
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
    """ A maintained collection of Maintenance Agencies.

        ItemType:
            :obj:`Agency`
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
    def _factory(*args_, **kwargs_):
        """Factory Method of AgencyScheme"""
        return AgencyScheme(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(AgencyScheme, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(AgencyScheme, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'Agency':
            obj_ = Agency._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.append(obj_)


class Item(NameableArtefact):
    """The Item is an item of content in an Item Scheme. This may be a concept in
       a concept scheme, a code in a codelist etc.
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
                self.add_child(c)
            else:
                raise ValueError('Item cannot have two childs with same URN')

    def __eq__(self, other):
        if isinstance(other, Item):
            return super(Item, self).__eq__(other)
        else:
            return False

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

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
        self._parent = value
        """
        if value is None:
            self._parent = value
        elif value.__class__ == self.__class__:
            value.addChild(self)
            self._parent = value
        else:
            raise TypeError(f"The parent of a {self._schemeType} has to be another {self._schemeType}  object")
        """

    def add_child(self, value):
        """Adds a child to the Item"""
        self._childs.append(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Item, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Item, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'Parent':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.parent = obj_.ref

    def _parse_XML(self, indent, head):
        head = f'{structureAbbr}:' + head

        prettyprint = indent != ''

        data = super(Item, self)._to_XML(prettyprint)
        indent = add_indent(indent)
        outfile = f'{indent}<{head} {data["Attributes"]}>'
        outfile += export_intern_data(data, indent)
        return outfile


class Code(Item):
    """ A language independent set of letters, numbers or symbols that represent
        a concept whose meaning is described in a natural language

        SchemeType:
            :obj:`Codelist`

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
    def _factory(*args_, **kwargs_):
        """Factory Method of Code"""
        return Code(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Code, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Code, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def _parse_XML(self, indent, head):
        outfile = super(Code, self)._parse_XML(indent, head)

        indent = add_indent(indent)
        outfile += f'{indent}</{structureAbbr}:{head}>'

        return outfile


class Agency(Item):
    """ Provides identity to all derived classes. It also provides annotations to derived classes
        because it is a subclass of AnnotableArtefact.

        SchemeType:
            :obj:`AgencyScheme`
    """
    _schemeType = "AgencyScheme"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 scheme: ItemScheme = None, contacts: List[Contact] = None):
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
        self._contacts = generic_setter(value, List[Contact])

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Agency"""
        return Agency(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Agency, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Agency, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'Contact':
            obj_ = Contact._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._contacts is None:
                self._contacts = []
            self._contacts.append(obj_)

    def _parse_XML(self, indent, head):
        outfile = super(Agency, self)._parse_XML(indent, head)

        indent = add_indent(indent)

        if self.contacts is not None:
            indent_child = add_indent(indent)
            for e in self.contacts:
                outfile += f'{indent_child}<{structureAbbr}:Contact>'
                outfile += e.to_xml(indent_child)
                outfile += f'{indent_child}</{structureAbbr}:Contact>'

        outfile += f'{indent}</{structureAbbr}:{head}>'

        return outfile


class Concept(Item):
    """ A concept is a unit of knowledge created by a unique combination of characteristics.

        SchemeType:
            :obj:`ConceptScheme`
    """

    _schemeType = "ConceptScheme"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 scheme: ItemScheme = None, parent: Item = None, childs=None,
                 coreRepresentation: Representation = None):
        if childs is None:
            childs = []
        if annotations is None:
            annotations = []
        super(Concept, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                      name=name, description=description,
                                      scheme=scheme, parent=parent, childs=childs)

        self.core_representation = coreRepresentation
        self._ref = None  # Attribute for storing the references to codelists.

    def __eq__(self, other):
        if isinstance(other, Concept):
            return super(Concept, self).__eq__(other) and self._coreRepresentation == other._coreRepresentation
        else:
            return False

    @property
    def core_representation(self):
        """Associates a Representation"""
        return self._coreRepresentation

    @core_representation.setter
    def core_representation(self, value):
        from .representation import Representation
        self._coreRepresentation = generic_setter(value, Representation)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Concept"""
        return Concept(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Concept, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=None, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Concept, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'CoreRepresentation':
            obj_ = Representation._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.core_representation = obj_

    def _parse_XML(self, indent, head):
        outfile = super(Concept, self)._parse_XML(indent, head)

        indent = add_indent(indent)
        indent_child = add_indent(indent)
        if self.core_representation is not None:
            indent_enum = add_indent(indent_child)
            indent_ref = add_indent(indent_enum)
            outfile += f'{indent_child}<{structureAbbr}:CoreRepresentation>'
            if self.core_representation.codelist is not None:
                outfile += f'{indent_enum}<{structureAbbr}:Enumeration>'
                if isinstance(self.core_representation.codelist, str):
                    agencyID, id_, version = split_unique_id(self.core_representation.codelist)

                    outfile += f'{indent_ref}<Ref package="codelist" agencyID="{agencyID}" ' \
                               f'id="{id_}" ' \
                               f'version="{version}" class="Codelist"/>'
                else:
                    outfile += f'{indent_ref}<Ref package="codelist" agencyID="{self.core_representation.codelist.agencyID}" ' \
                               f'id="{self.core_representation.codelist.id}" ' \
                               f'version="{self.core_representation.codelist.version}" class="Codelist"/>'

                outfile += f'{indent_enum}</{structureAbbr}:Enumeration>'

            outfile += f'{indent_child}</{structureAbbr}:CoreRepresentation>'

        outfile += f'{indent}</{structureAbbr}:{head}>'

        return outfile
