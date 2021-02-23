import json

from .base import *
from .dataTypes import FacetType, FacetValueType
# from .extras import ConstrainableArtifact, ContentConstraint, AttachmentConstraint
from .itemScheme import Agency
from .utils import genericSetter, qName, intSetter, stringSetter
from ..common.refs import RefBaseType
from ..utils.data_parser import DataParser
from ..utils.xml_base import find_attr_value_


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


class TextFormatType(DataParser):
    def __init__(self, facets=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)

        if facets is None:
            self._facets = []
        else:
            self._facets = facets

    @staticmethod
    def factory(*args_, **kwargs_):
        return TextFormatType(*args_, **kwargs_)

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
            if isinstance(e, Facet):
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
        if isinstance(value, Facet):
            self._components.append(value)
        else:
            raise TypeError(f"The object has to be of the Facet")

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Enumeration':
            obj_ = EnumerationType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.codelist = obj_.codelist
        elif nodeName_ == 'TextFormat':
            obj_ = TextFormatType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._components = obj_.facets
        # TODO Parsing Name of the Codelist


class Component(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None, componentList=None):

        if annotations is None:
            annotations = []
        super(Component, self).__init__(id_=id_, uri=uri, annotations=annotations)

        self.local_representation = localRepresentation
        self.component_list = componentList
        self._concept_identity_ref = None

    def __eq__(self, other):
        if isinstance(other, Component):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._local_representation == other._local_representation and
                    self._concept_identity_ref == other._concept_identity_ref)
        else:
            return False

    @property
    def local_representation(self):
        return self._local_representation

    @property
    def component_list(self):
        return self._component_list

    @local_representation.setter
    def local_representation(self, value):
        self._local_representation = genericSetter(value, Representation)

    @component_list.setter
    def component_list(self, value):
        self._component_list = genericSetter(value, ComponentList)


class Dimension(Component):
    _urnType = "datastructure"
    _qName = qName("str", "Dimension")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        if annotations is None:
            annotations = []
        super(Dimension, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                        localRepresentation=localRepresentation)

        self.position = position

    def __eq__(self, other):
        if isinstance(other, Dimension):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._local_representation == other._local_representation and
                    self._position == other._position)
        else:
            return False

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = intSetter(value)


class MeasureDimension(Dimension):
    _qName = qName("str", "MeasureDimension")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        if annotations is None:
            annotations = []
        super(MeasureDimension, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                               localRepresentation=localRepresentation, position=position)

    def __eq__(self, other):
        if isinstance(other, MeasureDimension):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._local_representation == other._local_representation and
                    self._position == other._position)
        else:
            return False


class TimeDimension(Dimension):
    _qName = qName("str", "TimeDimension")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        if annotations is None:
            annotations = []
        super(TimeDimension, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                            localRepresentation=localRepresentation, position=position)

    def __eq__(self, other):
        if isinstance(other, TimeDimension):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._local_representation == other._local_representation and
                    self._position == other._position)
        else:
            return False


class Attribute(Component):
    _urnType = "datastructure"
    _qName = qName("str", "Attribute")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None,
                 usageStatus: str = None, relatedTo=None):
        if annotations is None:
            annotations = []
        super(Attribute, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                        localRepresentation=localRepresentation)

        self.usageStatus = usageStatus
        self.relatedTo = relatedTo

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._local_representation == other._local_representation and
                    self._usageStatus == other._usageStatus and
                    self._relatedTo == other._relatedTo)
        else:
            return False

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
        elif (isinstance(value, PrimaryMeasure) or (value == "NoSpecifiedRelationship") or
              isinstance(value, GroupDimensionDescriptor) or isinstance(value, Dimension) or
              all(isinstance(n, (PrimaryMeasure, Dimension)) for n in value)):
            self._relatedTo = value
        else:
            raise ValueError(
                "The value for related To has to be None, the object of the GroupDimensionDescriptor "
                "class or an object of the DimensionClass or an object of the PrimaryMeasure class")


class PrimaryMeasure(Component):
    _urnType = "datastructure"
    _qName = qName("str", "PrimaryMeasure")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None):

        if annotations is None:
            annotations = []
        super(PrimaryMeasure, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                             localRepresentation=localRepresentation)

    def __eq__(self, other):
        if isinstance(other, PrimaryMeasure):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._local_representation == other._local_representation)
        else:
            return False


class ComponentList(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 components=None):

        if annotations is None:
            annotations = []
        if components is None:
            components = []
        super(ComponentList, self).__init__(id_=id_, uri=uri, annotations=annotations)
        self._components = {}
        for c in components:
            self.addComponent(c)

    def __eq__(self, other):
        if isinstance(other, ComponentList):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._components == other._components)
        else:
            return False

    @property
    def components(self):
        return self._components

    def addComponent(self, value):
        if isinstance(value, (Dimension, Attribute, PrimaryMeasure)):
            value.componentList = self
            self._components[value.id] = value
        else:
            raise TypeError(
                f"The object has to be of the dim_type [Dimension, Attribute, PrimaryMeasure], "
                f"{value.__class__.__name__} provided")

    def __len__(self):
        return len(self.components)

    def __getitem__(self, value):
        return self.components[value]


