"""
    Component file holds the classes for the Component and its derivatives
"""

import json
from datetime import datetime
from typing import List

from sdmxthon.model.base import InternationalString, MaintainableArtefact
from sdmxthon.model.component import Component
from sdmxthon.model.descriptors import AttributeDescriptor, ComponentList, \
    DimensionDescriptor, GroupDimensionDescriptor, MeasureDescriptor
from sdmxthon.model.extras import ReferencePeriod, ReleaseCalendar
from sdmxthon.model.header import Header, Party, Sender
from sdmxthon.model.utils import ConstraintRoleType, bool_setter, \
    generic_setter
from sdmxthon.parsers.writer_aux import create_namespaces, write_from_header, \
    parse_metadata, export_intern_data, add_indent, get_end_message
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import split_unique_id
from sdmxthon.utils.mappings import Data_Types_VTL, commonAbbr, structureAbbr


class MemberSelection(object):

    def __init__(self, is_included: bool = False,
                 values_for: Component = None, sel_value: list = None):
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
        if not isinstance(value, list):
            value = [value]
        self._selValue = generic_setter(value, list)

    @property
    def values_for(self):
        return self._values_for

    @values_for.setter
    def values_for(self, value):
        self._values_for = generic_setter(value, str)

    @property
    def is_included(self):
        return self._is_included

    @is_included.setter
    def is_included(self, value):
        self._is_included = bool_setter(value)


class CubeRegion(object):

    def __init__(self, is_included: bool = False,
                 member: List[MemberSelection] = None):
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
        self._member = generic_setter(value, list)

    @property
    def is_included(self):
        return self._is_included

    @is_included.setter
    def is_included(self, value):
        self._is_included = bool_setter(value)


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


class DataKeySet(object):

    def __init__(self, keys: list = None, isIncluded: bool = None):
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


class Constraint(MaintainableArtefact):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 name: InternationalString = None,
                 description: InternationalString = None,
                 version: str = None,
                 maintainer=None,
                 validFrom: datetime = None,
                 validTo: datetime = None,
                 isFinal: bool = None,
                 isExternalReference: bool = None,
                 serviceUrl: str = None,
                 structureUrl: str = None,
                 dataContentRegion: List[CubeRegion] = None,
                 dataKeySet: List[DataKeySet] = None,
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
                     maintainer=maintainer,
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

        self.data_content_keys = dataKeySet

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
        self._data_content_keys = generic_setter(value, list)

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


class KeySetType(object):
    def __init__(self):
        self._key = {}

    @property
    def key(self):
        return self._key


class ContentConstraint(Constraint):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 name: InternationalString = None,
                 description: InternationalString = None,
                 version: str = None,
                 maintainer=None,
                 validFrom: datetime = None,
                 validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None,
                 serviceUrl: str = None,
                 structureUrl: str = None,
                 dataContentRegion: List[CubeRegion] = None,
                 dataKeySet: List[DataKeySet] = None,
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
                     maintainer=maintainer,
                     validFrom=validFrom,
                     validTo=validTo,
                     isFinal=isFinal,
                     isExternalReference=isExternalReference,
                     serviceUrl=serviceUrl,
                     structureUrl=structureUrl,
                     dataContentRegion=dataContentRegion,
                     dataKeySet=dataKeySet,
                     metadataContentRegion=metadataContentRegion,
                     availableDates=availableDates,
                     calendar=calendar)
        if role is not None and role not in ConstraintRoleType:
            raise ValueError('ConstraintRole must be either '
                             '"allowableContent" or "actualContent"')
        self._role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in ConstraintRoleType:
            raise ValueError('ConstraintRole must be either '
                             '"Allowed" or "Actual"')
        self._role = value

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
            for i in self.data_content_keys:
                outfile += f'{indent_child}<{structureAbbr}:DataKeySet ' \
                           f'isIncluded="' \
                           f'{str(i.is_included).lower()}">'

                for e in i.keys:
                    outfile += f'{indent_child_2}<{structureAbbr}:Key>'

                    for k, v in e.items():
                        outfile += f'{indent_ref}<{commonAbbr}:KeyValue ' \
                                   f'id="{k}">'
                        outfile += f'{indent_value}<{commonAbbr}:Value>{v}' \
                                   f'</{commonAbbr}:Value>'
                        outfile += f'{indent_ref}</{commonAbbr}:KeyValue>'

                    outfile += f'{indent_child_2}</{structureAbbr}:Key>'

                outfile += f'{indent_child}</{structureAbbr}:DataKeySet>'

        if self.data_content_region is not None:

            for e in self.data_content_region:
                outfile += f'{indent_child}<{structureAbbr}:CubeRegion ' \
                           f'isIncluded="{str(e.is_included).lower()}">'
                for m in e.member:
                    outfile += f'{indent_child_2}<{commonAbbr}:KeyValue ' \
                               f'id="{m.values_for}">'
                    for j in m.sel_value:
                        outfile += f'{indent_ref}<{commonAbbr}:Value>{j}' \
                                   f'</{commonAbbr}:Value>'
                    outfile += f'{indent_child_2}</{commonAbbr}:KeyValue>'
                outfile += f'{indent_child}</{structureAbbr}:CubeRegion>'

        outfile += f'{indent}</{label}>'

        return outfile


