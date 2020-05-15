from lxml import etree
from datetime import datetime, date

from sdmxthon.model.itemScheme import (CodeList, ConceptScheme, OrganisationScheme, AgencyList)
from sdmxthon.model.structure import DataStructureDefinition
from sdmxthon.model.dataSet import DataSet
from sdmxthon import utils
from typing import List, Dict

import warnings


class Header():
    def __init__(self, id_: str = None, test: bool = None, prepared: datetime = None, 
                 senderId:str = None, receiverId:str = None, 
                 reportingBegin: datetime = None, reportingEnd:datetime = None,
                 structures: DataStructureDefinition = []):
        self.id = id_
        self.test = test
        self.prepared = prepared
        self.senderId = senderId 
        self.receiverId = receiverId

        self.reportingBegin=reportingBegin.strftime('%Y-%m-%dT%H:%M:%S') if reportingBegin is not None else None
        self.reportingEnd=reportingEnd.strftime('%Y-%m-%dT%H:%M:%S') if reportingEnd is not None else None
    
        self._structures = []
        for s in structures:
            self.addStructure(s)

    @property
    def id(self):
        return self._id 

    @property
    def test(self):
        return self._test

    @property
    def prepared(self):
        return self._prepared

    @property
    def senderId(self):
        return self._senderId

    @property
    def receiverId(self):
        return self._receiverId

    @property
    def reportingBegin(self):
        return self._reportingBegin

    @property
    def reportingEnd(self):
        return self._reportingEnd
    
    @property
    def structures(self):
        return self._structures

    @id.setter
    def id(self, value):
        self._id = utils.stringSetter(value)

    @test.setter
    def test(self, value):
        self._test = utils.boolSetter(value)

    @prepared.setter 
    def prepared(self, value):
        self._prepared = utils.dateSetter(value)

    @senderId.setter
    def senderId(self, value):
        self._senderId = utils.stringSetter(value)

    @receiverId.setter
    def receiverId(self, value):
        self._receiverId = utils.stringSetter(value)

    @reportingBegin.setter
    def reportingBegin(self, value):
        self._reportingBegin = utils.dateSetter(value)

    @reportingEnd.setter
    def reportingEnd(self, value):
        self._reportingEnd = utils.dateSetter(value)

    #TODO: Add to dimensionAtObservation to the header
    def addStructure(self, value):
        if isinstance(value, DataStructureDefinition):
            self._structures.append(value)
        else:
            raise TypeError(f"DataStructureDefinition object expected, {value.__class__.__name__} passed")

    def setPreparedFromString(self, date: str, format_: str = "%Y-%m-%d"):
        self._prepared = utils.setDateFromString(date, format_)

    def setReportingBeginFromString(self, date: str, format_: str = "%Y-%m-%d"):
        self._reportingBegin = utils.setDateFromString(date, format_)

    def setReportingEndFromString(self, date: str, format_: str = "%Y-%m-%d"):
        self._reportingEnd = utils.setDateFromString(date, format_)

    def getPreparedString(self,  format_: str = "%Y-%m-%d"):
        return utils.getDateString(self.prepared, format_)

    def getReportingBeginString(self,  format_: str = "%Y-%m-%d"):
        return utils.getDateString(self.reportingBegin, format_)

    def getReportingEndString(self,  format_: str = "%Y-%m-%d"):
        return utils.getDateString(self.reportingEnd, format_)


    def __repr__(self):
        return f"<SdmxHeader id={self.id}, test={self.test}, prepared={self.getPreparedString()}, sender={self.senderId}>"

    def toXml(self):
        header= etree.Element(utils.qName("mes", "Header"))
        
        idNode=etree.Element(utils.qName("mes", "ID"))
        idNode.text=self.id
        header.append(idNode)

        testNode=etree.Element(utils.qName("mes", "Test"))
        testNode.text="true" if self.test else "false"
        header.append(testNode)

        preparedNode=etree.Element(utils.qName("mes", "Prepared"))
        preparedNode.text=self.getPreparedString()
        header.append(preparedNode)

        senderNode=etree.Element(utils.qName("mes", "Sender"))
        senderNode.attrib["id"]=self.senderId
        header.append(senderNode)

        receiverNode=etree.Element(utils.qName("mes", "Receiver"))
        receiverNode.attrib["id"]=self.receiverId if self.receiverId is not None else "not_supplied"
        header.append(receiverNode)

        for s in self.structures:
            structureNode = etree.Element(utils.qName("mes", "Structure"))
            structureNode.attrib["structureID"] = s.id
            structureNode.attrib["dimensionAtObservation"] = "AllDimensions" #TODO: Implement other options

            strNode = etree.Element(utils.qName("com", "Structure"))
            
            refNode = etree.Element("Ref", attrib={"agencyID":s.maintainer.id, "id": s.id, "version":s.version})
            
            strNode.append(refNode)
            structureNode.append(strNode)
            
            header.append(structureNode)
            

        if self.reportingBegin is not None:
            repNode=etree.Element(utils.qName("mes", "ReportingBegin"))
            repNode.text=self.getReportingBeginString()
            header.append(repNode)

        if self.reportingEnd is not None:
            repNode=etree.Element(utils.qName("mes", "ReportingEnd"))
            repNode.text=self.getReportingEndString()
            header.append(repNode)

        return header

    @classmethod
    def fromXml(cls, elem):
        if isinstance(elem, etree._Element):
            header=cls()
            
            header.id = elem.find(utils.qName("mes", "ID")).text
            
            header.test = elem.find(utils.qName("mes", "Test")).text
            
            #Different timedate formats used by different providers. All of them have in common the date and time (from char 0 to 19)
            try:
                header.setPreparedFromString(elem.find(utils.qName("mes", "Prepared")).text[:19], "%Y-%m-%dT%H:%M:%S")
            except:
                warnings.warn(f"Not able to parse prepared date. Value received: {elem.find(utils.qName('mes', 'Prepared')).text}")
            
            header.senderId = elem.find(utils.qName("mes", "Sender")).get("id")
            
            receiver = elem.find(utils.qName("mes", "Receiver"))
            if receiver is not None: 
                header.receiverId = receiver.get("id")

            # if messageType=="GenericData":
            #     structure=headerElement.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure")
                
            return header
        else:
            raise ValueError("The input has to be an lxml etree element")

