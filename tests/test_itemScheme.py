#Test that I cannot attach an item scheme different to the item type

import unittest
from datetime import datetime
from model import itemScheme, base

class ItemSchemeTestCase(unittest.TestCase):
    def setUp(self):
        ls_en = base.LocalisedString(locale="en", label="test string")
        ls_es = base.LocalisedString(locale="es", label="String de prueba")
        self.i_string = base.InternationalString([ls_en, ls_es])
        self.annotation = base.Annotation(id_ = "AnnotationIDtest", 
                                        title = "Test title", 
                                        type_ = "Test type",
                                        url = "Test url", 
                                        text = self.i_string)
        
    def test_constructor(self):
        iScheme = itemScheme.ItemScheme(id_ = "id1",
                                            uri = "uri",
                                            annotations = [self.annotation],
                                            name = self.i_string,
                                            description = self.i_string,
                                            version = "1",
                                            validFrom=datetime(year=2020, month=4, day=29),
                                            validTo=datetime(year=2020, month=4, day=29),
                                            isFinal = True, 
                                            isExternalReference = False, 
                                            serviceUrl = "ServiceURL", 
                                            structureUrl = "StructureURK", 
                                            maintainer = None)

        self.assertEqual(iScheme.id, "id1", "ItemScheme id not correctly initiated")
        self.assertEqual(iScheme.uri, "uri", "ItemScheme uri not correctly initiated")
        self.assertEqual(iScheme.annotations, [self.annotation], "ItemScheme annotations not correctly initiated")
        self.assertEqual(iScheme.name, self.i_string, "ItemScheme name not correctly initiated")
        self.assertEqual(iScheme.description, self.i_string, "ItemScheme description not correctly initiated")
        self.assertEqual(iScheme.version, "1", "ItemScheme version not correctly initiated")
        self.assertEqual(iScheme.validFrom, datetime(year=2020, month=4, day=29), "ItemScheme validFrom not correctly initiated")
        self.assertEqual(iScheme.validTo, datetime(year=2020, month=4, day=29), "ItemScheme validTo not correctly initiated")
        self.assertEqual(iScheme.isFinal, True, "ItemScheme isFinal not correctly initiated")
        self.assertEqual(iScheme.isExternalReference, False, "ItemScheme isExternalReference not correctly initiated")
        self.assertEqual(iScheme.serviceUrl, "ServiceURL", "ItemScheme serviceUrl not correctly initiated")
        self.assertEqual(iScheme.structureUrl, "StructureURK", "ItemScheme structureUrl not correctly initiated")
        self.assertEqual(iScheme.maintainer, None, "ItemScheme maintainer not correctly initiated")
        
        iScheme = itemScheme.ItemScheme()
        self.assertEqual(iScheme.annotations, [], "ItemScheme not correctly initiated without arguments")


class ItemTestCase(unittest.TestCase):
    def setUp(self):
        ls_en = base.LocalisedString(locale="en", label="test string")
        ls_es = base.LocalisedString(locale="es", label="String de prueba")
        self.i_string = base.InternationalString([ls_en, ls_es])
        self.annotation = base.Annotation(id_ = "AnnotationIDtest", 
                                        title = "Test title", 
                                        type_ = "Test type",
                                        url = "Test url", 
                                        text = self.i_string)
        
    def test_constructor(self):
        item = itemScheme.Item(id_ = "id1",
                                uri = "uri",
                                annotations = [self.annotation],
                                name = self.i_string,
                                description = self.i_string,
                                isPartial= True)

        self.assertEqual(item.id, "id1", "Item id not correctly initiated")
        self.assertEqual(item.uri, "uri", "Item uri not correctly initiated")
        self.assertEqual(item.annotations, [self.annotation], "Item annotations not correctly initiated")
        self.assertEqual(item.name, self.i_string, "Item name not correctly initiated")
        self.assertEqual(item.description, self.i_string, "Item description not correctly initiated")
        self.assertEqual(item.isPartial, True, "Item isPartial not correctly initiated")
        
        item = itemScheme.Item()
        self.assertEqual(item.annotations, [], "Item not correctly initiated without arguments")


if __name__ == '__main__':
    unittest.main()