def add_type_facets(key, value, type_, facets):
    if value.representation is not None:
        if value.representation.type_ is not None:
            type_[key] = value.representation.type_
        else:
            type_[key] = 'String'

        if len(value.representation.facets) > 0:
            facets[key] = value.representation.facets
    else:
        type_[key] = 'String'


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
                 dimension_list: DimensionDescriptor = None,
                 measure_list: MeasureDescriptor = None,
                 attribute_list: AttributeDescriptor = None,
                 group_dimension_descriptor: GroupDimensionDescriptor = None,
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

        self.dimension_descriptor = dimension_list
        self.measure_descriptor = measure_list
        self.attribute_descriptor = attribute_list
        self.group_dimension_descriptor = group_dimension_descriptor
        self._constraints = constraint

    def __eq__(self, other):
        if isinstance(other, DataStructureDefinition):
            return (super.__eq__(self, other) and
                    self._dimensionDescriptor == other._dimensionDescriptor and
                    self._attributeDescriptor == other._attributeDescriptor and
                    self._measureDescriptor == other._measureDescriptor and
                    self._groupDimensionDescriptor ==
                    other._groupDimensionDescriptor)

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
            add_type_facets(k, v, type_, facets)

        if self.attribute_descriptor is not None:
            for k, v in self.attribute_descriptor.components.items():
                add_type_facets(k, v, type_, facets)

        if self.measure_descriptor is not None:
            for k, v in self.measure_descriptor.components.items():
                add_type_facets(k, v, type_, facets)

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
                        for m in e.member:
                            if m.values_for not in cubes.keys():
                                cubes[m.values_for] = set(
                                    m.sel_value)
                            else:
                                cubes[m.values_for].update(
                                    m.sel_value)
                if (c.data_content_keys is not None and
                        len(c.data_content_keys) > 0):
                    for e in c.data_content_keys:
                        if c.role is not None and c.role == "Allowed":
                            series += e.keys

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
        NAME = "name"
        ROLE = "role"
        TYPE = "type"
        NULLABLE = "nullable"
        for c in self.dimension_descriptor.components.values():

            type_ = "String"

            if (c.representation is not None and
                    c.representation.type_ is not None):
                type_ = c.representation.type_

            component = {NAME: c.id, ROLE: "Identifier",
                         TYPE: Data_Types_VTL[type_], NULLABLE: False}

            components.append(component)
        if self.attribute_descriptor is not None:
            for c in self.attribute_descriptor.components.values():
                type_ = "String"

                if (c.representation is not None and
                        c.representation.type_ is not None):
                    type_ = c.representation.type_

                component = {NAME: c.id, ROLE: "Attribute",
                             TYPE: Data_Types_VTL[type_], NULLABLE: True}

                components.append(component)
        for c in self.measure_descriptor.components.values():
            type_ = "String"

            if (c.representation is not None and
                    c.representation.type_ is not None):
                type_ = c.representation.type_

            component = {NAME: c.id, ROLE: "Measure",
                         TYPE: Data_Types_VTL[type_], NULLABLE: True}

            components.append(component)

        result = {"datasets": [{"name": dataset_name,
                                "DataStructure": components}]}
        if path is not None:
            with open(path, 'w') as fp:
                json.dump(result, fp)
        else:
            return result

    def to_xml(self,
               output_path: str = '',
               header: Header = None,
               id_: str = 'test',
               test: str = 'true',
               prepared: datetime = None,
               sender: str = 'Unknown',
               receiver: str = 'Not_supplied',
               prettyprint=True):
        """
        Exports the DataStructureDefinition to a XML file in SDMX-ML 2.1 format

        :param output_path: Path to save the file, defaults to ''
        :type output_path: str

        :param prettyprint: Specifies if the output file is formatted
        :type prettyprint: bool

        :param header: Header to be written, defaults to None
        :type header: Header

        .. important::

            If the header argument is not None, rest of the below arguments
            will not be used

        :param id_: ID of the Header, defaults to 'test'
        :type id_: str

        :param test: Mark as test file, defaults to 'true'
        :type test: str

        :param prepared: Datetime of the preparation of the Message, \
        defaults to current date and time
        :type prepared: datetime

        :param sender: ID of the Sender, defaults to 'Unknown'
        :type sender: str

        :param receiver: ID of the Receiver, defaults to 'Not_supplied'
        :type receiver: str

        :returns: A str, if outputPath is ''
        """
        outfile = create_namespaces(
            type_=MessageTypeEnum.Metadata,
            payload=None,
            prettyprint=True
        )

        if header is None:
            header = Header(id_, test, prepared, Sender(sender),
                            [Party(receiver)])

        outfile += write_from_header(header, prettyprint,
                                     type_=MessageTypeEnum.Metadata)
        payload = {'DataStructures': {self.unique_id: self}}
        outfile += parse_metadata(payload=payload,
                                  prettyprint=prettyprint)
        outfile += get_end_message(type_=MessageTypeEnum.Metadata)
        if output_path != '':
            with open(output_path, "w", encoding="UTF-8",
                      errors='replace') as f:
                f.write(outfile)
        else:
            return outfile
        return outfile

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

        outfile += f'{indent_child}</{structureAbbr}:DataStructureComponents>' \
                   f'{indent}</{label}>'

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
            return (super(DataFlowDefinition, self).__eq__(other) and
                    self._structure == other._structure)

        return False

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
        if self._constraints is None:
            self._constraints = []
        self._constraints.append(value)

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
