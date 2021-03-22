"""
    Component file holds the classes for the Component and its derivatives
"""

import json
from datetime import datetime

from SDMXThon.parsers.data_parser import DataParser
from SDMXThon.parsers.references import RelationshipRefType, RefBaseType
from SDMXThon.utils.handlers import export_intern_data, add_indent
from SDMXThon.utils.mappings import *
from SDMXThon.utils.xml_base import find_attr_value_
from .base import IdentifiableArtefact, MaintainableArtefact, InternationalString
# from .extras import ConstrainableArtifact, ContentConstraint, AttachmentConstraint
from .representation import Representation
from .utils import genericSetter, intSetter


class Component(IdentifiableArtefact):
    """ A component is an abstract super class used to define qualitative and quantitative data
        and metadata items that belong to a Component List and hence a Structure.
        Component is refined through its sub-classes."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None):
        super(Component, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations)

        self._local_representation = localRepresentation
        self._concept_identity = None

    def __eq__(self, other):
        if isinstance(other, Component):
            return super(Component, self).__eq__(other) and self._local_representation == other._local_representation \
                   and self._concept_identity == other._concept_identity
        else:
            return False

    @property
    def local_representation(self):
        """Association to the Representation of the Component if this is different from
        the coreRepresentation of the Concept which the Component uses (ConceptUsage) """
        return self._local_representation

    @local_representation.setter
    def local_representation(self, value):
        self._local_representation = genericSetter(value, Representation)

    @property
    def concept_identity(self):
        """Association to a Concept in a Concept Scheme that
            identifies and defines the semantic of the Component"""
        return self._concept_identity

    @concept_identity.setter
    def concept_identity(self, value):
        self._concept_identity = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Component, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'ConceptIdentity':
            obj_ = ConceptIdentityType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.concept_identity = obj_.ref
        elif nodeName_ == 'LocalRepresentation':
            obj_ = Representation._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._local_representation = obj_

    def _parse_XML(self, indent, head):

        if isinstance(self, TimeDimension):
            head = 'TimeDimension'

        head = f'{structureAbbr}:' + head

        prettyprint = indent != ''

        data = super(Component, self)._to_XML(prettyprint)
        indent = add_indent(indent)
        if isinstance(self, Dimension):
            outfile = f'{indent}<{head}{data["Attributes"]} position="{self._position}">'
        elif isinstance(self, Attribute):
            outfile = f'{indent}<{head}{data["Attributes"]} assignmentStatus="{self._usageStatus}">'
        else:
            outfile = f'{indent}<{head}{data["Attributes"]}>'
        outfile += export_intern_data(data, indent)

        indent_child = add_indent(indent)

        if self.concept_identity is not None:
            indent_ref = add_indent(indent_child)
            outfile += f'{indent_child}<{structureAbbr}:ConceptIdentity>'
            outfile += f'{indent_ref}<Ref maintainableParentID="{self.concept_identity.scheme.id}" ' \
                       f'package="conceptscheme" ' \
                       f'maintainableParentVersion="{self.concept_identity.scheme.version}" ' \
                       f'agencyID="{self.concept_identity.scheme.agencyID}" id="{self.concept_identity.id}" ' \
                       f'class="Concept"/>'
            outfile += f'{indent_child}</{structureAbbr}:ConceptIdentity>'

        if self.local_representation is not None:
            indent_enum = add_indent(indent_child)
            indent_ref = add_indent(indent_enum)
            outfile += f'{indent_child}<{structureAbbr}:LocalRepresentation>'
            if self.local_representation.codelist is not None:
                label_format = 'EnumerationFormat'
                outfile += f'{indent_enum}<{structureAbbr}:Enumeration>'
                outfile += f'{indent_ref}<Ref package="codelist" ' \
                           f'agencyID="{self.local_representation.codelist.agencyID}" ' \
                           f'id="{self.local_representation.codelist.id}" ' \
                           f'version="{self.local_representation.codelist.version}" class="Codelist"/>'
                outfile += f'{indent_enum}</{structureAbbr}:Enumeration>'
            else:
                label_format = 'TextFormat'
            format_attributes = f' textType="{self.local_representation.type_}"'

            if self.local_representation.facets is not None:
                for e in self.local_representation.facets:
                    format_attributes += f' {e.facetType}="{e.facetValue}"'

            outfile += f'{indent_enum}<{structureAbbr}:{label_format}{format_attributes}/>'

            outfile += f'{indent_child}</{structureAbbr}:LocalRepresentation>'

            if isinstance(self, Attribute):
                outfile += f'{indent_child}<{structureAbbr}:AttributeRelationship>'

                if isinstance(self.relatedTo, dict):
                    for k in self.relatedTo.keys():
                        outfile += f'{indent_enum}<{structureAbbr}:Dimension>'
                        outfile += f'{indent_ref}<Ref id="{k}"/>'
                        outfile += f'{indent_enum}</{structureAbbr}:Dimension>'
                elif isinstance(self.relatedTo, Dimension):
                    outfile += f'{indent_enum}<{structureAbbr}:Dimension>'
                    outfile += f'{indent_ref}<Ref id="{self.relatedTo.id}"/>'
                    outfile += f'{indent_enum}</{structureAbbr}:Dimension>'
                elif isinstance(self.relatedTo, PrimaryMeasure):
                    outfile += f'{indent_enum}<{structureAbbr}:PrimaryMeasure>'
                    outfile += f'{indent_ref}<Ref id="{self.relatedTo.id}"/>'
                    outfile += f'{indent_enum}</{structureAbbr}:PrimaryMeasure>'
                else:
                    outfile += f'{indent_enum}<{structureAbbr}:None/>'

                outfile += f'{indent_child}</{structureAbbr}:AttributeRelationship>'

        outfile += f'{indent}</{head}>'
        return outfile


class Dimension(Component, DataParser):
    """ A metadata concept used (most probably together with other metadata concepts)
        to classify a statistical series, e.g. a statistical concept indicating a certain
        economic activity or a geographical reference area.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        super(Dimension, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                        localRepresentation=localRepresentation)

        self.position = position

    def __eq__(self, other):
        if isinstance(other, Dimension):
            return super(Dimension, self).__eq__(other) and self._position == other._position
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Dimension"""
        return Dimension(*args_, **kwargs_)

    @property
    def position(self):
        """Position of the Dimension in the DimensionList"""
        return self._position

    @position.setter
    def position(self, value):
        self._position = intSetter(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Dimension, self)._build_attributes(node, attrs, already_processed)

        value = find_attr_value_('position', node)
        if value is not None and 'position' not in already_processed:
            already_processed.add('position')
            self.position = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Dimension, self)._build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


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

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DimensionReference':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.ref


class MeasureDimension(Dimension, DataParser):
    """ A statistical concept that identifies the component in the key structure
        that has an enumerated list of measures. This dimension has, as its representation
        the Concept Scheme that enumerates the measure concepts.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        super(MeasureDimension, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                               localRepresentation=localRepresentation, position=position)

    def __eq__(self, other):
        if isinstance(other, MeasureDimension):
            return super(MeasureDimension, self).__eq__(other)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MeasureDimension"""
        return MeasureDimension(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(MeasureDimension, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(MeasureDimension, self)._build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class TimeDimension(Dimension, DataParser):
    """A metadata concept that identifies the component in the key structure
       that has the role of “time”.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        super(TimeDimension, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                            localRepresentation=localRepresentation, position=position)

    def __eq__(self, other):
        if isinstance(other, TimeDimension):
            return super(TimeDimension, self).__eq__(other)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of TimeDimension"""
        return TimeDimension(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(TimeDimension, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(TimeDimension, self)._build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class Attribute(Component, DataParser):
    """A characteristic of an object or entity."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 usageStatus: str = None, relatedTo=None):
        super(Attribute, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                        localRepresentation=localRepresentation)

        self.usageStatus = usageStatus
        self.relatedTo = relatedTo

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return super(Attribute, self).__eq__(other) and self._usageStatus == other._usageStatus \
                   and self._relatedTo == other._relatedTo
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Attribute"""
        return Attribute(*args_, **kwargs_)

    @property
    def usageStatus(self):
        """Defines the usage status of the Attribute (Mandatory, Conditional)"""
        return self._usageStatus

    @property
    def relatedTo(self):
        """Association to a AttributeRelationship."""
        return self._relatedTo

    @usageStatus.setter
    def usageStatus(self, value):
        if value in ["Mandatory", "Conditional"] or value is None:
            self._usageStatus = value
        else:
            raise ValueError("The value for usageStatus has to be 'Mandatory' or 'Conditional'")

    @relatedTo.setter
    def relatedTo(self, value):
        if value is None:
            self._relatedTo = "NoSpecifiedRelationship"
        else:
            self._relatedTo = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Attribute, self)._build_attributes(node, attrs, already_processed)

        value = find_attr_value_('assignmentStatus', node)
        if value is not None and 'assignmentStatus' not in already_processed:
            already_processed.add('assignmentStatus')
            self.usageStatus = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Attribute, self)._build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)

        if nodeName_ == 'AttributeRelationship':
            obj_ = AttributeRelationshipType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if obj_.ref_id is None:
                self.relatedTo = None
            else:
                self.relatedTo = {'id': obj_.ref_id, 'type': obj_.ref_type}


class PrimaryMeasure(Component, DataParser):
    """The metadata concept that is the phenomenon to be measured in a data set.
       In a data set the instance of the measure is often called the observation.

    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None):

        super(PrimaryMeasure, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                             localRepresentation=localRepresentation)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of PrimaryMeasure"""
        return PrimaryMeasure(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, PrimaryMeasure):
            return super(PrimaryMeasure, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(PrimaryMeasure, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(PrimaryMeasure, self)._build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class ComponentList(IdentifiableArtefact):
    """An abstract definition of a list of components.
       A concrete example is a Dimension Descriptor which defines
       the list of Dimensions in a DataStructure Definition.
    """
    _componentType = None

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):

        super(ComponentList, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations)
        self._components = {}
        if components is not None:
            for c in components:
                self.addComponent(c)

    def __eq__(self, other):
        if isinstance(other, ComponentList):
            return super(ComponentList, self).__eq__(other) and self._components == other._components
        else:
            return False

    @property
    def components(self):
        """An aggregate association to one or more components which make up the list."""
        return self._components

    def addComponent(self, value):
        """Method to add a Component to the ComponentList"""
        if isinstance(self, MeasureDescriptor) and len(self._components) == 1:
            raise ValueError('Measure Descriptor cannot have more than one Primary Measure')
        elif isinstance(value, (Dimension, Attribute, PrimaryMeasure)):
            value.componentList = self
            self._components[value.id] = value
        elif isinstance(value, GroupDimension):
            value.componentList = self
            self._components[value.ref] = value
        else:
            raise TypeError(
                f"The object has to be of the dim_type [Dimension, Attribute, PrimaryMeasure], "
                f"{value.__class__.__name__} provided")

    def __len__(self):
        return len(self.components)

    def __getitem__(self, value):
        return self.components[value]

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ComponentList, self)._build_attributes(node, attrs, already_processed)

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
    """An ordered set of metadata concepts that, combined, classify a statistical series,
       and whose values, when combined (the key) in an instance such as a data set,
       uniquely identify a specific observation
    """
    _componentType = "Dimension"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):

        if components is None:
            components = []
        super(DimensionDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
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
        super(DimensionDescriptor, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Dimension':
            obj_ = Dimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)
        elif nodeName_ == 'TimeDimension':
            obj_ = TimeDimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class AttributeDescriptor(ComponentList, DataParser):
    """A set metadata concepts that define the attributes of a Data Structure Definition."""

    _componentType = "Attribute"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):
        if components is None:
            components = []

        super(AttributeDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
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
        super(AttributeDescriptor, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Attribute':
            obj_ = Attribute._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class MeasureDescriptor(ComponentList, DataParser):
    """A metadata concept that defines the measure of a Data Structure Definition"""

    _componentType = "PrimaryMeasure"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):

        if components is None:
            components = []
        super(MeasureDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
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
        super(MeasureDescriptor, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'PrimaryMeasure':
            obj_ = PrimaryMeasure._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class GroupDimensionDescriptor(ComponentList, DataParser):
    """A set metadata concepts that define a partial key derived from the Dimension Descriptor in a
    Data Structure Definition.
    """

    _componentType = "Dimension"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):
        if components is None:
            components = []
        super(GroupDimensionDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                       components=components)

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
        super(GroupDimensionDescriptor, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'GroupDimension':
            obj_ = GroupDimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class DataStructureDefinition(MaintainableArtefact):
    """A collection of metadata concepts, their structure and usage when used to collect
       or disseminate data.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None, dimensionDescriptor: DimensionDescriptor = None,
                 measureDescriptor: MeasureDescriptor = None, attributeDescriptor: AttributeDescriptor = None,
                 groupDimensionDescriptor: GroupDimensionDescriptor = None):

        super(DataStructureDefinition, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                      name=name, description=description,
                                                      version=version, validFrom=validFrom, validTo=validTo,
                                                      isFinal=isFinal, isExternalReference=isExternalReference,
                                                      serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                      maintainer=maintainer)

        self.dimensionDescriptor = dimensionDescriptor
        self.measureDescriptor = measureDescriptor
        self.attributeDescriptor = attributeDescriptor
        self.groupDimensionDescriptor = groupDimensionDescriptor

    def __eq__(self, other):
        if isinstance(other, DataStructureDefinition):
            return super.__eq__(self, other) and self._dimensionDescriptor == other._dimensionDescriptor \
                   and self._attributeDescriptor == other._attributeDescriptor \
                   and self._measureDescriptor == other._measureDescriptor \
                   and self._groupDimensionDescriptor == other._groupDimensionDescriptor
        else:
            return False

    def __str__(self):
        return '<DataStructureDefinition  - %s:%s(%s)>' % (self.agencyID, self.id, self.version)

    def __unicode__(self):
        return u'<DataStructureDefinition  - %s:%s(%s)>' % (self.agencyID, self.id, self.version)

    def __repr__(self):
        return '<DataStructureDefinition  - %s:%s(%s)>' % (self.agencyID, self.id, self.version)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataStructureDefinition"""
        return DataStructureDefinition(*args_, **kwargs_)

    @property
    def dimensionDescriptor(self):
        """An ordered set of metadata concepts that, combined, classify a statistical series,
           and whose values, when combined (the key) in an instance such as a data set,
           uniquely identify a specific observation"""
        return self._dimensionDescriptor

    @property
    def measureDescriptor(self):
        """A metadata concept that defines the measure of a Data Structure Definition"""
        return self._measureDescriptor

    @property
    def attributeDescriptor(self):
        """A set metadata concepts that define the attributes of a Data Structure Definition."""
        return self._attributeDescriptor

    @property
    def groupDimensionDescriptor(self):
        """A set metadata concepts that define a partial key derived
           from the Dimension Descriptor in a Data Structure Definition."""
        return self._groupDimensionDescriptor

    @property
    def dimensionCodes(self):
        """Keys of the dimensionDescriptor components"""
        return [k for k in self.dimensionDescriptor.components]

    @property
    def attributeCodes(self):
        """Keys of the attributeDescriptor components"""
        if self.attributeDescriptor is not None:
            return [k for k in self.attributeDescriptor.components]
        else:
            return []

    @property
    def datasetAttributeCodes(self):
        """Attributes with no specified relationship"""
        result = []
        if self.attributeDescriptor is not None:
            for k in self.attributeDescriptor.components:
                if self.attributeDescriptor[k].relatedTo == "NoSpecifiedRelationship":
                    result.append(k)
        return result

    @property
    def observationAttributeCodes(self):
        """Attributes related to a Primary Measure"""
        result = []
        if self.attributeDescriptor is not None:
            for k in self.attributeDescriptor.components:
                if self.attributeDescriptor[k].relatedTo == "PrimaryMeasure":
                    result.append(k)
        return result

    @property
    def facetedObjects(self):
        """Returns any component that has facets"""
        facets = {}
        for k, v in self.dimensionDescriptor.components.items():
            if v.local_representation is not None:
                if len(v.local_representation.facets) > 0:
                    facets[k] = v.local_representation.facets
            elif v.concept_identity is not None and not \
                    isinstance(v.concept_identity, dict) and v.concept_identity.coreRepresentation is not None and \
                    len(v.concept_identity.coreRepresentation.facets) > 0:
                facets[k] = v.concept_identity.coreRepresentation.facets

        if self.attributeDescriptor is not None:
            for k, v in self.attributeDescriptor.components.items():
                if v.local_representation is not None:
                    if len(v.local_representation.facets) > 0:
                        facets[k] = v.local_representation.facets
                elif v.concept_identity is not None and not \
                        isinstance(v.concept_identity, dict) and v.concept_identity.coreRepresentation is not None and \
                        len(v.concept_identity.coreRepresentation.facets) > 0:
                    facets[k] = v.concept_identity.coreRepresentation.facets

        if self.measureDescriptor is not None:
            for k, v in self.measureDescriptor.components.items():
                if v.local_representation is not None:
                    if len(v.local_representation.facets) > 0:
                        facets[k] = v.local_representation.facets
                elif v.concept_identity is not None and not \
                        isinstance(v.concept_identity, dict) and v.concept_identity.coreRepresentation is not None and \
                        len(v.concept_identity.coreRepresentation.facets) > 0:
                    facets[k] = v.concept_identity.coreRepresentation.facets
        return facets

    @property
    def measureCode(self):
        """Key of the MeasureDescriptor component (PrimaryMeasure)"""
        return list(self.measureDescriptor.components.keys())[0]

    @dimensionDescriptor.setter
    def dimensionDescriptor(self, value):
        self._dimensionDescriptor = genericSetter(value, DimensionDescriptor)
        if value is not None:
            value.dsd = self

    @measureDescriptor.setter
    def measureDescriptor(self, value):
        self._measureDescriptor = genericSetter(value, MeasureDescriptor)
        if value is not None:
            value.dsd = self

    @attributeDescriptor.setter
    def attributeDescriptor(self, value):
        self._attributeDescriptor = genericSetter(value, AttributeDescriptor)
        if value is not None:
            value.dsd = self

    @groupDimensionDescriptor.setter
    def groupDimensionDescriptor(self, value):
        self._groupDimensionDescriptor = genericSetter(value, GroupDimensionDescriptor)
        if value is not None:
            value.dsd = self

    def to_vtl_json(self, path: str = None):
        """Formats the DataStructureDefinition as a VTL DataStructure"""
        dataset_name = self.id
        components = []
        for c in self.dimensionDescriptor.components.values():

            if c.local_representation is None:
                type_ = "String"
            elif c.local_representation.type_ is None:
                type_ = "String"
            else:
                type_ = c.local_representation.type_

            component = {"name": c.id, "role": "Identifier",
                         "type": Data_Types_VTL[type_], "isNull": False}

            components.append(component)
        for c in self.attributeDescriptor.components.values():
            if c.local_representation is None:
                type_ = "String"
            elif c.local_representation.type_ is None:
                type_ = "String"
            else:
                type_ = c.local_representation.type_

            component = {"name": c.id, "role": "Attribute",
                         "type": Data_Types_VTL[type_], "isNull": True}

            components.append(component)
        for c in self.measureDescriptor.components.values():
            if c.local_representation is None:
                type_ = "String"
            elif c.local_representation.type_ is None:
                type_ = "String"
            else:
                type_ = c.local_representation.type_

            component = {"name": c.id, "role": "Measure",
                         "type": Data_Types_VTL[type_], "isNull": True}

            components.append(component)

        result = {"DataSet": {"name": dataset_name, "DataStructure": components}}
        if path is not None:
            with open(path, 'w') as fp:
                fp.write(json.dumps(result))
        else:
            return result

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(DataStructureDefinition, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(DataStructureDefinition, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'DataStructureComponents':
            obj_ = DataStructureComponentType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._attributeDescriptor = obj_.attributeDescriptor
            self._dimensionDescriptor = obj_.dimensionDescriptor
            self._measureDescriptor = obj_.measureDescriptor
            self._groupDimensionDescriptor = obj_.groupDimensionDescriptor

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

        if self._dimensionDescriptor is not None:
            outfile += self._dimensionDescriptor._parse_XML(indent_child, f'{structureAbbr}:DimensionList')

        if self._attributeDescriptor is not None:
            outfile += self._attributeDescriptor._parse_XML(indent_child, f'{structureAbbr}:AttributeList')

        if self._measureDescriptor is not None:
            outfile += self._measureDescriptor._parse_XML(indent_child, f'{structureAbbr}:MeasureList')

        outfile += f'{indent_child}</{structureAbbr}:DataStructureComponents>'

        outfile += f'{indent}</{label}>'

        return outfile


class DataFlowDefinition(MaintainableArtefact):
    """Abstract concept (i.e. the structure without any data) of a flow of data
       that providers will provide for different reference periods.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None, structure: DataStructureDefinition = None):
        super(DataFlowDefinition, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                 name=name, description=description,
                                                 version=version, validFrom=validFrom, validTo=validTo,
                                                 isFinal=isFinal, isExternalReference=isExternalReference,
                                                 serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                 maintainer=maintainer)
        self.structure = structure

    def __eq__(self, other):
        if isinstance(other, DataFlowDefinition):
            return super(DataFlowDefinition, self).__eq__(other) and self._structure == other._structure

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
        self._structure = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(DataFlowDefinition, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(DataFlowDefinition, self)._build_children(child_, node, nodeName_, fromsubclass_=False,
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
            outfile += f'{indent_ref}<Ref id="{self.structure.id}" version="{self.structure.version}" ' \
                       f'agencyID="{self.structure.agencyID}" package="datastructure" class="DataStructure"/>'
            outfile += f'{indent_child}</{structureAbbr}:Structure>'

        outfile += f'{indent}</{label}>'

        return outfile


class AttributeRelationshipType(DataParser):
    """Parser of the Attribute Relationship"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref_id = None
        self._ref_type = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of AttributeRelationshipType"""
        return AttributeRelationshipType(*args_, **kwargs_)

    @property
    def ref_id(self):
        """ID of the component referenced"""
        return self._ref_id

    @property
    def ref_type(self):
        """Type of the component referenced (Dimension, PrimaryMeasure)"""
        return self._ref_type

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'None':
            self._ref_id = None
            self._ref_type = None
        elif nodeName_ == 'PrimaryMeasure':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref_id = obj_.ref
            self._ref_type = 'PrimaryMeasure'
        elif nodeName_ == 'Dimension':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._ref_id is None:
                self._ref_id = obj_.ref
            elif not isinstance(self._ref_id, list):
                self._ref_id = [self._ref_id]
            if isinstance(self._ref_id, list):
                self._ref_id.append(obj_.ref)
            self._ref_type = 'Dimension'


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

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = f"{obj_.agencyID}:{obj_.id_}({obj_.version})"


class ConceptIdentityType(DataParser):
    """Parser of the Concept Identity of a Component"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of ConceptIdentityType"""
        return ConceptIdentityType(*args_, **kwargs_)

    @property
    def ref(self):
        """Reference to a Concept in the Concept Identity, specifying the
        Concept Scheme unique ID and Concept ID in it"""
        return self._ref

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = {"CS": f"{obj_.agencyID}:{obj_.maintainableParentID}({obj_.maintainableParentVersion})",
                         "CON": f"{obj_.id_}"}


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
        """An ordered set of metadata concepts that, combined, classify a statistical series,
           and whose values, when combined (the key) in an instance such as a data set,
           uniquely identify a specific observation"""
        return self._dimension_descriptor

    @property
    def attributeDescriptor(self):
        """A set metadata concepts that define the attributes of a Data Structure Definition."""
        return self._attribute_descriptor

    @property
    def measureDescriptor(self):
        """A metadata concept that defines the measure of a Data Structure Definition"""
        return self._measure_descriptor

    @property
    def groupDimensionDescriptor(self):
        """A set metadata concepts that define a partial key derived
           from the Dimension Descriptor in a Data Structure Definition."""
        return self._groupDimensionDescriptor

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
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
