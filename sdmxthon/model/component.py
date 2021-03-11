import json

from .base import *
# from .extras import ConstrainableArtifact, ContentConstraint, AttachmentConstraint
from .itemScheme import Representation
from .references import RelationshipRefType, RefBaseType
from .utils import genericSetter, intSetter
from ..parsers.data_parser import DataParser
from ..utils.mappings import Data_Types_VTL
from ..utils.xml_base import find_attr_value_


class Component(IdentifiableArtefact):
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
        return self._local_representation

    @local_representation.setter
    def local_representation(self, value):
        self._local_representation = genericSetter(value, Representation)

    @property
    def concept_identity(self):
        return self._concept_identity

    @concept_identity.setter
    def concept_identity(self, value):
        self._concept_identity = value

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
        if nodeName_ == 'ConceptIdentity':
            obj_ = ConceptIdentityType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.concept_identity = obj_.ref
        elif nodeName_ == 'LocalRepresentation':
            obj_ = Representation.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._local_representation = obj_


class Dimension(Component, DataParser):
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
    def factory(*args_, **kwargs_):
        return Dimension(*args_, **kwargs_)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = intSetter(value)

    def build_attributes(self, node, attrs, already_processed):
        super(Dimension, self).build_attributes(node, attrs, already_processed)

        value = find_attr_value_('position', node)
        if value is not None and 'position' not in already_processed:
            already_processed.add('position')
            self.position = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(Dimension, self).build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class GroupDimension(DataParser):
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
        return self._ref

    @staticmethod
    def factory(*args_, **kwargs_):
        return GroupDimension(*args_, **kwargs_)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DimensionReference':
            obj_ = RelationshipRefType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.ref


