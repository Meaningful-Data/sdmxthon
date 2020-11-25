import json
import warnings
from typing import Dict

from .base import *
from .dataTypes import FacetType, FacetValueType
from .itemScheme import Concept, CodeList, ConceptScheme, Agency
from .utils import genericSetter, qName, getReferences, intSetter, getNameAndDescription, stringSetter


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
                raise ValueError(f"The facet type {value} is not recognised")
        else:
            raise ValueError("Facet type should be of the str type")

    @facetValue.setter
    def facetValue(self, value):
        self._facetValue = stringSetter(value)

    @facetValueType.setter
    def facetValueType(self, value):
        if isinstance(value, str) or value is None:
            if value in FacetValueType or value is None:
                self._facetValueType = value
            else:
                raise ValueError(f"The facet value type {value} is not recognised")
        else:
            raise ValueError("Facet value type should be of the str type")


class Representation:
    # TODO: Method to get the objects from the reference
    def __init__(self, concept: Concept = None, facets: list() = [],
                 codeList: CodeList = None, conceptScheme: ConceptScheme = None):
        self.concept = concept
        self.codeList = codeList
        self.conceptScheme = conceptScheme

        for f in facets:
            self.addFacet(f)

        self._conceptReference = None
        self._codeListReference = None
        self._conceptSchemeReference = None

    @property
    def concept(self):
        return self._concept

    @property
    def facets(self):
        return self._facets

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
            raise TypeError(f"The object has to be of the type Facet")


class Component(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 localRepresentation: Representation = None, componentList=None):

        super(Component, self).__init__(id_=id_, uri=uri, annotations=annotations)

        self.localRepresentation = localRepresentation
        self.componentList = componentList
        self._conceptIdentityRef = None

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
            urn = f"urn:sdmx:org.sdmx.infomodel.datastructure.{self.__class__.__name__}={self.componentList.dsd.maintainer.id}:{self.componentList.dsd.id}({self.componentList.dsd.version}).{self.id}"
        except:
            urn = ""
        return urn

    def toXml(self):
        xml = super().toXml()
        if self.__class__ == Dimension:
            xml.attrib["position"] = str(self.position)
        if self.__class__ == Attribute:
            xml.attrib["assignmentStatus"] = "Conditional"  # Hard coded

        if self.localRepresentation.concept is not None:
            concept = etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptIdentity")
            attrib = {
                "agencyID": "RBI",
                ##Hardcoded! For solving it, just add the scheme object to the concept (i.e. the concept scheme should be an attribute of concept)
                "class": "Concept",
                "id": self.representation.concept.id,
                "maintainableParentID": "RBI_CONCEPTS",  ##Hardcoded
                "maintainableParentVersion": "1.0",
                "package": "conceptscheme"
            }

            ref = etree.Element("Ref", attrib=attrib)

            concept.append(ref)
            xml.append(concept)

        localRep = etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}LocalRepresentation")
        if self.representation.codeList is not None:
            enum = etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration")

            attrib = {
                "agencyID": "RBI",
                ##Hardcoded! For solving it, just add the scheme object to the concept (i.e. the concept scheme should be an attribute of concept)
                "class": "Codelist",
                "id": self.representation.codeList.id,
                "package": "codelist",
                "version": "1.0"
            }

            ref = etree.Element("Ref", attrib=attrib)

            enum.append(ref)
            localRep.append(enum)
        elif self.id == "TIME_PERIOD":
            localRep.append(etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat",
                                          attrib={
                                              "textType": "GregorianDay"}))  # Harcoded! What's the link with facets?
        else:
            localRep.append(etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat",
                                          attrib={"textType": "String"}))  # Harcoded! What's the link with facets?

        xml.append(localRep)

        if self.__class__ == Attribute:  # Hard coded
            attachment = etree.Element(
                "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}AttributeRelationship")
            pm = etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}PrimaryMeasure")
            pm.append(etree.Element("Ref", attrib={"id": "OBS_VALUE"}))
            attachment.append(pm)
            xml.append(attachment)

        return xml

    @classmethod
    def fromXml(cls, elem):
        # 1. Instantiate the right class
        componentType = etree.QName(elem).localname

        inst = globals()[componentType]()

        # 2. Get common attributes
        inst.id = elem.get("id")

        # 3. Get references
        # 3.1 Get concept identity
        conceptIdentity = elem.find(qName("str", "ConceptIdentity"))
        if conceptIdentity is None:
            raise ValueError("Component {inst.id} does not have a ConceptIdentity")

        inst._conceptIdentityRef = getReferences(conceptIdentity)

        # 3.2 Get local representation. TODO get facets
        localRepresentation = elem.find(qName("str", "LocalRepresentation"))
        if localRepresentation is not None:
            lr = Representation()
            enumeration = localRepresentation.find(qName("str", "Enumeration"))

            if enumeration is not None:
                lr._codeListReference = getReferences(enumeration)
                inst.localRepresentation = lr

        # 4. Get position for dimension
        if isinstance(inst, Dimension):
            inst.position = elem.get("position")

        # 5. Get usageStatus  and  realatedTo for attribute
        if isinstance(inst, Attribute):
            inst.usageStatus = elem.get("assignmentStatus")

            # TODO: Get attributes relationships to dimensions or dimension groups
            relationship = elem.find(qName("str", "AttributeRelationship"))
            if relationship is not None:
                if relationship.find(qName("str", "PrimaryMeasure")) is not None:
                    inst.relatedTo = "PrimaryMeasure"
                elif relationship.find(qName("str", "None")) is not None:
                    inst.relatedTo = "NoSpecifiedRelationship"
                else:
                    warnings.warn(f"Relationship for attribute {inst.id} could not be extracted")

        return inst


