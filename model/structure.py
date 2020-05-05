import json
from lxml import etree
from .base import *
from .itemScheme import Concept, CodeList, ConceptScheme

class DataStructureDefinition(MaintainableArtefact):
    # def __init___(self, urn=None, url=None, id=None, name=None, description=None,  annotations=[], version=None, validFrom=None, validTo=None,
    #             final=None, isExternalReference=None, serviceUrl=None, structureUrl=None, isPartial=None, items=[]):
    def __init__(self):

        self._dimensionDescriptor=None
        self._measureDescriptor=None
        self._attributeDescriptor=None
        self._groupDimensionDescriptor=None

        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructure"

        self._name=None
        self._description=None
        
        self.final=None
        self.isExternalReference=None
        self.serviceUrl=None
        self.structureUrl=None

        super().__init__()

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

    @dimensionDescriptor.setter
    def dimensionDescriptor(self,value):
        if value is None:
            pass
        elif type(value)==DimensionDescriptor:
            self._dimensionDescriptor=value
        else:
            raise TypeError("The dimensionDescriptor has to be an instance of the DimensionDescriptor class")
    
    @measureDescriptor.setter
    def measureDescriptor(self,value):
        if value is None:
            pass
        elif type(value)==MeasureDescriptor:
            self._measureDescriptor=value
        else:
            raise TypeError("The measureDescriptor has to be an instance of the MeasureDescriptor class")

    @attributeDescriptor.setter
    def attributeDescriptor(self,value):
        if value is None:
            pass
        elif type(value)==AttributeDescriptor:
            self._attributeDescriptor=value
        else:
            raise TypeError("The attributeDescritpor has to be an instance of the AttributeDescriptor class")

    @groupDimensionDescriptor.setter
    def groupDimensionDescriptor(self,value):
        if value is None:
            pass
        elif type(value)==GroupDimensionDescriptor:
            self._groupDimensionDescriptor=value
        else:
            raise TypeError("The groupDimensionDescriptor has to be an instance of the GroupDimensionDescriptor class")


    def toXml(self):
        xml = super().toXml()
        dsdComponents=etree.SubElement(xml, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructureComponents")

        dsdComponents.append(self.dimensionDescriptor.toXml())
        dsdComponents.append(self.attributeDescriptor.toXml())
        dsdComponents.append(self.measureDescriptor.toXml())

        xml.append(dsdComponents)
        return xml

    def toVtlJson(self, path):
        dataTypesMapping={
            "String":"String",
            "ObservationalTimePeriod":"Date",
            "BigInteger":"Integer"
        }


        datasetName=self.id
        components=[]
        for c in self.dimensionList.components:
            component={}
    
            component["name"]=c.id
            component["role"]="Identifier"
            component["type"]=dataTypesMapping[c.localRepresentation["dataType"]]
            component["isNull"]=False

            components.append(component)
        for c in self.attributeList.components:
            component={}
    
            component["name"]=c.id
            component["role"]="Attribute"
            component["type"]=dataTypesMapping[c.localRepresentation["dataType"]]
            component["isNull"]=True#We should use the assignmentStatus
            components.append(component)
        for c in self.measureList.components:
            component={}
    
            component["name"]=c.id
            component["role"]="Measure"
            component["type"]=dataTypesMapping[c.localRepresentation["dataType"]]
            component["isNull"]=True
            components.append(component)

        rslt = {"DataSet":{"name":datasetName, "DataStructure":components}}
        with open(path, 'w') as fp:
            json.dump(rslt, fp)
        return rslt

    @classmethod 
    def fromXml(cls, structureElement):
        if type(structureElement)!=etree._Element:
            raise ValueError("The input has to be an lxml etree element")
        else:

            #Change this to get the agency!
            self._agencyId=structureElement.get("agencyID")
            
            self._id=structureElement.get("id")
            self._version=structureElement.get("version")
            self._uri=structureElement.get("uri")
            self._urn=structureElement.get("urn")

            self._names={}
            
            for n in structureElement.findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Name"):
                self._names[n.get("{http://www.w3.org/XML/1998/namespace}lang")] =n.text
            #More attributes to be done!

            dataStructureComponents=structureElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructureComponents") 

            self._dimensionList=ComponentList(dataStructureComponents.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DimensionList"))
            self._measureList=ComponentList(dataStructureComponents.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}MeasureList"))
            attributeList=dataStructureComponents.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}AttributeList")
            if attributeList is not None:
                self._attributeList=ComponentList(attributeList)
            
            groupDimensionList=dataStructureComponents.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}GroupDimensionList")
            if groupDimensionList is not None:
                self._groupDimensionList=ComponentList(groupDimensionList)

