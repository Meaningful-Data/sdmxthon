from lxml import etree
import os
from urllib.parse import urlparse, urljoin
from datetime import datetime

from .structure import DataStructureDefinition
from .dataSet import DataSet

class Message():
    def __init__(self, messageType=None, header=None, payload=None): 
        if messageType is not None: 
            self.messageType=messageType
        if header is not None:
            self.header=header
        self._payload={}
        if payload is not None:
            for i in payload:
                self.addPayloadElement(i, payload[i])

    @property
    def messageType(self):
        return self._messageType
    @property
    def header(self):
        return self._header
    @property
    def payload(self):
        return self._payload


    @messageType.setter
    def messageType(self,value):
        if value in ["Structure", "GenericData", "StructureSpecificData"]:
            self._messageType=value
        else:
            raise ValueError("message type not valid or not implemented")
    @header.setter
    def header(self, value):
        if type(value)==Header:
            self._header=value
        else:
            raise TypeError("The header has to be an instance of the Header class")
    
    def addPayloadElement(self, key, elements):
        #Validations to be added!
        if key not in self.payload:
            self._payload[key]={}   
        
        for e in elements:
            self._payload[key][e.id]=e

    def toXml(self, fullPath=None):
        #Root element
        if self.messageType=="Structure":
            nsmap={
                "xsi":"http://www.w3.org/2001/XMLSchema-instance",
                "xml":"http://www.w3.org/XML/1998/namespace",
                "mes":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
                "str":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
                "com":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
            }
            schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd"      

        elif self.messageType=="GenericData":
            nsmap={
                "xsi":"http://www.w3.org/2001/XMLSchema-instance",
                # "xml":"http://www.w3.org/XML/1998/namespace",
                "message":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
                "generic":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
                "common":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
            }
            schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd"      

        # elif self.messageType=="StructureSpecificData":
        #     nsmap={
        #         "xsi":"http://www.w3.org/2001/XMLSchema-instance",
        #         # "xml":"http://www.w3.org/XML/1998/namespace",
        #         "message":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
        #         "data":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific",
        #         "common":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
                
        #     }
        #     schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd"            

        root = etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}" + self.messageType, nsmap=nsmap)
        
        root.attrib["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"]=schemaLocation

        #Header
        root.append(self.header.toXml())

        #Payload for Structure messages
        if self.messageType=="Structure":

            structures=etree.SubElement(root, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structures")   
            
            if "AgencyScheme" in self.payload:
                organisationSchemes=etree.SubElement(root, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}OrganisationSchemes")
                for i in self.payload["AgencyScheme"]:
                    organisationSchemes.append(self.payload["AgencyScheme"][i].toXml())
                structures.append(organisationSchemes)

            if "ConceptScheme" in self.payload:
                conceptSchemes=etree.SubElement(root, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Concepts")
                for i in self.payload["ConceptScheme"]:
                    conceptSchemes.append(self.payload["ConceptScheme"][i].toXml())
                structures.append(conceptSchemes)

            if "CodeList" in self.payload:
                codelists=etree.SubElement(root, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Codelists")
                for i in self.payload["CodeList"]:
                    codelists.append(self.payload["CodeList"][i].toXml())
                structures.append(codelists)

            if "DataFlow" in self.payload:
                dataFlows=etree.SubElement(root, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflows")
                for i in self.payload["DataFlow"]:
                    dataFlows.append(self.payload["DataFlow"][i].toXml())
                structures.append(dataFlows)

            if "DataStructure" in self.payload:
                dsds=etree.SubElement(root, "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructures")
                for i in self.payload["DataStructure"]:
                    dsds.append(self.payload["DataStructure"][i].toXml())
                structures.append(dsds)

        elif self.messageType=="GenericData":
            #Payload for dataset message
            if "DataSet" in self.payload:
                for d in self.payload["DataSet"]:
                    root.append(self.payload["DataSet"][d].toXml())
                

        if fullPath is not None:
            tree=etree.ElementTree(root)
            tree.write(fullPath, pretty_print=True, xml_declaration=True,   encoding="utf-8")


        return root

    @classmethod
    def fromXml(cls, fullPath):
        message=cls()

        tree = etree.parse(fullPath)
        
        #First get the type of file
        messageType=tree.getroot().tag.split("}")[1]
        message.messageType=messageType

        #Now we get the header etree element
        headerElement=tree.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Header")
        #To be done, parse the header

        #Now, depending of the type of message
        if messageType=="Structure":
            header=Header(headerElement,"Structure")
            message.header=header
            
            bodyElement=tree.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structures")
            
            #self._body["dataStructures"]={}
            dataStructures=bodyElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructures").findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructure")
            for d in dataStructures:
                dataStructure=DataStructureDefinition.fromXml(d)

                #self._body["dataStructures"][dataStructure.id]=dataStructure

        elif self.messageType=="GenericData":
            self._header=Header(headerElement,"GenericData")

            bodyElement=tree.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet")
            self._body["dataSet"]=DataSet(bodyElement, self.header.structure["dimensionAtObservation"])


class Header():
    def __init__(self, id=None, test=None,senderId=None, receiverId=None, structure=None, reportingBegin=None, reportingEnd=None):
        self.id=id
        self.test=test
        self.prepared=datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.senderId=senderId 
        self.receiverId=receiverId

        self.structure=structure
        self.reportingBegin=reportingBegin.strftime('%Y-%m-%dT%H:%M:%S') if reportingBegin is not None else None
        self.reportingEnd=reportingEnd.strftime('%Y-%m-%dT%H:%M:%S') if reportingEnd is not None else None
    
    def __repr__(self):
        return "<SdmxHeader id={}, test={}, prepared={}, sender={}>".format(self.id, self.test, self.prepared, self.sender["id"])

    def toXml(self):
        header= etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Header")
        
        idNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}ID")
        idNode.text=self.id
        header.append(idNode)

        testNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Test")
        testNode.text="false" if self.id != True else "true"
        header.append(testNode)

        preparedNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Prepared")
        preparedNode.text=self.prepared
        header.append(preparedNode)

        senderNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Sender")
        senderNode.attrib["id"]=self.senderId
        header.append(senderNode)

        receiverNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Receiver")
        receiverNode.attrib["id"]=self.receiverId if self.receiverId is not None else "not_supplied"
        header.append(receiverNode)

        if self.structure is not None:
            structureNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure")
            structureNode.attrib["structureID"]=self.structure["id"]
            if "dimensionAtObservation" in self.structure:
                structureNode.attrib["dimensionAtObservation"]=self.structure["dimensionAtObservation"]
            
            strNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Structure")
            refNode=etree.Element("Ref", attrib={"agencyID":"RBI", "id": self.structure["id"], "version":"1.0"})
            strNode.append(refNode)
            
            structureNode.append(strNode)
            
            header.append(structureNode)

        if self.reportingBegin is not None:
            repNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}ReportingBegin")
            repNode.text=self.reportingBegin
            header.append(repNode)

        if self.reportingEnd is not None:
            repNode=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}ReportingEnd")
            repNode.text=self.reportingEnd
            header.append(repNode)

        return header

    @classmethod
    def fromXml(cls, headerElement=None, messageType=None):
        if headerElement is None:
            pass
        elif type(headerElement)==etree._Element:
            header=cls()
            header.id=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}ID").text
            header.test=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Test").text
            header.prepared=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Prepared").text
            header.senderId=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Sender").get("id")
            receiver=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Receiver")
            if receiver is not None: 
                header.receiverId=receiver

            if messageType=="GenericData":
                structure=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure")
                
                #To do: structure
                #header.structure=structure.attrib
                #self._structure["urn"]=structure.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Structure").find("URN").text


        else:
            raise ValueError("The input has to be an lxml etree element")


