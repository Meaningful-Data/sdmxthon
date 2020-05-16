from lxml import etree
from datetime import datetime, date

from sdmxthon.model.itemScheme import (CodeList, ConceptScheme, OrganisationScheme, AgencyList)
from sdmxthon.model.structure import DataStructureDefinition, DataFlowDefinition
from sdmxthon.model.dataSet import DataSet
from sdmxthon.model.base import InternationalString
from sdmxthon.model import dataTypes
from sdmxthon import utils
from typing import List, Dict

import warnings

class PayloadStructureType(object):
    """Implementes the PayloadStructureType Complex Type from SDMX schemas

    Attributes:
        structureId: The structureID attribute uniquely identifies the structure for the 
                purpose of referencing it from the payload. This is only used in structure 
                specific formats. Although it is required, it is only useful when more 
                than one data set is present in the message
        schemaURL: provides a location from which the structure specific schema can be located.
        namespace: provides the namespace for structure-specific formats. By communicating 
                    this information in the header, it is possible to generate the structure 
                    specific schema while processing the message.
        dimensionAtObservation: used to reference the dimension at the observation level for data messages
            Values: 'AllDimensions', 'TIME_PERIOD' or any dimension of the dsd
        explicitMeasures: indicates whether explicit measures are used in the cross sectional format. 
                            This is only applicable for the measure dimension as the dimension at the 
                            observation level or the flat structure
        externalReferenceAttributeGroup: TODO
        provisionAgreement: TODO
        structureUsage: references a flow which the data or metadata is reported against
        structure: references the structure which defines the structure of the data or metadata set
    """    
    def __init__(self, structureId:str = None, schemaURL:str = None, namespace:str = None,
                     dimensionAtObservation:str = "AllDimensions", explicitMeasures:str = None,
                     externalReferenceAttributeGroup = None, provisionAgreement = None,
                     structureUsage:DataFlowDefinition = None, structure:DataStructureDefinition = None):
        
        @property
        def structureId(self):
            return self._structureId

        @property
        def schemaURL(self):
            return self._schemaURL

        @property
        def namespace(self):
            return self._namespace

        @property
        def dimensionAtObservation(self):
            return self._dimensionAtObservation

        @property
        def explicitMeasures(self):
            return self._explicitMeasures

        @property
        def externalReferenceAttributeGroup(self):
            return self._externalReferenceAttributeGroup

        @property
        def provisionAgreement(self):
            return self._provisionAgreement

        @property
        def structureUsage(self):
            return self._structureUsage

        @property
        def structure(self):
            return self._structure

        @structureId.setter
        def structureId(self, value):
            structureId = utils.stringSetter(value)

        @schemaURL.setter
        def schemaURL(self, value):
            self._schemaURL = utils.stringSetter(value)

        @namespace.setter
        def namespace(self, value):
            self._namespace = utils.stringSetter(value)

        @dimensionAtObservation.setter
        def dimensionAtObservation(self, value):
            self._dimensionAtObservation = utils.stringSetter(value, "[A-Za-z0-9_@$\-]+")

        @explicitMeasures.setter
        def explicitMeasures(self, value):
            self._explicitMeasures = utils.boolSetter(value)

        @externalReferenceAttributeGroup.setter
        def externalReferenceAttributeGroup(self, value):
            self._externalReferenceAttributeGroup = value

        @provisionAgreement.setter
        def provisionAgreement(self, value):
            self._provisionAgreement = value

        @structureUsage.setter
        def structureUsage(self, value):
            self._structureUsage = utils.genericSetter(value, DataFlowDefinition)

        @structure.setter
        def structure(self, value):
            self._structure - utils.genericSetter(value, DataStructureDefinition)


        def isValid(self):
            if self.structureId is None:
                return "Error: structureId required"
            elif self.dimensionAtObservation is None:
                return "Error: dimensionAtObservation required"
            elif provisionAgreement is None and structureUsage is None and structure is None:
                return "Error: one between provisionAgreement, structureUsage and structure cannot be None"
            elif provisionAgreement is not None and structureUsage is not None:
                return "Error: only one between provisionAgreement, structureUsage and structure can be not None"
            elif provisionAgreement is not None and structure is not None:
                return "Error: only one between provisionAgreement, structureUsage and structure can be not None"
            elif structure is not None and structureUsage is not None:
                return "Error: only one between provisionAgreement, structureUsage and structure can be not None"
            else:
                return True

        def toXml(self):
            if not self.isValid():
                raise ValueError(f"Could not generate XML. {self.isValid()}")
            else:
                structure= etree.Element(utils.qName("mes", "Structure"))
                
                structure.attrib["structureID"] = self.structureId
                structure.attrib["dimensionAtObservation"] = self.dimensionAtObservation
                
                if self.schemaURL is not None:
                    structure.attrib["schemaURL"] = self.schemaURL
                
                if self.namespace is not None:
                    structure.attrib["namespace"] = self.namespace
                
                if self.explicitMeasures is not None:
                    structure.attrib["explicitMeasures"] = self.explicitMeasures
                
                if self.externalReferenceAttributeGroup is not None:
                    pass #TODO
                
                if self.provisionAgreement is not None:
                    pass #TODO
                
                if self.structureUsage is not None:
                    strNode = etree.Element(utils.qName("com", "StructureUsage"))
                    refNode = self.structureUsage.referenceToXml()
                    refNode.attrib["urn"] = self.urn
                    strNode.append(refNode)

                if self.structure is not None:                
                    strNode = etree.Element(utils.qName("com", "Structure"))
                    refNode = self.structure.referenceToXml()
                    refNode.attrib["urn"] = self.urn
                    strNode.append(refNode)

                structure.append(strNode)

                return structure

