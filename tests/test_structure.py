#TODO: Setters and attributes checking

import unittest
from datetime import datetime
from sdmxthon.model import message, base
from pathlib import Path

STRUCTURE_MESSAGES = Path().absolute() / "tests" /"resources_structureMessage"
DATA_MESSAGES = Path().absolute() / "tests" /"resources_dataMessage"


class RBI_ALE(unittest.TestCase):
    def setUp(self):
        self.mes = message.Message().fromXml(str(STRUCTURE_MESSAGES / "RBI_ALE.xml"))
        
    def test_header(self):
        self.assertEqual(self.mes.header.id, "IDREFdea3c385-f916-47c0-9069-fadf911dcd0e", "Wrong message ID")
        self.assertEqual(self.mes.header.test, False, "Wrong test attibute")
        self.assertEqual(self.mes.header.prepared, datetime(2020, 5, 11, 15, 20, 22), "Wrong prepared attibute")
        self.assertEqual(self.mes.header.senderId, "Unknown", "Wrong senderId attibute")
        self.assertEqual(self.mes.header.receiverId, "not_supplied", "Wrong receiverId attibute")

    def test_codelists(self):
        urn = "urn:sdmx:org.sdmx.infomodel.codelist.Codelist=RBI:CL_ADD_DET(1.0)" 
        
        self.assertEqual(len(self.mes.codeLists), 305)

        #Testing attributes
        self.assertEqual(self.mes.codeLists[urn].maintainer.id, "RBI")
        self.assertEqual(self.mes.codeLists[urn].urn, urn, "The urn is not correctly generated")
        self.assertEqual(self.mes.codeLists[urn].isExternalReference, False)
        
        #Testing name        
        self.assertEqual(len(self.mes.codeLists[urn].name.localisedStrings), 1)

        self.assertEqual(self.mes.codeLists[urn].name.getLocales(), {"en"})
        self.assertEqual(self.mes.codeLists[urn].name["en"], "Additional Details")


        #Testing items
        self.assertEqual(len(self.mes.codeLists[urn].items), 5)

        urnCode  = "urn:sdmx:org.sdmx.infomodel.codelist.Code=RBI:CL_ADD_DET(1.0).AGGGL"
        self.assertEqual(self.mes.codeLists[urn].items["AGGGL"].id, "AGGGL")
        self.assertEqual(self.mes.codeLists[urn].items["AGGGL"].name["en"], "Aggregate Gap Limit (in US Dollar mio)")
        self.assertEqual(self.mes.codeLists[urn].items["AGGGL"].urn, urnCode)

    def test_conceptSchemes(self):
        urn = "urn:sdmx:org.sdmx.infomodel.conceptscheme.ConceptScheme=RBI:RBI_SCM(1.0)" 
        
        self.assertEqual(len(self.mes.conceptSchemes), 1)

        #Testing attributes
        self.assertEqual(self.mes.conceptSchemes[urn].maintainer.id, "RBI")
        self.assertEqual(self.mes.conceptSchemes[urn].urn, urn, "The urn is not correctly generated")
        self.assertEqual(self.mes.conceptSchemes[urn].isExternalReference, False)
        
        #Testing name        
        self.assertEqual(len(self.mes.conceptSchemes[urn].name.localisedStrings), 1)

        self.assertEqual(self.mes.conceptSchemes[urn].name.getLocales(), {"en"})
        self.assertEqual(self.mes.conceptSchemes[urn].name["en"], "RBI Scheme")


        #Testing items
        self.assertEqual(len(self.mes.conceptSchemes[urn].items), 467)

        urnConcept  = "urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=RBI:RBI_SCM(1.0).Acc_Type"
        self.assertEqual(self.mes.conceptSchemes[urn].items["Acc_Type"].id, "Acc_Type")
        self.assertEqual(self.mes.conceptSchemes[urn].items["Acc_Type"].name["en"], "Account Type")
        self.assertEqual(self.mes.conceptSchemes[urn].items["Acc_Type"].urn, urnConcept)

        self.assertEqual(self.mes.conceptSchemes[urn].items["Acc_Type"].coreRepresentation._codeListReference["id_"], "CL_Acc_Type")
        self.assertEqual(self.mes.conceptSchemes[urn].items["Acc_Type"].coreRepresentation._codeListReference["version"], "1.0")
        self.assertEqual(self.mes.conceptSchemes[urn].items["Acc_Type"].coreRepresentation._codeListReference["agencyId"], "RBI")

    def test_dsds(self):
        urn = "urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=RBI:AALOE(1.0)" 

        self.assertEqual(len(self.mes.dsds), 433)

        #Testing attributes
        self.assertEqual(self.mes.dsds[urn].maintainer.id, "RBI")
        self.assertEqual(self.mes.dsds[urn].urn, urn, "The urn is not correctly generated")
        self.assertEqual(self.mes.dsds[urn].isExternalReference, False)
        self.assertEqual(self.mes.dsds[urn].isFinal, False)
        self.assertEqual(self.mes.dsds[urn].version, "1.0")
        
        #Testing name        
        self.assertEqual(len(self.mes.dsds[urn].name.localisedStrings), 1)

        self.assertEqual(self.mes.dsds[urn].name.getLocales(), {"en"})
        self.assertEqual(self.mes.dsds[urn].name["en"], "Ageing analysis of long outstanding entries")


        #Testing descriptors
        self.assertEqual(len(self.mes.dsds[urn].dimensionDescriptor), 6)
        self.assertEqual(len(self.mes.dsds[urn].attributeDescriptor), 5)
        self.assertEqual(len(self.mes.dsds[urn].measureDescriptor), 1)

        #Testing dimension descriptor
        urnDd = "urn:sdmx:org.sdmx.infomodel.datastructure.DimensionDescriptor=RBI:AALOE(1.0).DimensionDescriptor"
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor.urn, urnDd)
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor.id, "DimensionDescriptor")
            #Testign dimensions
        urnDimension = "urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=RBI:AALOE(1.0).RECO_PER"
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"].urn, urnDimension)
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"].id, "RECO_PER")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"].position, 1)
            #Concept identity
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"]._conceptIdentityRef["id_"], "RECO_PER")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"]._conceptIdentityRef["agencyId"], "RBI")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"]._conceptIdentityRef["maintainableParentId"], "RBI_SCM")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"]._conceptIdentityRef["package"], "conceptscheme")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"]._conceptIdentityRef["maintainableParentVersion"], "1.0")
            #Local representation
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"].localRepresentation._codeListReference["id_"], "CL_RECO_PER")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"].localRepresentation._codeListReference["version"], "1.0")
        self.assertEqual(self.mes.dsds[urn].dimensionDescriptor["RECO_PER"].localRepresentation._codeListReference["agencyId"], "RBI")

        #Testing attribute descriptor
        urnDd = "urn:sdmx:org.sdmx.infomodel.datastructure.AttributeDescriptor=RBI:AALOE(1.0).AttributeDescriptor"
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor.urn, urnDd)
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor.id, "AttributeDescriptor")
            #Testign attributes
        urnAttribute = "urn:sdmx:org.sdmx.infomodel.datastructure.DataAttribute=RBI:AALOE(1.0).COMMENT"
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"].urn, urnAttribute)
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"].id, "COMMENT")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"].usageStatus, "Conditional")
            #Concept identity
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"]._conceptIdentityRef["id_"], "COMMENT")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"]._conceptIdentityRef["agencyId"], "SDMX")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"]._conceptIdentityRef["maintainableParentId"], "CROSS_DOMAIN_CONCEPTS")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"]._conceptIdentityRef["package"], "conceptscheme")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"]._conceptIdentityRef["maintainableParentVersion"], "1.0")
            #AttributeRelationship
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["COMMENT"].relatedTo, "PrimaryMeasure")
            #Local representation
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["FREQ"].localRepresentation._codeListReference["id_"], "CL_FREQ")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["FREQ"].localRepresentation._codeListReference["version"], "1.0")
        self.assertEqual(self.mes.dsds[urn].attributeDescriptor["FREQ"].localRepresentation._codeListReference["agencyId"], "RBI")

        #Testing measure descriptor
        urnDd = "urn:sdmx:org.sdmx.infomodel.datastructure.MeasureDescriptor=RBI:AALOE(1.0).MeasureDescriptor"
        self.assertEqual(self.mes.dsds[urn].measureDescriptor.urn, urnDd)
        self.assertEqual(self.mes.dsds[urn].measureDescriptor.id, "MeasureDescriptor")
            #Testign attributes
        urnMeasure = "urn:sdmx:org.sdmx.infomodel.datastructure.PrimaryMeasure=RBI:AALOE(1.0).OBS_VALUE"
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"].urn, urnMeasure)
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"].id, "OBS_VALUE")
            #Concept identity
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"]._conceptIdentityRef["id_"], "OBS_VALUE")
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"]._conceptIdentityRef["agencyId"], "SDMX")
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"]._conceptIdentityRef["maintainableParentId"], "CROSS_DOMAIN_CONCEPTS")
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"]._conceptIdentityRef["package"], "conceptscheme")
        self.assertEqual(self.mes.dsds[urn].measureDescriptor["OBS_VALUE"]._conceptIdentityRef["maintainableParentVersion"], "1.0")

        #Test codes methods
        dimensionCodes = ['RECO_PER', 'Measure_Type', 'Entry_Type', 'Area_Operation', 'DMID', 'TIME_PERIOD']
        self.assertEqual(self.mes.dsds[urn].dimensionCodes, dimensionCodes)
        attributeCodes = ['COMMENT', 'FREQ', 'DEPENDENCY_TYPE', 'Currency', 'AUDST']
        self.assertEqual(self.mes.dsds[urn].attributeCodes, attributeCodes)
        self.assertEqual(self.mes.dsds[urn].measureCode, "OBS_VALUE")