class ComponentList(IdentifiableArtefact):
    def __init__(self):
        self._components=[]
        super().__init__()
    
    @property
    def components(self):
        return self._components

    def addComponent(self, component):
        if component is None:
            pass
        elif type(component)==self._componentType:
            self._components.append(component)
        else:
            raise TypeError("The component has to be an instance of the class {}".format(self._componentType))

    def toXml(self):
        xml=super().toXml()
        for c in self.components:
            xml.append(c.toXml())

        return xml



        

    # def __init__(self, componentListElement=None):
    #     if componentListElement is None:
    #         self._componentListType=None
    #         self._id=None
    #         self._urn=None
    #         self._components=[]
    #     elif type(componentListElement)==etree._Element:
    #         self._parse(componentListElement)
    #     else:
    #         raise ValueError("The input has to be an lxml etree element")
    # def _parse(self, componentListElement):
    #     self._componentListType=componentListElement.tag.split("}")[1]
    #     self._id=componentListElement.get("id")
    #     self._urn=componentListElement.get("urn")
    #     self._components=[]

    #     objectsMapping={
    #         "DimensionList":Dimension,
    #         "AttributeList":Attribute,
    #         "MeasureList":Measure
    #     }
    #     obj=objectsMapping[self.componentListType]
    #     #What happens with GroupDimensionLists?

    #     for c in  componentListElement.getchildren():
    #         self._components.append(obj(c))

class DimensionDescriptor(ComponentList):
    def __init__(self):
        self._componentType=Dimension
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DimensionList"
        super().__init__()

class AttributeDescriptor(ComponentList):
    def __init__(self):
        self._componentType=Attribute
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}AttributeList"
        super().__init__()

class MeasureDescriptor(ComponentList):
    def __init__(self):
        self._componentType=PrimaryMeasure
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}MeasureList"
        super().__init__()

class GroupDimensionDescriptor(ComponentList):
    def __init__(self):
        self._componentType=Dimension
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Group"
        super().__init__()