class Message():
    def __init__(self, header=None): 

        self.header = header        

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        if isinstance(value, Header) or value is None:
            self._header=value
        else:
            raise TypeError("The header has to be an instance of the Header class")

    @staticmethod
    def fromXml(fullPath):
        messageTypeMapping = {
            "Structure" : StructureMessage,
            "GenericData" : GenericDataMessage, 
            "StructureSpecificData" : StructureSpecificDataMessage
        }

        tree = etree.parse(fullPath)
        
        #1. Instantiate the right type of message
        messageType = etree.QName(tree.getroot().tag).localname
        message = messageTypeMapping[messageType]()

        #2. Get the header etree element
        headerElement = tree.find(utils.qName("mes", "Header"))
        message.header = Header.fromXml(headerElement)

        #3. Apply the specific parsing method
        message.parseSpecific(tree)

        return message

class StructureMessage(Message):
    def __init__(self, header = None, codeLists: List[CodeList] = [], 
                conceptSchemes: List[ConceptScheme] = [], organisationSchemes: List[OrganisationScheme] = [],
                dsds: List[DataStructureDefinition] = []):
        
        super(StructureMessage, self).__init__(header)
        
        self._codeLists = {}
        self._conceptSchemes = {}
        self._organisationSchemes = {}
        self._dsds = {}

        for c in codeLists:
            self.addCodelist(c)

        for c in conceptSchemes:
            self.addConceptScheme(c)

        for o in organisationSchemes:
            self.addOrganisationScheme(o)

        for d in dsds:
            self.addDsd(d)


        # categoryScheme: Dict[str, CategoryScheme] = categoryScheme
        # constraint: DictLike[str, ContentConstraint] = DictLike()
        # dataflow: DictLike[str, DataflowDefinition] = DictLike()        
        # provisionagreement: DictLike[str, ProvisionAgreement] = DictLike()

    @property
    def codeLists(self):
        return self._codeLists
    
    @property
    def conceptSchemes(self):
        return self._conceptSchemes
    
    @property
    def organisationSchemes(self):
        return self._organisationSchemes

    @property
    def dsds(self):
        return self._dsds

    def addCodeList(self, codeList: CodeList):
        utils.addToMessage(codeList, CodeList, self._codeLists)

    def addConceptScheme(self, conceptScheme: ConceptScheme):
        utils.addToMessage(conceptScheme, ConceptScheme, self._conceptSchemes)

    def addOrganisationScheme(self, organisationScheme: OrganisationScheme):
        utils.addToMessage(organisationScheme, OrganisationScheme, self._organisationSchemes)

    def addDsd(self, dsd: DataStructureDefinition):
        utils.addToMessage(dsd, DataStructureDefinition, self._dsds)

    def parseSpecific(self, tree):

        bodyElement = tree.find(utils.qName("mes", "Structures"))

        #1. Organisation schemes
        organisationSchemes = bodyElement.find(utils.qName("str", "OrganisationSchemes"))
        
        if organisationSchemes is not None: 
            agencySchemes = organisationSchemes.findall(utils.qName("str", "AgencyScheme"))

            for aS in agencySchemes:
                agencyScheme = AgencyList().fromXml(aS)
                self.addOrganisationScheme(agencyScheme)

        #2. Codeslists
        codeLists = bodyElement.find(utils.qName("str", "Codelists"))
        if codeLists is not None: 
            codeLists = codeLists.findall(utils.qName("str", "Codelist"))

            for cL in codeLists:
                codeList = CodeList.fromXml(cL)
                self.addCodeList(codeList)

        #3. ConceptSchmemes
        conceptSchemes = bodyElement.find(utils.qName("str", "Concepts"))
        if conceptSchemes is not None: 
            conceptSchemes = conceptSchemes.findall(utils.qName("str", "ConceptScheme"))

            for cS in conceptSchemes:
                conceptScheme = ConceptScheme.fromXml(cS)
                self.addConceptScheme(conceptScheme)

        #4. DataStructureDefinitions
        dsds = bodyElement.find(utils.qName("str", "DataStructures"))
        if dsds is not None: 
            dsds = dsds.findall(utils.qName("str", "DataStructure"))

            for d in dsds:
                dsd = DataStructureDefinition.fromXml(d)
                self.addDsd(dsd)

    def toXml(self, fullPath:str = None):
        #TODO: Review

        #1. Root element
        nsmap={
            "xsi":"http://www.w3.org/2001/XMLSchema-instance",
            "xml":"http://www.w3.org/XML/1998/namespace",
            "mes":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
            "str":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
            "com":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
        }
        schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd" 

        root = etree.Element(utils.qName("mes", "Structure"), nsmap=nsmap)
        root.attrib["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"]=schemaLocation

        #2. Add header
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