class MeasureDimension(Dimension, DataParser):
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
    def factory(*args_, **kwargs_):
        return MeasureDimension(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        super(MeasureDimension, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(MeasureDimension, self).build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class TimeDimension(Dimension, DataParser):
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
    def factory(*args_, **kwargs_):
        return TimeDimension(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        super(TimeDimension, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(TimeDimension, self).build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class Attribute(Component, DataParser):
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
    def factory(*args_, **kwargs_):
        return Attribute(*args_, **kwargs_)

    @property
    def usageStatus(self):
        return self._usageStatus

    @property
    def relatedTo(self):
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

    def build_attributes(self, node, attrs, already_processed):
        super(Attribute, self).build_attributes(node, attrs, already_processed)

        value = find_attr_value_('assignmentStatus', node)
        if value is not None and 'assignmentStatus' not in already_processed:
            already_processed.add('assignmentStatus')
            self.usageStatus = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(Attribute, self).build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)

        if nodeName_ == 'AttributeRelationship':
            obj_ = AttributeRelationshipType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.ref_id is None:
                self.relatedTo = None
            else:
                self.relatedTo = {'id': obj_.ref_id, 'type': obj_.ref_type}


class PrimaryMeasure(Component, DataParser):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 localRepresentation: Representation = None):

        super(PrimaryMeasure, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                             localRepresentation=localRepresentation)

    @staticmethod
    def factory(*args_, **kwargs_):
        return PrimaryMeasure(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, PrimaryMeasure):
            return super(PrimaryMeasure, self).__eq__(other)
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(PrimaryMeasure, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(PrimaryMeasure, self).build_children(child_, node, nodeName_, fromsubclass_=False, gds_collector_=None)


class ComponentList(IdentifiableArtefact):
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
        return self._components

    def addComponent(self, value):
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

    def build_attributes(self, node, attrs, already_processed):
        super(ComponentList, self).build_attributes(node, attrs, already_processed)


class DimensionDescriptor(ComponentList, DataParser):
    _componentType = Dimension

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):

        if components is None:
            components = []
        super(DimensionDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                  components=components)

    @staticmethod
    def factory(*args_, **kwargs_):
        return DimensionDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, DimensionDescriptor):
            return super(DimensionDescriptor, self).__eq__(other)
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(DimensionDescriptor, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Dimension':
            obj_ = Dimension.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)
        elif nodeName_ == 'TimeDimension':
            obj_ = TimeDimension.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class AttributeDescriptor(ComponentList, DataParser):
    _componentType = Attribute

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):
        if components is None:
            components = []

        super(AttributeDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                  components=components)

    @staticmethod
    def factory(*args_, **kwargs_):
        return AttributeDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, AttributeDescriptor):
            return super(AttributeDescriptor, self).__eq__(other)
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(AttributeDescriptor, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Attribute':
            obj_ = Attribute.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class MeasureDescriptor(ComponentList, DataParser):
    _componentType = PrimaryMeasure

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 components=None):

        if components is None:
            components = []
        super(MeasureDescriptor, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                components=components)

    @staticmethod
    def factory(*args_, **kwargs_):
        return MeasureDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, MeasureDescriptor):
            return super(MeasureDescriptor, self).__eq__(other)
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(MeasureDescriptor, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PrimaryMeasure':
            obj_ = PrimaryMeasure.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class GroupDimensionDescriptor(ComponentList, DataParser):
    _componentType = Dimension

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
    def factory(*args_, **kwargs_):
        return GroupDimensionDescriptor(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        super(GroupDimensionDescriptor, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'GroupDimension':
            obj_ = GroupDimension.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.addComponent(obj_)


class DataStructureDefinition(MaintainableArtefact):
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
    def factory(*args_, **kwargs_):
        return DataStructureDefinition(*args_, **kwargs_)

    @property
    def dimensionDescriptor(self):
        return self._dimensionDescriptor

    @property
    def measureDescriptor(self):
        return self._measureDescriptor

    @property
    def attributeDescriptor(self):
        return self._attributeDescriptor

    @property
    def groupDimensionDescriptor(self):
        return self._groupDimensionDescriptor

    @property
    def dimensionCodes(self):
        return [k for k in self.dimensionDescriptor.components]

    @property
    def attributeCodes(self):
        if self.attributeDescriptor is not None:
            return [k for k in self.attributeDescriptor.components]
        else:
            return []

    @property
    def datasetAttributeCodes(self):
        result = []
        if self.attributeDescriptor is not None:
            for k in self.attributeDescriptor.components:
                if self.attributeDescriptor[k].relatedTo == "NoSpecifiedRelationship":
                    result.append(k)
        return result

    @property
    def observationAttributeCodes(self):
        result = []
        if self.attributeDescriptor is not None:
            for k in self.attributeDescriptor.components:
                if self.attributeDescriptor[k].relatedTo == "PrimaryMeasure":
                    result.append(k)
        return result

    @property
    def facetedObjects(self):
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

    def toVtlJson(self, path):
        dataset_name = self.id
        components = []
        for c in self.dimensionDescriptor.components.values():

            if c.local_representation.type_ is None:
                type_ = "String"
            else:
                type_ = c.local_representation.type_

            component = {"name": c.id, "role": "Identifier",
                         "type": Data_Types_VTL[type_], "isNull": False}

            components.append(component)
        for c in self.attributeDescriptor.components.values():

            if c.local_representation.type_ is None:
                type_ = "String"
            else:
                type_ = c.local_representation.type_

            component = {"name": c.id, "role": "Attribute",
                         "type": Data_Types_VTL[type_], "isNull": True}

            components.append(component)
        for c in self.measureDescriptor.components.values():

            if c.local_representation.type_ is None:
                type_ = "String"
            else:
                type_ = c.local_representation.type_

            component = {"name": c.id, "role": "Measure",
                         "type": Data_Types_VTL[type_], "isNull": True}

            components.append(component)

        result = {"DataSet": {"name": dataset_name, "DataStructure": components}}
        with open(path, 'w') as fp:
            fp.write(json.dumps(result))
        return result

    def build_attributes(self, node, attrs, already_processed):
        super(DataStructureDefinition, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):

        super(DataStructureDefinition, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'DataStructureComponents':
            obj_ = DataStructureComponentType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._attributeDescriptor = obj_.attributeDescriptor
            self._dimensionDescriptor = obj_.dimensionDescriptor
            self._measureDescriptor = obj_.measureDescriptor
            self._groupDimensionDescriptor = obj_.groupDimensionDescriptor


class DataFlowDefinition(MaintainableArtefact):
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
    def factory(*args_, **kwargs_):
        return DataFlowDefinition(*args_, **kwargs_)

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        self._structure = value

    def build_attributes(self, node, attrs, already_processed):
        super(DataFlowDefinition, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(DataFlowDefinition, self).build_children(child_, node, nodeName_, fromsubclass_=False,
                                                       gds_collector_=None)
        if nodeName_ == 'Structure':
            obj_ = StructureType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structure = obj_.ref


class AttributeRelationshipType(DataParser):
    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref_id = None
        self._ref_type = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return AttributeRelationshipType(*args_, **kwargs_)

    @property
    def ref_id(self):
        return self._ref_id

    @property
    def ref_type(self):
        return self._ref_type

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'None':
            self._ref_id = None
            self._ref_type = None
        elif nodeName_ == 'PrimaryMeasure':
            obj_ = RelationshipRefType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref_id = obj_.ref
            self._ref_type = 'PrimaryMeasure'
        elif nodeName_ == 'Dimension':
            obj_ = RelationshipRefType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if self._ref_id is None:
                self._ref_id = obj_.ref
            elif not isinstance(self._ref_id, list):
                self._ref_id = [self._ref_id]
            if isinstance(self._ref_id, list):
                self._ref_id.append(obj_.ref)
            self._ref_type = 'Dimension'


class StructureType(DataParser):
    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureType(*args_, **kwargs_)

    @property
    def ref(self):
        return self._ref

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = RefBaseType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = f"{obj_.agencyID}:{obj_.id_}({obj_.version})"


class ConceptIdentityType(DataParser):
    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return ConceptIdentityType(*args_, **kwargs_)

    @property
    def ref(self):
        return self._ref

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = RefBaseType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = {"CS": f"{obj_.agencyID}:{obj_.maintainableParentID}({obj_.maintainableParentVersion})",
                         "CON": f"{obj_.id_}"}


class DataStructureComponentType(DataParser):
    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._measure_descriptor = None
        self._attribute_descriptor = None
        self._dimension_descriptor = None
        self._groupDimensionDescriptor = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataStructureComponentType(*args_, **kwargs_)

    @property
    def dimensionDescriptor(self):
        return self._dimension_descriptor

    @property
    def attributeDescriptor(self):
        return self._attribute_descriptor

    @property
    def measureDescriptor(self):
        return self._measure_descriptor

    @property
    def groupDimensionDescriptor(self):
        return self._groupDimensionDescriptor

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DimensionList':
            obj_ = DimensionDescriptor.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dimension_descriptor = obj_
        elif nodeName_ == 'AttributeList':
            obj_ = AttributeDescriptor.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._attribute_descriptor = obj_
        elif nodeName_ == 'MeasureList':
            obj_ = MeasureDescriptor.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._measure_descriptor = obj_
        elif nodeName_ == 'Group':
            obj_ = GroupDimensionDescriptor.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._groupDimensionDescriptor = obj_