class Component(IdentifiableArtefact):
    def __init__(self):
        self._representation=None
        super().__init__()

    @property
    def representation(self):
        return self._representation
    @representation.setter 
    def representation(self, value):
        if value is None:
            pass
        elif type(value)==Representation:
            self._representation=value
        else:
            raise TypeError("The representation has to be an instance of the representation class")

    def toXml(self):
        xml=super().toXml()
        if self.__class__==Dimension:
            xml.attrib["position"]=str(self.position)
        if self.__class__==Attribute:
            xml.attrib["assignmentStatus"]="Conditional" #Hard coded


        
        if self.representation.concept is not None:
            concept=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptIdentity")
            attrib={
                "agencyID":"RBI", ##Hardcoded! For solving it, just add the scheme object to the concept (i.e. the concept scheme should be an attribute of concept)
                "class":"Concept",
                "id":self.representation.concept.id,
                "maintainableParentID":"RBI_CONCEPTS",##Hardcoded
                "maintainableParentVersion":"1.0",
                "package":"conceptscheme"
            }
            
            ref=etree.Element("Ref", attrib=attrib)

            concept.append(ref)
            xml.append(concept)

        localRep=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}LocalRepresentation")
        if self.representation.codeList is not None:
            enum=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration")
            
            attrib={
                "agencyID":"RBI", ##Hardcoded! For solving it, just add the scheme object to the concept (i.e. the concept scheme should be an attribute of concept)
                "class":"Codelist",
                "id":self.representation.codeList.id,
                "package":"codelist",
                "version":"1.0"
            }
            
            ref=etree.Element("Ref", attrib=attrib)

            enum.append(ref)
            localRep.append(enum)
        elif self.id=="TIME_PERIOD":
            localRep.append(etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat", attrib={"textType":"GregorianDay"})) #Harcoded! What's the link with facets?
        else:
            localRep.append(etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat", attrib={"textType":"String"})) #Harcoded! What's the link with facets?

        xml.append(localRep)


        if self.__class__==Attribute: #Hard coded
            attachment=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}AttributeRelationship")
            pm=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}PrimaryMeasure")
            pm.append(etree.Element("Ref", attrib={"id":"OBS_VALUE"}))
            attachment.append(pm)
            xml.append(attachment)


        return xml

class Representation():
    def __init__(self):
        self._concept=None
        self._facets=[]
        self._codeList=None
        self._conceptScheme=None


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
        if value is None:
            pass
        elif type(value)==Concept:
            self._concept=value
        else:
            raise TypeError("The concept has to be an instance of the Concept class")        

    @codeList.setter
    def codeList(self, value):
        if value is None:
            pass
        elif type(value)==CodeList:
            self._codeList=value
        else:
            raise TypeError("The codelist has to be an instance of the CodeList class")     

    @conceptScheme.setter
    def conceptScheme(self, value):
        if value is None:
            pass
        elif type(value)==ConceptScheme:
            self._conceptScheme=value
        else:
            raise TypeError("The conceptScheme has to be an instance of the ConceptScheme class")

    def addFacet(self, value):
        if value is None:
            pass
        elif type(value)==Facet:
            self._facets.append(value)
        else:
            raise TypeError("Facets have to be an instance of the Facet class")      

    # @property
    # def conceptIdentity(self):
    #     return self._conceptIdentity
    # @property
    # def localRepresentation(self):
    #     return self._localRepresentation

    # def __init__(self, componentElement=None):
    #     if componentElement is None:
    #         self._id=None
    #         self._urn=None
    #     elif type(componentElement)==etree._Element:
    #         self._parse(componentElement)
    #     else:
    #         raise ValueError("The input has to be an lxml etree element")
    # def _parse(self, componentElement):
    #     pass
    
    # def __repr__(self):
    #     return "<{} - id={}>".format(self.__class__.__name__, self.id)

    # def _setConceptIdentity(self, componentElement):
    #     conceptIdentity=componentElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptIdentity").getchildren()[0]
    #     self._conceptIdentity=conceptIdentity.attrib
    
    # def _setLocalRepresentation(self, componentElement):
    #     self._localRepresentation={}
    #     localRepresentation=componentElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}LocalRepresentation")
        
    #     enumeration =localRepresentation.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration")
    #     if enumeration is not None:
    #         self._localRepresentation["type"]="enumerated"
    #         self._localRepresentation["values"]=enumeration.getchildren()[0].attrib
    #         self._localRepresentation["dataType"]=localRepresentation.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}EnumerationFormat").get("textType")
    #     else:
    #         self._localRepresentation["type"]="non-enumerated"
    #         self._localRepresentation["dataType"]=localRepresentation.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat").get("textType")


    # @property
    # def id(self):
    #     return self._id
    # @property
    # def urn(self):
    #     return self._urn 

class Facet():
    def __init__(self):
        self.facetType=None
        self.facetValue=None
        self.facetValueType=None