class Dimension(Component):
    _urnType = "datastructure"
    _qName = qName("str", "Dimension")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 localRepresentation: Representation = None,
                 position: int = None):
        super(Dimension, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                        localRepresentation=localRepresentation)

        self.position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = intSetter(value)


class MeasureDimension(Dimension):
    _qName = qName("str", "MeasureDimension")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 localRepresentation: Representation = None,
                 position: int = None):
        super(MeasureDimension, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                               localRepresentation=localRepresentation, position=position)


class TimeDimension(Dimension):
    _qName = qName("str", "TimeDimension")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 localRepresentation: Representation = None,
                 position: int = None):
        super(TimeDimension, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                            localRepresentation=localRepresentation, position=position)


class Attribute(Component):
    _urnType = "datastructure"
    _qName = qName("str", "Attribute")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 localRepresentation: Representation = None,
                 usageStatus: str = None, relatedTo=None):

        super(Attribute, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                        localRepresentation=localRepresentation)

        self.usageStatus = usageStatus
        self.relatedTo = relatedTo

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
            raise ValueError("The value for usageStatus has to be 'mandatory' or 'conditional'")

    @relatedTo.setter
    def relatedTo(self, value):
        if value is None:
            self._relatedTo = "NoSpecifiedRelationship"
        elif value == "PrimaryMeasure" or value == "NoSpecifiedRelationship" or isinstance(value,
                                                                                           GroupDimensionDescriptor) or isinstance(
            value, Dimension):
            self._relatedTo = value
        else:
            raise ValueError(
                "The value for related To has to be None, 'PrimaryMeasure' an object of the GroupDimensionDescriptor class or an object of the DimensionClass")

    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.datastructure.DataAttribute={self.componentList.dsd.maintainer.id}:{self.componentList.dsd.id}({self.componentList.dsd.version}).{self.id}"
        except:
            urn = ""
        return urn


class PrimaryMeasure(Component):
    _urnType = "datastructure"
    _qName = qName("str", "PrimaryMeasure")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 localRepresentation: Representation = None):
        super(PrimaryMeasure, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                             localRepresentation=localRepresentation)


