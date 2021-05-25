"""
    Component file holds the classes for the Component and its derivatives
"""

import json
from datetime import datetime
from typing import List

from SDMXThon.parsers.data_parser import DataParser
from SDMXThon.parsers.references import RelationshipRefType, RefBaseType
from SDMXThon.utils.handlers import export_intern_data, add_indent, \
    split_unique_id
from SDMXThon.utils.mappings import structureAbbr, Data_Types_VTL, commonAbbr
from SDMXThon.utils.xml_base import find_attr_value_
from .base import IdentifiableArtefact, MaintainableArtefact, \
    InternationalString
from .component import Component, Dimension, TimeDimension, Attribute, \
    PrimaryMeasure
from .extras import ReferencePeriod, ReleaseCalendar
from .utils import generic_setter, ConstraintRoleType, bool_setter


class GroupDimension(DataParser):
    """ Parser of a Dimension in a GroupDimensionDescriptor"""

    def __init__(self, gds_collector=None):
        super(GroupDimension, self).__init__(gds_collector)
        self._ref = None

    def __eq__(self, other):
        if isinstance(other, GroupDimension):
            return super(GroupDimension, self).__eq__(other)
        else:
            return False

    @property
    def ref(self):
        """Reference to the dimension"""
        return self._ref

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GroupDimension"""
        return GroupDimension(*args_, **kwargs_)

    def _build_children(self, child_, node, nodeName_,
                        fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DimensionReference':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.ref


class ComponentList(IdentifiableArtefact):
    """An abstract definition of a list of components.
       A concrete example is a Dimension Descriptor which defines
       the list of Dimensions in a DataStructure Definition.
    """
    _componentType = None

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):

        super(ComponentList, self).__init__(id_=id_, uri=uri, urn=urn,
                                            annotations=annotations)
        self._components = {}
        if components is not None:
            for c in components:
                self.add_component(c)

    def __eq__(self, other):
        if isinstance(other, ComponentList):
            return (super(ComponentList, self).__eq__(other) and
                    self._components == other._components)
        else:
            return False

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    @property
    def components(self):
        """An aggregate association to one or more components
        which make up the list."""
        return self._components

    def add_component(self, value):
        """Method to add a Component to the ComponentList"""
        if isinstance(self, MeasureDescriptor) and len(self._components) == 1:
            raise ValueError('Measure Descriptor cannot have '
                             'more than one Primary Measure')
        elif isinstance(value, (Dimension, Attribute, PrimaryMeasure)):
            value.componentList = self
            self._components[value.id] = value
        elif isinstance(value, GroupDimension):
            value.componentList = self
            self._components[value.ref] = value
        else:
            raise TypeError(
                f"The object has to be of the dim_type "
                f"[Dimension, Attribute, PrimaryMeasure], "
                f"{value.__class__.__name__} provided")

    def __len__(self):
        return len(self.components)

    def __getitem__(self, value):
        return self.components[value]

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ComponentList, self)._build_attributes(node, attrs,
                                                     already_processed)

    def _parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(ComponentList, self)._to_XML(prettyprint)

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes}>'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        for i in self.components.values():
            outfile += i._parse_XML(indent, self._componentType)

        outfile += f'{indent}</{label}>'

        return outfile


class DimensionDescriptor(ComponentList, DataParser):
    """An ordered set of metadata concepts that, combined, classify a
    statistical series, and whose values, when combined (the key) in an
    instance such as a data set, uniquely identify a specific observation
    """
    _componentType = "Dimension"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):

        if components is None:
            components = []
        super(DimensionDescriptor, self).__init__(id_=id_, uri=uri, urn=urn,
                                                  annotations=annotations,
                                                  components=components)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DimensionDescriptor"""
        return DimensionDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, DimensionDescriptor):
            return super(DimensionDescriptor, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(DimensionDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Dimension':
            obj_ = Dimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)
        elif nodeName_ == 'TimeDimension':
            obj_ = TimeDimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class AttributeDescriptor(ComponentList, DataParser):
    """A set metadata concepts that define the attributes of a
    Data Structure Definition."""

    _componentType = "Attribute"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):
        if components is None:
            components = []

        super(AttributeDescriptor, self).__init__(id_=id_, uri=uri, urn=urn,
                                                  annotations=annotations,
                                                  components=components)

    @staticmethod
    def _factory(*args_, **kwargs_):

        """Factory Method of AttributeDescriptor"""
        return AttributeDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, AttributeDescriptor):
            return super(AttributeDescriptor, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(AttributeDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Attribute':
            obj_ = Attribute._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class MeasureDescriptor(ComponentList, DataParser):
    """A metadata concept that defines the measure of a
    Data Structure Definition"""

    _componentType = "PrimaryMeasure"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):

        if components is None:
            components = []
        super(MeasureDescriptor, self).__init__(id_=id_, uri=uri, urn=urn,
                                                annotations=annotations,
                                                components=components)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MeasureDescriptor"""
        return MeasureDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, MeasureDescriptor):
            return super(MeasureDescriptor, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(MeasureDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'PrimaryMeasure':
            obj_ = PrimaryMeasure._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class GroupDimensionDescriptor(ComponentList, DataParser):
    """A set metadata concepts that define a partial key derived from the
    Dimension Descriptor in a Data Structure Definition.
    """

    _componentType = "Dimension"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):
        if components is None:
            components = []
        super(GroupDimensionDescriptor, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations, components=components)

    def __eq__(self, other):
        if isinstance(other, GroupDimensionDescriptor):
            return super(GroupDimensionDescriptor, self).__eq__(other)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GroupDimensionDescriptor"""
        return GroupDimensionDescriptor(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(GroupDimensionDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'GroupDimension':
            obj_ = GroupDimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class MemberSelection(DataParser):

    def __init__(self, is_included: bool = False,
                 values_for: Component = None, sel_value: list = None,
                 gds_collector=None):
        super(MemberSelection, self).__init__(gds_collector_=gds_collector)
        self.is_included = is_included
        self.values_for = values_for
        self.sel_value = []
        if sel_value is not None:
            self.sel_value = sel_value

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MemberSelection"""
        return MemberSelection(*args_, **kwargs_)

    @property
    def sel_value(self) -> list:
        return self._selValue

    @sel_value.setter
    def sel_value(self, value):
        self._selValue = generic_setter(value, list)

    @property
    def values_for(self):
        return self._values_for

    @values_for.setter
    def values_for(self, value):
        self._values_for = generic_setter(value, Component)

    @property
    def is_included(self):
        return self._is_included

    @is_included.setter
    def is_included(self, value):
        self._is_included = bool_setter(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._values_for = value

        value = find_attr_value_('include', node)
        if value is not None and 'include' not in already_processed:
            already_processed.add('include')
            value = self._gds_parse_boolean(value)
            self.is_included = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""

        if nodeName_ == 'Value':
            self.sel_value.append(child_.text)


class CubeRegion(DataParser):

    def __init__(self, is_included: bool = False,
                 member: MemberSelection = None, gds_collector=None):
        super(CubeRegion, self).__init__(gds_collector_=gds_collector)
        self.is_included = is_included

        self.member = member

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of CubeRegion"""
        return CubeRegion(*args_, **kwargs_)

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = generic_setter(value, MemberSelection)

    @property
    def is_included(self):
        return self._is_included

    @is_included.setter
    def is_included(self, value):
        self._is_included = bool_setter(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('include', node)
        if value is not None and 'include' not in already_processed:
            already_processed.add('include')
            value = self._gds_parse_boolean(value)
            self.is_included = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""

        if nodeName_ == 'KeyValue':
            obj_ = MemberSelection._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.member = obj_


class MetadataTargetRegion:

    def __init__(self, comp_list: ComponentList, isIncluded: bool = False,
                 member: MemberSelection = None):
        self.is_included = isIncluded

        self.comp_list = comp_list

        self.member = member

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = generic_setter(value, MemberSelection)

    @property
    def comp_list(self):
        return self._compList

    @comp_list.setter
    def comp_list(self, value):
        self._compList = generic_setter(value, ComponentList)

    @property
    def is_included(self):
        return self._isIncluded

    @is_included.setter
    def is_included(self, value):
        self._isIncluded = generic_setter(value, bool)


class DataKeySet(DataParser):

    def __init__(self, keys: list = None, isIncluded: bool = None,
                 gds_collector=None):
        super(DataKeySet, self).__init__(gds_collector_=gds_collector)

        self.keys = []

        if keys is not None:
            self.keys = keys

        self._isIncluded = isIncluded

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataKeySet"""
        return DataKeySet(*args_, **kwargs_)

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, value):
        self._keys = generic_setter(value, list)

    @property
    def is_included(self):
        return self._isIncluded

    @is_included.setter
    def is_included(self, value):
        self._isIncluded = bool_setter(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._valuesFor = value

        value = find_attr_value_('isIncluded', node)
        if value is not None and 'isIncluded' not in already_processed:
            already_processed.add('isIncluded')
            value = self._gds_parse_boolean(value)
            self.is_included = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""

        if nodeName_ == 'Key':
            obj_ = KeySetType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.keys.append(obj_.key)


class Constraint(MaintainableArtefact):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 name: InternationalString = None,
                 description: InternationalString = None,
                 version: str = None, validFrom: datetime = None,
                 validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None,
                 serviceUrl: str = None,
                 structureUrl: str = None,
                 dataContentRegion: List[CubeRegion] = None,
                 dataContentKeys: DataKeySet = None,
                 metadataContentRegion: List[MetadataTargetRegion] = None,
                 availableDates: List[ReferencePeriod] = None,
                 calendar: List[ReleaseCalendar] = None):
        if annotations is None:
            annotations = []
        super(Constraint, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     name=name, description=description,
                     version=version, validFrom=validFrom,
                     validTo=validTo,
                     isFinal=isFinal,
                     isExternalReference=isExternalReference,
                     serviceUrl=serviceUrl,
                     structureUrl=structureUrl)
        self.metadata_content_region = []
        self.data_content_region = []
        self.available_dates = []
        self.calendar = []

        if dataContentRegion is not None:
            self.data_content_region = dataContentRegion

        if metadataContentRegion is not None:
            self.metadata_content_region = metadataContentRegion
        if availableDates is not None:
            self.available_dates = availableDates
        if calendar is not None:
            self.calendar = calendar

        self.data_content_keys = dataContentKeys

        self._ref_attach = None
        self._type_attach = None

    @property
    def data_content_region(self) -> list:
        return self._data_content_region

    @data_content_region.setter
    def data_content_region(self, value):
        self._data_content_region = generic_setter(value, list)

    @property
    def data_content_keys(self):
        return self._data_content_keys

    @data_content_keys.setter
    def data_content_keys(self, value):
        self._data_content_keys = generic_setter(value, DataKeySet)

    @property
    def metadata_content_region(self):
        return self._metadata_content_region

    @metadata_content_region.setter
    def metadata_content_region(self, value):
        self._metadata_content_region = value

    @property
    def available_dates(self):
        return self._available_dates

    @available_dates.setter
    def available_dates(self, value):
        self._available_dates = generic_setter(value, list)

    @property
    def calendar(self):
        return self._calendar

    @calendar.setter
    def calendar(self, value):
        self._calendar = generic_setter(value, list)

    @property
    def ref_attach(self):
        return self._ref_attach

    @property
    def type_attach(self):
        return self._type_attach

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Constraint, self)._build_attributes(node, attrs,
                                                  already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Constraint, self)._build_children(child_, node, nodeName_,
                                                fromsubclass_, gds_collector_)

        if nodeName_ == 'ConstraintAttachment':
            obj_ = AttachmentConstraintType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref_attach = obj_.ref
            self._type_attach = obj_.type_

        elif nodeName_ == 'CubeRegion':
            obj_ = CubeRegion._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.data_content_region.append(obj_)

        elif nodeName_ == 'DataKeySet':
            obj_ = DataKeySet._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.data_content_keys = obj_


class AttachmentConstraintType(DataParser):

    def __init__(self, gds_collector=None):
        super(AttachmentConstraintType, self).__init__(
            gds_collector_=gds_collector)
        self._ref = None
        self._type = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of AttachmentConstraintType"""
        return AttachmentConstraintType(*args_, **kwargs_)

    @property
    def ref(self):
        return self._ref

    @property
    def type_(self):
        return self._type

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""

        if nodeName_ == 'Dataflow' or nodeName_ == 'DataStructure':
            obj_ = StructureType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.ref
            self._type = nodeName_


class KeySetType(DataParser):
    def __init__(self, gds_collector=None):
        super(KeySetType, self).__init__(gds_collector_=gds_collector)

        self._key = {}

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of KeySetType"""
        return KeySetType(*args_, **kwargs_)

    @property
    def key(self):
        return self._key

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""

        if nodeName_ == 'KeyValue':
            obj_ = MemberSelection._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._key[obj_.values_for] = obj_.sel_value[0]


class ContentConstraint(Constraint):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 name: InternationalString = None,
                 description: InternationalString = None,
                 version: str = None, validFrom: datetime = None,
                 validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None,
                 serviceUrl: str = None,
                 structureUrl: str = None,
                 dataContentRegion: List[CubeRegion] = None,
                 metadataContentRegion: List[MetadataTargetRegion] = None,
                 availableDates: List[ReferencePeriod] = None,
                 calendar: List[ReleaseCalendar] = None,
                 role: str = None):
        if annotations is None:
            annotations = []
        super(ContentConstraint, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     name=name,
                     description=description,
                     version=version,
                     validFrom=validFrom,
                     validTo=validTo,
                     isFinal=isFinal,
                     isExternalReference=isExternalReference,
                     serviceUrl=serviceUrl,
                     structureUrl=structureUrl,
                     dataContentRegion=dataContentRegion,
                     metadataContentRegion=metadataContentRegion,
                     availableDates=availableDates,
                     calendar=calendar)
        if role is not None and role not in ConstraintRoleType:
            raise ValueError('ConstraintRole must be either '
                             '"allowableContent" or "actualContent"')
        self._role = role

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of ContentConstraint"""
        return ContentConstraint(*args_, **kwargs_)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in ConstraintRoleType:
            raise ValueError('ConstraintRole must be either '
                             '"Allowed" or "Actual"')
        else:
            self._role = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ContentConstraint, self)._build_attributes(node, attrs,
                                                         already_processed)

        value = find_attr_value_('type', node)
        if value is not None and 'type' not in already_processed:
            already_processed.add('type')
            self.role = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(ContentConstraint, self)._build_children(child_, node, nodeName_,
                                                       fromsubclass_,
                                                       gds_collector_)

    def _parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(Constraint, self)._to_XML(prettyprint)

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes} type="{self.role}">'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        indent_child = add_indent(indent)
        indent_child_2 = add_indent(indent_child)
        indent_ref = add_indent(indent_child_2)
        indent_value = add_indent(indent_ref)

        outfile += f'{indent_child}<{structureAbbr}:ConstraintAttachment>'
        outfile += f'{indent_child_2}<{structureAbbr}:{self.type_attach}>'

        agencyID, id_, version = split_unique_id(self.ref_attach)

        outfile += f'{indent_ref}<Ref id="{id_}" ' \
                   f'version="{version}" ' \
                   f'agencyID="{agencyID}" ' \
                   f'package="datastructure" class="{self.type_attach}"/>'

        outfile += f'{indent_child_2}</{structureAbbr}:{self.type_attach}>'
        outfile += f'{indent_child}</{structureAbbr}:ConstraintAttachment>'

        if self.data_content_keys is not None:

            outfile += f'{indent_child}<{structureAbbr}:DataKeySet ' \
                       f'isIncluded="' \
                       f'{str(self.data_content_keys.is_included).lower()}">'

            for e in self.data_content_keys.keys:
                outfile += f'{indent_child_2}<{structureAbbr}:Key>'

                for k, v in e.items():
                    outfile += f'{indent_ref}<{commonAbbr}:KeyValue id="{k}">'
                    outfile += f'{indent_value}<{commonAbbr}:Value>{v}' \
                               f'</{commonAbbr}:Value>'
                    outfile += f'{indent_ref}</{commonAbbr}:KeyValue>'

                outfile += f'{indent_child_2}</{structureAbbr}:Key>'

            outfile += f'{indent_child}</{structureAbbr}:DataKeySet>'

        if self.data_content_region is not None:

            for e in self.data_content_region:
                outfile += f'{indent_child}<{structureAbbr}:CubeRegion ' \
                           f'isIncluded="{str(e.is_included).lower()}">'
                outfile += f'{indent_child_2}<{commonAbbr}:KeyValue ' \
                           f'id="{e.member.values_for}">'
                for j in e.member.sel_value:
                    outfile += f'{indent_ref}<{commonAbbr}:Value>{j}' \
                               f'</{commonAbbr}:Value>'
                outfile += f'{indent_child_2}</{commonAbbr}:KeyValue>'
                outfile += f'{indent_child}</{structureAbbr}:CubeRegion>'

        outfile += f'{indent}</{label}>'

        return outfile


class DataStructureDefinition(MaintainableArtefact):
    """A collection of metadata concepts, their structure and usage when used
    to collect or disseminate data."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 name: InternationalString = None,
                 description: InternationalString = None,
                 version: str = None, validFrom: datetime = None,
                 validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None,
                 serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 dimensionDescriptor: DimensionDescriptor = None,
                 measureDescriptor: MeasureDescriptor = None,
                 attributeDescriptor: AttributeDescriptor = None,
                 groupDimensionDescriptor: GroupDimensionDescriptor = None,
                 constraint: list = None):

        super(DataStructureDefinition, self). \
            __init__(id_=id_, uri=uri,
                     urn=urn,
                     annotations=annotations,
                     name=name,
                     description=description,
                     version=version,
                     validFrom=validFrom,
                     validTo=validTo,
                     isFinal=isFinal,
                     isExternalReference=isExternalReference,
                     serviceUrl=serviceUrl,
                     structureUrl=structureUrl,
                     maintainer=maintainer)

        self.dimension_descriptor = dimensionDescriptor
        self.measure_descriptor = measureDescriptor
        self.attribute_descriptor = attributeDescriptor
        self.group_dimension_descriptor = groupDimensionDescriptor
        self._constraints = constraint

    def __eq__(self, other):
        if isinstance(other, DataStructureDefinition):
            return (super.__eq__(self, other) and
                    self._dimensionDescriptor == other._dimensionDescriptor and
                    self._attributeDescriptor == other._attributeDescriptor and
                    self._measureDescriptor == other._measureDescriptor and
                    self._groupDimensionDescriptor ==
                    other._groupDimensionDescriptor)
        else:
            return False

    def __str__(self):
        return '<DataStructureDefinition  - %s:%s(%s)>' % (
            self.agencyID, self.id, self.version)

    def __unicode__(self):
        return u'<DataStructureDefinition  - %s:%s(%s)>' % (
            self.agencyID, self.id, self.version)

    def __repr__(self):
        return '<DataStructureDefinition  - %s:%s(%s)>' % (
            self.agencyID, self.id, self.version)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataStructureDefinition"""
        return DataStructureDefinition(*args_, **kwargs_)

    @property
    def dimension_descriptor(self):
        """An ordered set of metadata concepts that, combined, classify a
        statistical series, and whose values, when combined (the key)
        in an instance such as a data set, uniquely identify a
        specific observation"""
        return self._dimensionDescriptor

    @property
    def measure_descriptor(self):
        """A metadata concept that defines the measure of a
        Data Structure Definition"""
        return self._measureDescriptor

    @property
    def attribute_descriptor(self):
        """A set metadata concepts that define the attributes of a Data
        Structure Definition. """
        return self._attributeDescriptor

    @property
    def group_dimension_descriptor(self):
        """A set metadata concepts that define a partial key derived
           from the Dimension Descriptor in a Data Structure Definition."""
        return self._groupDimensionDescriptor

    @property
    def dimension_codes(self):
        """Keys of the dimensionDescriptor components"""
        return [k for k in self.dimension_descriptor.components]

    @property
    def attribute_codes(self):
        """Keys of the attributeDescriptor components"""
        if self.attribute_descriptor is not None:
            return [k for k in self.attribute_descriptor.components]
        else:
            return []

    @property
    def dataset_attribute_codes(self):
        """Attributes with no specified relationship"""
        result = []
        if self.attribute_descriptor is not None:
            for k in self.attribute_descriptor.components:
                if self.attribute_descriptor[k].related_to == \
                        "NoSpecifiedRelationship":
                    result.append(k)
        return result

    @property
    def content(self):
        """Extracts the content of a DSD as a dict"""

        result = {'dimensions': self.dimension_descriptor.components,
                  'measure': self.measure_descriptor.components[
                      self.measure_code]
                  }

        if self.attribute_descriptor is not None:
            result['attributes'] = self.attribute_descriptor.components

        if self.group_dimension_descriptor is not None:
            result['groups'] = self.group_dimension_descriptor

        return result

    @property
    def _facet_type(self):
        """Returns any component that has facets"""
        facets = {}
        type_ = {}
        for k, v in self.dimension_descriptor.components.items():
            if v.representation is not None:
                if v.representation.type_ is not None:
                    type_[k] = v.representation.type_

                if len(v.representation.facets) > 0:
                    facets[k] = v.representation.facets

        if self.attribute_descriptor is not None:
            for k, v in self.attribute_descriptor.components.items():
                if v.representation is not None:
                    if v.representation.type_ is not None:
                        type_[k] = v.representation.type_

                    if len(v.representation.facets) > 0:
                        facets[k] = v.representation.facets

        if self.measure_descriptor is not None:
            for k, v in self.measure_descriptor.components.items():
                if v.representation is not None:
                    if v.representation.type_ is not None:
                        type_[k] = v.representation.type_

                    if len(v.representation.facets) > 0:
                        facets[k] = v.representation.facets

        return facets, type_

    @property
    def _format_constraints(self):
        """Returns the constraints in a formatted way for validation"""
        cubes = {}
        series = []

        if self.constraints is not None:
            for c in self.constraints:
                if len(c.data_content_region) > 0:
                    for e in c.data_content_region:
                        if e.member.values_for not in cubes.keys():
                            cubes[e.member.values_for] = set(
                                e.member.sel_value)
                        else:
                            cubes[e.member.values_for].update(
                                e.member.sel_value)
                if c.data_content_keys is not None and \
                        c.role is not None and \
                        c.role == "Allowed":
                    series += c.data_content_keys.keys

        return cubes, series

    @property
    def measure_code(self):
        """Key of the MeasureDescriptor component (PrimaryMeasure)"""
        return list(self.measure_descriptor.components.keys())[0]

    @dimension_descriptor.setter
    def dimension_descriptor(self, value):
        self._dimensionDescriptor = generic_setter(value, DimensionDescriptor)

    @measure_descriptor.setter
    def measure_descriptor(self, value):
        self._measureDescriptor = generic_setter(value, MeasureDescriptor)

    @attribute_descriptor.setter
    def attribute_descriptor(self, value):
        self._attributeDescriptor = generic_setter(value, AttributeDescriptor)

    @group_dimension_descriptor.setter
    def group_dimension_descriptor(self, value):
        self._groupDimensionDescriptor = \
            generic_setter(value, GroupDimensionDescriptor)

    @property
    def constraints(self):
        return self._constraints

    def add_constraint(self, value: ContentConstraint):
        if self._constraints is None:
            self._constraints = []
        self._constraints.append(value)

    def to_vtl_json(self, path: str = None):
        """Formats the DataStructureDefinition as a VTL DataStructure"""
        dataset_name = self.id
        components = []
        for c in self.dimension_descriptor.components.values():

            type_ = "String"

            if (c.representation is not None and
                    c.representation.type_ is not None):
                type_ = c.representation.type_

            component = {"name": c.id, "role": "Identifier",
                         "type": Data_Types_VTL[type_], "isNull": False}

            components.append(component)
        if self.attribute_descriptor is not None:
            for c in self.attribute_descriptor.components.values():
                type_ = "String"

                if (c.representation is not None and
                        c.representation.type_ is not None):
                    type_ = c.representation.type_

                component = {"name": c.id, "role": "Attribute",
                             "type": Data_Types_VTL[type_], "isNull": True}

                components.append(component)
        for c in self.measure_descriptor.components.values():
            type_ = "String"

            if (c.representation is not None and
                    c.representation.type_ is not None):
                type_ = c.representation.type_

            component = {"name": c.id, "role": "Measure",
                         "type": Data_Types_VTL[type_], "isNull": True}

            components.append(component)

        result = {
            "DataSet": {"name": dataset_name, "DataStructure": components}}
        if path is not None:
            with open(path, 'w') as fp:
                fp.write(json.dumps(result))
        else:
            return result

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(DataStructureDefinition, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(DataStructureDefinition, self). \
            _build_children(child_, node, nodeName_, fromsubclass_,
                            gds_collector_)

        if nodeName_ == 'DataStructureComponents':
            obj_ = DataStructureComponentType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.attribute_descriptor = obj_.attributeDescriptor
            self.dimension_descriptor = obj_.dimensionDescriptor
            self.measure_descriptor = obj_.measureDescriptor
            self.group_dimension_descriptor = obj_.groupDimensionDescriptor

    def _parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(DataStructureDefinition, self)._to_XML(prettyprint)

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes}>'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        indent_child = add_indent(indent)

        outfile += f'{indent_child}<{structureAbbr}:DataStructureComponents>'

        if self.dimension_descriptor is not None:
            outfile += self.dimension_descriptor. \
                _parse_XML(indent_child, f'{structureAbbr}:DimensionList')

        if self.attribute_descriptor is not None:
            outfile += self.attribute_descriptor. \
                _parse_XML(indent_child, f'{structureAbbr}:AttributeList')

        if self.measure_descriptor is not None:
            outfile += self.measure_descriptor. \
                _parse_XML(indent_child, f'{structureAbbr}:MeasureList')

        outfile += f'{indent_child}</{structureAbbr}:DataStructureComponents>'

        outfile += f'{indent}</{label}>'

        return outfile


class DataFlowDefinition(MaintainableArtefact):
    """Abstract concept (i.e. the structure without any data) of a flow of data
       that providers will provide for different reference periods.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 name: InternationalString = None,
                 description: InternationalString = None,
                 version: str = None, validFrom: datetime = None,
                 validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None,
                 serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 structure: DataStructureDefinition = None,
                 constraints: list = None):
        super(DataFlowDefinition, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     name=name,
                     description=description,
                     version=version,
                     validFrom=validFrom,
                     validTo=validTo,
                     isFinal=isFinal,
                     isExternalReference=isExternalReference,
                     serviceUrl=serviceUrl,
                     structureUrl=structureUrl,
                     maintainer=maintainer)
        self.structure = structure
        self._constraints = constraints

    def __eq__(self, other):
        if isinstance(other, DataFlowDefinition):
            return super(DataFlowDefinition, self).__eq__(
                other) and self._structure == other._structure

    def __str__(self):
        return f'<DataFlowDefinition - {self.unique_id}>'

    def __unicode__(self):
        return f'<DataFlowDefinition - {self.unique_id}>'

    def __repr__(self):
        return f'<DataFlowDefinition - {self.unique_id}>'

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataFlowDefinition"""
        return DataFlowDefinition(*args_, **kwargs_)

    @property
    def structure(self):
        """Associates a DataflowDefinition to the DataStructureDefinition."""
        return self._structure

    @structure.setter
    def structure(self, value):
        self._structure = generic_setter(value, DataStructureDefinition)

    def add_constraint(self, value: ContentConstraint):
        self._constraints.append(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(DataFlowDefinition, self)._build_attributes(node, attrs,
                                                          already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(DataFlowDefinition, self)._build_children(child_, node,
                                                        nodeName_,
                                                        fromsubclass_=False,
                                                        gds_collector_=None)
        if nodeName_ == 'Structure':
            obj_ = StructureType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._structure = obj_.ref

    def _parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(DataFlowDefinition, self)._to_XML(prettyprint)

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes}>'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        indent_child = add_indent(indent)
        indent_ref = add_indent(indent_child)

        if self.structure is not None:
            outfile += f'{indent_child}<{structureAbbr}:Structure>'

            if isinstance(self.structure, str):
                agencyID, id_, version = split_unique_id(self.structure)

                outfile += f'{indent_ref}<Ref id="{id_}" ' \
                           f'version="{version}" ' \
                           f'agencyID="{agencyID}" ' \
                           f'package="datastructure" class="DataStructure"/>'
            else:
                outfile += f'{indent_ref}<Ref id="{self.structure.id}" ' \
                           f'version="{self.structure.version}" ' \
                           f'agencyID="{self.structure.agencyID}" ' \
                           f'package="datastructure" class="DataStructure"/>'
            outfile += f'{indent_child}</{structureAbbr}:Structure>'

        outfile += f'{indent}</{label}>'

        return outfile


class StructureType(DataParser):
    """Parser of the Structure of a DataFlowDefinition"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Structure"""
        return StructureType(*args_, **kwargs_)

    @property
    def ref(self):
        """Reference to the DataStructureDefinition"""
        return self._ref

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = f"{obj_.agencyID}:{obj_.id_}({obj_.version})"


class DataStructureComponentType(DataParser):
    """Parser of the DataStructureComponent XML element"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._measure_descriptor = None
        self._attribute_descriptor = None
        self._dimension_descriptor = None
        self._groupDimensionDescriptor = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataStructureComponentType"""
        return DataStructureComponentType(*args_, **kwargs_)

    @property
    def dimensionDescriptor(self):
        """An ordered set of metadata concepts that, combined, classify a
        statistical series, and whose values, when combined (the key) in an
        instance such as a data set, uniquely identify a specific
        observation """
        return self._dimension_descriptor

    @property
    def attributeDescriptor(self):
        """A set metadata concepts that define the attributes of a Data
        Structure Definition. """
        return self._attribute_descriptor

    @property
    def measureDescriptor(self):
        """A metadata concept that defines the measure of a Data Structure
        Definition """
        return self._measure_descriptor

    @property
    def groupDimensionDescriptor(self):
        """A set metadata concepts that define a partial key derived
           from the Dimension Descriptor in a Data Structure Definition."""
        return self._groupDimensionDescriptor

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DimensionList':
            obj_ = DimensionDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dimension_descriptor = obj_
        elif nodeName_ == 'AttributeList':
            obj_ = AttributeDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._attribute_descriptor = obj_
        elif nodeName_ == 'MeasureList':
            obj_ = MeasureDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._measure_descriptor = obj_
        elif nodeName_ == 'Group':
            obj_ = GroupDimensionDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._groupDimensionDescriptor = obj_