class BaseHeader(object):
    """Implementes the BaseHeaderType Complex Type from SDMX schemas

    Attributes:
        id: identifies an identification for the message, assigned by the sender.
        test: indicates whether the message is for test purposes or not.
        prepared: date the message was prepared
        senderId: information about the party that is transmitting the message. TODO: Add all possible information
        receiverId: information about the party that is the intended recipient of the message. TODO: Allow multiple receivers, add all information
        name: name for the transmission
        structures: provides a reference to the structure (either explicitly or through a 
            structure usage reference) that describes the format of data or reference metadata. 
            In addition to the structure, it is required to also supply the namespace of the 
            structure specific schema that defines the format of the data/metadata. 
            For cross sectional data, additional information is also required to state 
            which dimension is being used at the observation level. This information will allow 
            the structure specific schema to be generated. For generic format messages, 
            this is used to simply reference the underlying structure. 
            It is not mandatory in these cases and the generic data/metadata sets
             will require this reference explicitly.
        provider: TODO
        datasetAction: provides a code for determining whether the enclosed message 
            is an Update or Delete message 
        datasetIds: provides an identifier for a contained data set
        extracted: time-stamp from the system rendering the data
        reportingBegin: provides the start of the time period covered by the message (in the case of data)
        reportingEnd: provides the end of the time period covered by the message (in the case of data)
        embargoDate: time period before which the data included in this message is not available
        source: human-readable information about the source of the data

    TODO: create classes for PartyType, SenderType, DataProviderReferenceType. 
            For the time being only Id is allowed and they are of the str type
    """


    def __init__(self, id_: str = None, test: bool = False, prepared: datetime = None, 
                 senderId:str = None, receiverId:str = None, 
                 name:InternationalString = None, structures:List[PayloadStructureType] = [],
                 provider = None, datasetAction:str = None,
                 datasetIds: List[str] = [], extracted: datetime = None,
                 reportingBegin:datetime = None, reportingEnd:datetime = None,
                 embargoDate:datetime = None, source:InternationalString = None):
        
        self.id = id_
        self.test = test
        self.prepared = prepared
        self.senderId = senderId 
        self.receiverId = receiverId
        self.name = name
        self.provider = provider
        self.datasetAction = datasetAction
        self.extracted = extracted
        self.reportingBegin = reportingBegin
        self.reportingEnd = reportingEnd
        self.embargoDate = embargoDate
        self.source = source

        self._structures = []
        self._datasetIds = []
        
        for s in structures:
            self.addStructure(s)
        for d in datasetIds:
            self.addDatasetId(d)

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
    def name(self):
        return self._name

    @property
    def provider(self):
        return self._provider

    @property
    def datasetAction(self):
        return self._datasetAction

    @property
    def datasetIds(self):
        return self._datasetIds

    @property
    def extracted(self):
        return self._extracted

    @property
    def embargoDate(self):
        return self._embargoDate

    @property
    def source(self):
        return self._source

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

    @name.setter
    def name(self, value):
        self._name = utils.genericSetter(value, InternationalString)

    @provider.setter
    def provider(self, value):
        self._provider = value

    @datasetAction.setter
    def datasetAction(self, value):
        self._datasetAction = utils.stringSetter(value, enumeration = dataTypes.ActionType)

    @extracted.setter
    def extracted(self, value):
        self._extracted = utils.dateSetter(value)

    @reportingBegin.setter
    def reportingBegin(self, value):
        self._reportingBegin = utils.dateSetter(value)

    @reportingEnd.setter
    def reportingEnd(self, value):
        self._reportingEnd = utils.dateSetter(value)

    @embargoDate.setter
    def embargoDate(self, value):
        self._embargoDate = utils.dateSetter(value)

    @source.setter
    def source(self, value):
        self._source = utils.stringSetter(value)

    def addStructure(self, value):
        self._structures.append(utils.genericSetter(value, DataStructureDefinition))

    def addDatasetId(self, value):
        self._datasetIds.append(utils.stringSetter(value))

    # def setPreparedFromString(self, date: str, format_: str = "%Y-%m-%d"):
    #     self._prepared = utils.setDateFromString(date, format_)

    # def setReportingBeginFromString(self, date: str, format_: str = "%Y-%m-%d"):
    #     self._reportingBegin = utils.setDateFromString(date, format_)

    # def setReportingEndFromString(self, date: str, format_: str = "%Y-%m-%d"):
    #     self._reportingEnd = utils.setDateFromString(date, format_)

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
        
        node = etree.Element(utils.qName("mes", "ID"))
        node.text=self.id
        header.append(node)

        node = etree.Element(utils.qName("mes", "Test"))
        node.text = "true" if self.test else "false"
        header.append(node)

        node = etree.Element(utils.qName("mes", "Prepared"))
        node.text = self.getPreparedString()
        header.append(node)

        node = etree.Element(utils.qName("mes", "Sender"))
        node.attrib["id"] = self.senderId
        header.append(node)

        node = etree.Element(utils.qName("mes", "Receiver"))
        node.attrib["id"] = self.receiverId if self.receiverId is not None else "not_supplied"
        header.append(node)

        for n in self.name.localisedStrings:
            header.append(n.toXml(tag = utils.qName("com", "Name")))

        for s in self.structures:
            header.append(s.toXml())

        if self.datasetAction is not None:
            node = etree.Element(utils.qName("mes", "DataSetAction"))
            node.text = self.datasetAction
            header.append(node)

        for d in datasetIds:
            node = etree.Element(utils.qName("mes", "DataSetID"))
            node.text = self.d
            header.append(node)

        if self.extracted is not None:
            node = etree.Element(utils.qName("mes", "Extracted"))
            node.text = utils.getDateString(self.extracted, "%Y-%m-%dT%H:%M:%S")
            header.append(node)

        if self.reportingBegin is not None:
            node = etree.Element(utils.qName("mes", "ReportingBegin"))
            node.text = utils.getDateString(self.reportingBegin, "%Y-%m-%dT%H:%M:%S")
            header.append(node)

        if self.reportingEnd is not None:
            node = etree.Element(utils.qName("mes", "ReportingEnd"))
            node.text = utils.getDateString(self.reportingEnd, "%Y-%m-%dT%H:%M:%S")
            header.append(node)
        
        if self.embargoDate is not None:
            node = etree.Element(utils.qName("mes", "EmbargoDate"))
            node.text = utils.getDateString(self.embargoDate, "%Y-%m-%dT%H:%M:%S")
            header.append(node)

        for s in self.sources.localisedStrings:
            header.append(s.toXml(tag = utils.qName("mes", "Source")))

        return header

    @classmethod
    def fromXml(cls, elem):
        #TODO
        if isinstance(elem, etree._Element):
            header = cls()
            
            header.id = elem.find(utils.qName("mes", "ID")).text
            
            header.test = elem.find(utils.qName("mes", "Test")).text
            
            #Different timedate formats used by different providers. All of them have in common the date and time (from char 0 to 19)
            try:
                header.prepared = elem.find(utils.qName("mes", "Prepared")).text[:19]
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

class Message(object):
    def __init__(self, header = None): 

        self.header = header        

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = utils.genericSetter(value, BaseHeader)

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
        message.header = BaseHeader.fromXml(headerElement)

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