class ComponentList(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 components: Dict = [], dsd=None):

        super(ComponentList, self).__init__(id_=id_, uri=uri, annotations=annotations)

        self._components = {}
        for c in components:
            self.addComponent(c)

    @property
    def components(self):
        return self._components

    @property
    def dsd(self):
        return self._dsd

    @dsd.setter
    def dsd(self, value):
        self._dsd = genericSetter(value, DataStructureDefinition)

    def addComponent(self, value):
        if isinstance(value, self._componentType):
            value.componentList = self
            self._components[value.id] = value
        else:
            raise TypeError(
                f"The object has to be of the type {self._componentType.__name__}, {value.__class__.__name__} provided")

    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.datastructure.{self.__class__.__name__}={self.dsd.maintainer.id}:{self.dsd.id}({self.dsd.version}).{self.id}"
        except:
            urn = ""
        return urn

    def __len__(self):
        return len(self.components)

    def __getitem__(self, value):
        return self.components[value]

    def toXml(self):
        xml = super().toXml()
        for c in self.components:
            xml.append(c.toXml())

        return xml

    @classmethod
    def fromXml(cls, elem: etree._Element):
        # 1. Instantiate the right class
        componentListType = etree.QName(elem).localname

        objectsMapping = {
            "DimensionList": DimensionDescriptor,
            "AttributeList": AttributeDescriptor,
            "MeasureList": MeasureDescriptor,
            "GroupDimensionList": GroupDimensionDescriptor
        }

        inst = objectsMapping[componentListType]()

        # 2. Get id (only attribute)
        inst.id = elem.get("id")

        # 3. get components
        components = elem.getchildren()
        for c in components:
            inst.addComponent(Component.fromXml(c))

        return inst


class DimensionDescriptor(ComponentList):
    _componentType = Dimension
    _urnType = "datastructure"
    _qName = qName("str", "DimensionList")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 components: List[Dimension] = []):
        super(DimensionDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                  components=components)


class AttributeDescriptor(ComponentList):
    _componentType = Attribute
    _urnType = "datastructure"
    _qName = qName("str", "AttributeList")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 components: List[Attribute] = []):
        super(AttributeDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                  components=components)


class MeasureDescriptor(ComponentList):
    _componentType = PrimaryMeasure
    _urnType = "datastructure"
    _qName = qName("str", "MeasureList")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 components: List[PrimaryMeasure] = []):
        super(MeasureDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                components=components)


class GroupDimensionDescriptor(ComponentList):
    _componentType = Dimension
    _urnType = "datastructure"
    _qName = qName("str", "Group")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 components: List[Dimension] = []):
        super(GroupDimensionDescriptor, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                       components=components)


