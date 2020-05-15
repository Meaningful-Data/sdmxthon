#TODO: Setters and attributes checking

import unittest
from datetime import datetime
from sdmxthon.model import message, base
from pathlib import Path

STRUCTURE_MESSAGES = Path().absolute() / "tests" /"resources_structureMessage"
DATA_MESSAGES = Path().absolute() / "tests" /"resources_dataMessage"


class EcbOrgschmeTestCase(unittest.TestCase):
    def setUp(self):
        self.mes = message.Message().fromXml(str(STRUCTURE_MESSAGES / "ECB_orgscheme.xml"))
        
    def test_header(self):
        self.assertEqual(self.mes.header.id, "IDREF8689", "Wrong message ID")
        self.assertEqual(self.mes.header.test, False, "Wrong test attibute")
        self.assertEqual(self.mes.header.prepared, datetime(2018, 11, 11, 11, 27,33), "Wrong prepared attibute")
        self.assertEqual(self.mes.header.senderId, "ECB", "Wrong senderId attibute")
        self.assertEqual(self.mes.header.receiverId, "not_supplied", "Wrong receiverId attibute")

    def test_organisationScheme(self):
        urn1 = "urn:sdmx:org.sdmx.infomodel.base.AgencyScheme=ECB:AGENCIES(1.0)" 
        urn2 = "urn:sdmx:org.sdmx.infomodel.base.AgencyScheme=SDMX:AGENCIES(1.0)"
        self.assertEqual(len(self.mes.organisationSchemes), 2)
        
        #Testing attributes
        self.assertEqual(self.mes.organisationSchemes[urn1].maintainer.id, "ECB")
        self.assertEqual(self.mes.organisationSchemes[urn2].maintainer.id, "SDMX")

        self.assertEqual(self.mes.organisationSchemes[urn1].urn, urn1, "The urn is not correctly generated")
        self.assertEqual(self.mes.organisationSchemes[urn2].urn, urn2, "The urn is not correctly generated")
        
        #Testing name
        self.assertEqual(len(self.mes.organisationSchemes[urn1].name.localisedStrings), 1)
        self.assertEqual(len(self.mes.organisationSchemes[urn2].name.localisedStrings), 1)

        self.assertEqual(self.mes.organisationSchemes[urn1].name.getLocales(), {"en"})
        self.assertEqual(self.mes.organisationSchemes[urn1].name["en"], "Agencies")
        self.assertEqual(self.mes.organisationSchemes[urn2].name.getLocales(), {"en"})
        self.assertEqual(self.mes.organisationSchemes[urn2].name["en"], "SDMX Agency Scheme")


        #Testing items
        self.assertEqual(len(self.mes.organisationSchemes[urn1].items), 1)
        self.assertEqual(len(self.mes.organisationSchemes[urn2].items), 7)

        name = base.InternationalString([base.LocalisedString("en", "ECB Dissemination")])
        urn  = "urn:sdmx:org.sdmx.infomodel.base.Agency=ECB.DISS"
        self.assertEqual(self.mes.organisationSchemes[urn1].items["DISS"].id, "DISS")
        self.assertEqual(self.mes.organisationSchemes[urn1].items["DISS"].name["en"], "ECB Dissemination")
        self.assertEqual(self.mes.organisationSchemes[urn1].items["DISS"].urn, urn)

        name = base.InternationalString([base.LocalisedString("en", "Bank for International Settlements")])
        urn  = "urn:sdmx:org.sdmx.infomodel.base.Agency=BIS"
        self.assertEqual(self.mes.organisationSchemes[urn2].items["BIS"].id, "BIS")
        self.assertEqual(self.mes.organisationSchemes[urn2].items["BIS"].name["en"], "Bank for International Settlements")
        self.assertEqual(self.mes.organisationSchemes[urn2].items["BIS"].urn, urn)