class DimensionDescriptor(ComponentList):
    _componentType = Dimension
    _urnType = "datastructure"
    _qName = qName("str", "DimensionList")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 components=None):

        if annotations is None:
            annotations = []
        if components is None:
            components = []
        super(DimensionDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                  components=components)

    def __eq__(self, other):
        if isinstance(other, DimensionDescriptor):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._components == other._components)
        else:
            return False


class AttributeDescriptor(ComponentList):
    _componentType = Attribute
    _urnType = "datastructure"
    _qName = qName("str", "AttributeList")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 components=None):
        if components is None:
            components = []
        if annotations is None:
            annotations = []

        super(AttributeDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                  components=components)

    def __eq__(self, other):
        if isinstance(other, AttributeDescriptor):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._components == other._components)
        else:
            return False


class MeasureDescriptor(ComponentList):
    _componentType = PrimaryMeasure
    _urnType = "datastructure"
    _qName = qName("str", "MeasureList")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 components=None):

        if components is None:
            components = []
        if annotations is None:
            annotations = []
        super(MeasureDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                components=components)

    def __eq__(self, other):
        if isinstance(other, MeasureDescriptor):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._components == other._components)
        else:
            return False


class GroupDimensionDescriptor(ComponentList):
    _componentType = Dimension
    _urnType = "datastructure"
    _qName = qName("str", "Group")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 components=None):
        if components is None:
            components = []
        if annotations is None:
            annotations = []
        super(GroupDimensionDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                       components=components)


class DataStructureComponentType(DataParser):


class DataStructureDefinition(MaintainableArtefact, DataParser):
    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None, dimensionDescriptor: DimensionDescriptor = None,
                 measureDescriptor: MeasureDescriptor = None, attributeDescriptor: AttributeDescriptor = None,
                 groupDimensionDescriptor: GroupDimensionDescriptor = None):

        if annotations is None:
            annotations = []
        super(DataStructureDefinition, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                      name=name, description=description,
                                                      version=version, validFrom=validFrom, validTo=validTo,
                                                      isFinal=isFinal, isExternalReference=isExternalReference,
                                                      serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                      maintainer=maintainer)

        self.dimensionDescriptor = dimensionDescriptor
        self.measureDescriptor = measureDescriptor
        self.attributeDescriptor = attributeDescriptor
        self.groupDimensionDescriptor = groupDimensionDescriptor

        self._urnType = "datastructure"
        self._qName = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructure"

    def __eq__(self, other):
        if isinstance(other, DataStructureDefinition):
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
                    self._dimensionDescriptor == other._dimensionDescriptor and
                    self._attributeDescriptor == other._attributeDescriptor and
                    self._measureDescriptor == other._measureDescriptor)
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
        list_codes = []
        for k, v in self.dimensionDescriptor.components.items():
            if v.local_representation is not None and len(v.local_representation.facets) > 0:
                list_codes.append(k)

        if self.attributeDescriptor is not None:
            for k, v in self.attributeDescriptor.components.items():
                if v.local_representation is not None and len(v.local_representation.facets) > 0:
                    list_codes.append(k)

        if self.measureDescriptor is not None:
            for k, v in self.measureDescriptor.components.items():
                if v.local_representation is not None and len(v.local_representation.facets) > 0:
                    list_codes.append(k)
        return list_codes

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
        data_types_mapping = {
            "String": "String",
            "ObservationalTimePeriod": "Date",
            "BigInteger": "Integer"
        }

        dataset_name = self.id
        components = []
        for c in self.dimensionDescriptor.components:
            component = {"name": c.id, "role": "Identifier",
                         "dim_type": data_types_mapping[c.local_representation["dataType"]], "isNull": False}

            components.append(component)
        for c in self.attributeDescriptor.components:
            component = {"name": c.id, "role": "Attribute",
                         "dim_type": data_types_mapping[c.local_representation["dataType"]], "isNull": True}

            components.append(component)
        for c in self.measureDescriptor.components:
            component = {"name": c.id, "role": "Measure",
                         "dim_type": data_types_mapping[c.local_representation["dataType"]], "isNull": True}

            components.append(component)

        result = {"DataSet": {"name": dataset_name, "DataStructure": components}}
        with open(path, 'w') as fp:
            json.dump(result, fp)
        return result

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
        if nodeName_ == 'DataStructureComponents':
            obj_ = DataStructureComponentType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.append(obj_)

        # TODO Parse Name and Description