class DataMessage(Message):

    def __init__(self, header=None, 
                  dataSets:List = [], dataFlow = None, observationDimension = None):
        
        super(DataMessage, self).__init__(header)

        self._dataSets = []

        for d in dataSets:
            self.addDataSet(d)
        # self.dataFlow = dataFlow
        # self.observationDimension = observationDimension
    
    @property
    def dataSets(self):
        return self._dataSets

    def addDataSet(self, value):
        if isinstance(value, DataSet):
            self._dataSets.append(value)
        else:
            raise TypeError(f"Dataset object expected, {value.__class__.__name__} passed")

class GenericDataMessage(DataMessage):
    def toXml(self, fullPath:str = None):

        #1. Root element
        nsmap={
            "xsi":"http://www.w3.org/2001/XMLSchema-instance",
            # "xml":"http://www.w3.org/XML/1998/namespace",
            "message":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
            "generic":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
            "common":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
        }
        schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd"      

        root = etree.Element(utils.qName("mes", "GenericData"), nsmap=nsmap)        
        root.attrib["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"] = schemaLocation

        #2. Header
        if self.header is None:
            raise ValueError("The message does not have a header. Header is required for generating XML")
        root.append(self.header.toXml())

 
        #3. Datasets
        for d in self.dataSets:
            root.append(d.toXml())

        if fullPath is not None:
            tree=etree.ElementTree(root)
            tree.write(fullPath, pretty_print=True, xml_declaration=True,   encoding="utf-8")

class StructureSpecificDataMessage(DataMessage):
    pass