class Dimension(Component):
    def __init__(self):
        self.position=None
        self._dimensionType=None
        self._urnType="datastructure"
        # self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dimension"



        super().__init__()

    
    @property
    def _qName(self):
        if self.dimensionType=="TimeDimension":
            return "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TimeDimension"
        else:
            return "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dimension"

    
    @property
    def dimensionType(self):
        return self._dimensionType

    @dimensionType.setter 
    def dimensionType(self, value):
        if value is None: 
            pass
        elif value in ["Dimension", "MeasureDimension", "TimeDimension"]:
            self._dimensionType=value
        else:
            raise ValueError("The value for dimension type has to be Dimension, MeasureDimension or TimeDimension")


    # def _parse(self, componentElement):
    #     self._id=componentElement.get("id")
    #     self._urn=componentElement.get("urn")
    #     self._position=int(componentElement.get("position"))
    #     self._dimensionType=componentElement.tag.split("}")[1]

    #     self._setConceptIdentity(componentElement)
    #     self._setLocalRepresentation(componentElement)

class Attribute(Component):
    def __init__(self):
        self.usageStatus=None
        self.relatedTo=None
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Attribute"
        super().__init__()

    # def _parse(self, componentElement):
    #     self._id=componentElement.get("id")
    #     self._urn=componentElement.get("urn")
    #     self._assignmentStatus=componentElement.get("assignmentStatus")

    #     self._setConceptIdentity(componentElement)
    #     self._setLocalRepresentation(componentElement)
    
    @property
    def usageStatus(self):
        return self._usageStatus
    @usageStatus.setter 
    def usageStatus(self,value):
        if value is None: 
            pass
        elif value in ["mandatory", "conditional"]:
            self._usageStatus=value
        else:
            raise ValueError("The value for usageStatushas to be mandatory or conditional")

    @property
    def relatedTo(self):
        return self._relatedTo
    @relatedTo.setter 
    def relatedTo(self,value):
        if value is None: 
            self._relatedTo="NoSpecifiedRelationship"
        elif value == "PrimaryMeasureRelationship" :
            self._relatedTo=value
        elif type(value)==GroupDimensionDescriptor:
            self._relatedTo=value 
        elif type(value)==Dimension:
            self._relatedTo=value
        else:
            raise ValueError("The value for related To has to be None, 'PrimaryMeasureRelationship' an object of the GroupDimensionDescriptor class or an object of the DimensionClass")       

class PrimaryMeasure(Component):
    def __init__(self):
        self.usageStatus=None
        self.relatedTo=None
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}PrimaryMeasure"
        super().__init__()
    # def _parse(self, componentElement):
    #     self._id=componentElement.get("id")
    #     self._urn=componentElement.get("urn")

    #     self._setConceptIdentity(componentElement)
    #     self._setLocalRepresentation(componentElement)

class DataFlowDefinition(MaintainableArtefact):
    def __init__(self):
        self.structure=None
        self._urnType="datastructure"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflow"

        self._name=None
        self._description=None
        
        self.final=None
        self.isExternalReference=None
        self.serviceUrl=None
        self.structureUrl=None

        super().__init__()

    @property
    def structure(self):
        return self._structure
    @structure.setter 
    def structure(self, value):
        if value is None:
            pass
        elif type(value)==DataStructureDefinition:
            self._structure=value 
        else:
            raise TypeError("the structure has to be an instance of the DataStructureDefinition class")

    def toXml(self):
        xml=super().toXml()

        structure=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Structure")
        
        attrib={
            "agencyID":"RBI", ##Hardcoded! For solving it, just add the scheme object to the concept (i.e. the concept scheme should be an attribute of concept)
            "class":"DataStructure",
            "id":self.structure.id,
            "package":"datastructure",
            "version":"1.0"
        }
        
        ref=etree.Element("Ref", attrib=attrib)

        structure.append(ref)
        xml.append(structure)
        return xml 
