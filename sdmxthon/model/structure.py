import json

from .base import *
from .dataTypes import FacetType, FacetValueType
from .itemScheme import Concept, CodeList, ConceptScheme
from .utils import genericSetter, qName, intSetter, stringSetter


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


class Representation:
    def __init__(self, concept: Concept = None, facets=None,
                 codeList: CodeList = None, conceptScheme: ConceptScheme = None):
        self._components = []
        if facets is None:
            facets = []
        for f in facets:
            self.addFacet(f)
        self.concept = concept
        self.codeList = codeList
        self.conceptScheme = conceptScheme

        self._conceptReference = None
        self._codeListReference = None
        self._conceptSchemeReference = None

    def __eq__(self, other):
        if isinstance(other, Representation):
            return (self._concept == other._concept and
                    self._codeList == other._codeList and
                    self._conceptScheme == other._conceptScheme and
                    self._conceptReference == other._conceptReference and
                    self._codeListReference == other._codeListReference and
                    self._conceptSchemeReference == other._conceptReference)
        else:
            return False

    @property
    def concept(self):
        return self._concept

    @property
    def facets(self):
        facets = []
        for e in self._components:
            if isinstance(e, Facet):
                facets.append(e)
        return facets

    @property
    def codeList(self):
        return self._codeList

    @property
    def conceptScheme(self):
        return self._conceptScheme

    @concept.setter
    def concept(self, value):
        self._concept = genericSetter(value, Concept)

    @codeList.setter
    def codeList(self, value):
        self._codeList = genericSetter(value, CodeList)

    @conceptScheme.setter
    def conceptScheme(self, value):
        self._conceptScheme = genericSetter(value, ConceptScheme)

    def addFacet(self, value):
        if isinstance(value, Facet):
            self._components.append(value)
        else:
            raise TypeError(f"The object has to be of the Facet")


class Component(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 localRepresentation: Representation = None, componentList=None):

        if annotations is None:
            annotations = []
        super(Component, self).__init__(id_=id_, uri=uri, annotations=annotations)

        self.localRepresentation = localRepresentation
        self.componentList = componentList
        self._conceptIdentityRef = None

    def __eq__(self, other):
        if isinstance(other, Component):
            return (self._id == other._id and
                    self.uri == other.uri and
                    self._annotations == other._annotations and
                    self._localRepresentation == other._localRepresentation and
                    self._conceptIdentityRef == other._conceptIdentityRef)
        else:
            return False

    @property
    def localRepresentation(self):
        return self._localRepresentation

    @property
    def componentList(self):
        return self._componentList

    @localRepresentation.setter
    def localRepresentation(self, value):
        self._localRepresentation = genericSetter(value, Representation)

    @componentList.setter
    def componentList(self, value):
        self._componentList = genericSetter(value, ComponentList)

    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.datastructure.{self.__class__.__name__}=" \
                  f"{self.componentList.dsd.maintainer.id}:{self.componentList.dsd.id}" \
                  f"({self.componentList.dsd.version}).{self.id}"
        except:
            urn = ""
        return urn


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
                    self._localRepresentation == other._localRepresentation and
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
                    self._localRepresentation == other._localRepresentation and
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
                    self._localRepresentation == other._localRepresentation and
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
                    self._localRepresentation == other._localRepresentation and
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

    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.datastructure.DataAttribute={self.componentList.dsd.maintainer.id}:" \
                  f"{self.componentList.dsd.id}({self.componentList.dsd.version}).{self.id}"
        except:
            urn = ""
        return urn


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
                    self._localRepresentation == other._localRepresentation)
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

    """
    @property
    def dsd(self):
        return self._dsd

    @dsd.setter
    def dsd(self, value):
        self._dsd = genericSetter(value, DataStructureDefinition)
    """

    def addComponent(self, value):
        if isinstance(value, (Dimension, Attribute, PrimaryMeasure)):
            value.componentList = self
            self._components[value.id] = value
        else:
            raise TypeError(
                f"The object has to be of the dim_type [Dimension, Attribute, PrimaryMeasure], "
                f"{value.__class__.__name__} provided")

    """
    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.datastructure.{self.__class__.__name__}={self.dsd.maintainer.id}:{self.dsd.id}({self.dsd.version}).{self.id}"
        except:
            urn = ""
        return urn
    """

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


class DataStructureDefinition(MaintainableArtefact):
    _urnType = "datastructure"
    _qName = qName("str", "DataStructure")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 dimensionDescriptor: DimensionDescriptor = None, measureDescriptor: MeasureDescriptor = None,
                 attributeDescriptor: AttributeDescriptor = None,
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
        return '<DataStructureDefinition  - %s:%s(%s)>' % (self.agencyId, self.id, self.version)

    def __unicode__(self):
        return u'<DataStructureDefinition  - %s:%s(%s)>' % (self.agencyId, self.id, self.version)

    def __repr__(self):
        return '<DataStructureDefinition  - %s:%s(%s)>' % (self.agencyId, self.id, self.version)

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
        rslt = []
        if self.attributeDescriptor is not None:
            for k in self.attributeDescriptor.components:
                if self.attributeDescriptor[k].relatedTo == "NoSpecifiedRelationship":
                    rslt.append(k)
        return rslt

    @property
    def observationAttributeCodes(self):
        rslt = []
        if self.attributeDescriptor is not None:
            for k in self.attributeDescriptor.components:
                if self.attributeDescriptor[k].relatedTo == "PrimaryMeasure":
                    rslt.append(k)
        return rslt

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
        dataTypesMapping = {
            "String": "String",
            "ObservationalTimePeriod": "Date",
            "BigInteger": "Integer"
        }

        datasetName = self.id
        components = []
        for c in self.dimensionDescriptor.components:
            component = {"name": c.id, "role": "Identifier",
                         "dim_type": dataTypesMapping[c.localRepresentation["dataType"]], "isNull": False}

            components.append(component)
        for c in self.attributeDescriptor.components:
            component = {"name": c.id, "role": "Attribute",
                         "dim_type": dataTypesMapping[c.localRepresentation["dataType"]], "isNull": True}

            components.append(component)
        for c in self.measureDescriptor.components:
            component = {"name": c.id, "role": "Measure",
                         "dim_type": dataTypesMapping[c.localRepresentation["dataType"]], "isNull": True}

            components.append(component)

        rslt = {"DataSet": {"name": datasetName, "DataStructure": components}}
        with open(path, 'w') as fp:
            json.dump(rslt, fp)
        return rslt


class DataFlowDefinition(MaintainableArtefact):
    _urnType = "datastructure"
    _qName = qName("str", "Dataflow")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 structure: DataStructureDefinition = None):
        if annotations is None:
            annotations = []
        super(DataFlowDefinition, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                 name=name, description=description,
                                                 version=version, validFrom=validFrom, validTo=validTo,
                                                 isFinal=isFinal, isExternalReference=isExternalReference,
                                                 serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                 maintainer=maintainer)
        self.structure = structure

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        self._structure = genericSetter(value, DataStructureDefinition)