class DataStructureDefinition(MaintainableArtefact):
    _urnType = "datastructure"
    _qName = qName("str", "DataStructure")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 dimensionDescriptor: DimensionDescriptor = None, measureDescriptor: MeasureDescriptor = None,
                 attributeDescriptor: AttributeDescriptor = None,
                 groupDimensionDescriptor: GroupDimensionDescriptor = None):

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

    def toXml(self):
        xml = super().toXml()
        dsdComponents = etree.SubElement(xml,
                                         "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructureComponents")

        dsdComponents.append(self.dimensionDescriptor.toXml())
        dsdComponents.append(self.attributeDescriptor.toXml())
        dsdComponents.append(self.measureDescriptor.toXml())

        xml.append(dsdComponents)
        return xml

    def toVtlJson(self, path):
        dataTypesMapping = {
            "String": "String",
            "ObservationalTimePeriod": "Date",
            "BigInteger": "Integer"
        }

        datasetName = self.id
        components = []
        for c in self.dimensionList.components:
            component = {}

            component["name"] = c.id
            component["role"] = "Identifier"
            component["type"] = dataTypesMapping[c.localRepresentation["dataType"]]
            component["isNull"] = False

            components.append(component)
        for c in self.attributeList.components:
            component = {}

            component["name"] = c.id
            component["role"] = "Attribute"
            component["type"] = dataTypesMapping[c.localRepresentation["dataType"]]
            component["isNull"] = True  # We should use the assignmentStatus
            components.append(component)
        for c in self.measureList.components:
            component = {}

            component["name"] = c.id
            component["role"] = "Measure"
            component["type"] = dataTypesMapping[c.localRepresentation["dataType"]]
            component["isNull"] = True
            components.append(component)

        rslt = {"DataSet": {"name": datasetName, "DataStructure": components}}
        with open(path, 'w') as fp:
            json.dump(rslt, fp)
        return rslt

    def referenceToXml(self):
        """Creates a lxml Element for providing Ref.

        Returns:
            Am lxml Element
        """
        ref = etree.Element("Ref")

        ref.attrib["agencyID"] = self.agencyId
        ref.attrib["id"] = self.id
        ref.attrib["version"] = self.version
        ref.attrib["class"] = "DataStructure"

        return ref

    @classmethod
    def fromXml(cls, elem: etree._Element):
        if not isinstance(elem, etree._Element):
            raise ValueError("The input has to be an lxml etree element")

        # 1. Instantiate class
        dsd = cls()

        # 2. Get and instantiate maintainer
        maintainerId = elem.get("agencyID")
        maintainer = Agency(id_=maintainerId)
        dsd.maintainer = maintainer

        # 3. Get other attributes
        dsd.id = elem.get("id")
        dsd.version = elem.get("version")
        dsd.uri = elem.get("uri")
        dsd.isExternalRefernce = elem.get("isExternalReference")
        dsd.isFinal = elem.get("isFinal")

        # 4. Get Name and description
        name, description = getNameAndDescription(elem)
        dsd.name = name
        dsd.description = description

        # 5. Get components
        dataStructureComponents = elem.find(qName("str", "DataStructureComponents"))

        # 5.1 Get dimensions
        dimensionList = dataStructureComponents.find(qName("str", "DimensionList"))
        dsd.dimensionDescriptor = DimensionDescriptor.fromXml(dimensionList)

        # 5.2 Get measure
        measureList = dataStructureComponents.find(qName("str", "MeasureList"))
        dsd.measureDescriptor = MeasureDescriptor.fromXml(measureList)

        # 5.3 Get attributes
        attributeList = dataStructureComponents.find(qName("str", "AttributeList"))
        if attributeList is not None:
            dsd.attributeDescriptor = AttributeDescriptor.fromXml(attributeList)

        # 5.4 Get group dimensions
        groupDimensionList = dataStructureComponents.find(qName("str", "GroupDimensionList"))
        if groupDimensionList is not None:
            dsd.groupDimensionDescriptor = GroupDimensionDescriptor.fromXml(groupDimensionList)

        return dsd


class DataFlowDefinition(MaintainableArtefact):
    _urnType = "datastructure"
    _qName = qName("str", "Dataflow")

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None,
                 structure: DataStructureDefinition = None):
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

    def toXml(self):
        xml = super().toXml()

        structure = etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Structure")

        attrib = {
            "agencyID": "RBI",
            ##Hardcoded! For solving it, just add the scheme object to the concept (i.e. the concept scheme should be an attribute of concept)
            "class": "DataStructure",
            "id": self.structure.id,
            "package": "datastructure",
            "version": "1.0"
        }

        ref = etree.Element("Ref", attrib=attrib)

        structure.append(ref)
        xml.append(structure)
        return xml

    def referenceToXml(self):
        """Creates a lxml Element for providing Ref.

        Returns:
            Am lxml Element
        """
        ref = etree.Element("Ref")

        ref.attrib["agencyId"] = self.agencyId
        ref.attrib["id"] = self.id
        ref.attrib["version"] = self.version
        ref.attrib["class"] = "DataFlow"

        return ref
