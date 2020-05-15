#Test that I cannot attach an item scheme different to the item type

import unittest
from datetime import datetime
from sdmxthon.model import itemScheme, base

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
        maintainer = itemScheme.Agency()
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
                                            maintainer = maintainer)

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
        self.assertEqual(iScheme.maintainer, maintainer, "ItemScheme maintainer not correctly initiated")
        
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

class ConceptSchemeCase(unittest.TestCase):
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
        concept1 = itemScheme.Concept(id_="test1")
        concept2 = itemScheme.Concept(id_="test2")
        conceptScheme = itemScheme.ConceptScheme(id_ = "id1",
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
                                            maintainer = None,
                                            items=[concept1, concept2])

        self.assertEqual(conceptScheme.id, "id1", "ConceptScheme id not correctly initiated")
        self.assertEqual(conceptScheme.uri, "uri", "ConceptScheme uri not correctly initiated")
        self.assertEqual(conceptScheme.annotations, [self.annotation], "ConceptScheme annotations not correctly initiated")
        self.assertEqual(conceptScheme.name, self.i_string, "ConceptScheme name not correctly initiated")
        self.assertEqual(conceptScheme.description, self.i_string, "ConceptScheme description not correctly initiated")
        self.assertEqual(conceptScheme.version, "1", "ConceptScheme version not correctly initiated")
        self.assertEqual(conceptScheme.validFrom, datetime(year=2020, month=4, day=29), "ConceptScheme validFrom not correctly initiated")
        self.assertEqual(conceptScheme.validTo, datetime(year=2020, month=4, day=29), "ConceptScheme validTo not correctly initiated")
        self.assertEqual(conceptScheme.isFinal, True, "ConceptScheme isFinal not correctly initiated")
        self.assertEqual(conceptScheme.isExternalReference, False, "ConceptScheme isExternalReference not correctly initiated")
        self.assertEqual(conceptScheme.serviceUrl, "ServiceURL", "ConceptScheme serviceUrl not correctly initiated")
        self.assertEqual(conceptScheme.structureUrl, "StructureURK", "ConceptScheme structureUrl not correctly initiated")
        self.assertEqual(conceptScheme.maintainer, None, "ConceptScheme maintainer not correctly initiated")
        self.assertEqual(conceptScheme.items, {"test1": concept1, "test2": concept2}, "ConceptScheme items not correctly initiated")

        conceptScheme = itemScheme.ConceptScheme()
        self.assertEqual(conceptScheme.annotations, [], "ConceptScheme not correctly initiated without arguments")
    
    def test_append(self):
        conceptScheme = itemScheme.ConceptScheme()
        concept1 = itemScheme.Concept(id_="test")
        code = itemScheme.Code()

        conceptScheme.append(concept1)
        self.assertEqual(conceptScheme.items, {"test": concept1}, f"Error appending a concept to a concept scheme {conceptScheme.items}")
        self.assertEqual(concept1.scheme, conceptScheme, "Error appending a concept to a concept scheme. The property scheme of the concept has not changed")

        conceptScheme.append(concept1)
        self.assertEqual(conceptScheme.items,  {"test": concept1}, "Error, the same concept appended twice to a concept scheme")

        with self.assertRaises(TypeError):
            conceptScheme.append(code)

class CodeListCase(unittest.TestCase):
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
        code1 = itemScheme.Code(id_="test1")
        code2 = itemScheme.Code(id_="test2")
        codeList = itemScheme.CodeList(id_ = "id1",
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
                                            maintainer = None,
                                            items=[code1, code2])

        self.assertEqual(codeList.id, "id1", "CodeList id not correctly initiated")
        self.assertEqual(codeList.uri, "uri", "CodeList uri not correctly initiated")
        self.assertEqual(codeList.annotations, [self.annotation], "CodeList annotations not correctly initiated")
        self.assertEqual(codeList.name, self.i_string, "CodeList name not correctly initiated")
        self.assertEqual(codeList.description, self.i_string, "CodeList description not correctly initiated")
        self.assertEqual(codeList.version, "1", "CodeList version not correctly initiated")
        self.assertEqual(codeList.validFrom, datetime(year=2020, month=4, day=29), "CodeList validFrom not correctly initiated")
        self.assertEqual(codeList.validTo, datetime(year=2020, month=4, day=29), "CodeList validTo not correctly initiated")
        self.assertEqual(codeList.isFinal, True, "CodeList isFinal not correctly initiated")
        self.assertEqual(codeList.isExternalReference, False, "CodeList isExternalReference not correctly initiated")
        self.assertEqual(codeList.serviceUrl, "ServiceURL", "CodeList serviceUrl not correctly initiated")
        self.assertEqual(codeList.structureUrl, "StructureURK", "CodeList structureUrl not correctly initiated")
        self.assertEqual(codeList.maintainer, None, "CodeList maintainer not correctly initiated")
        self.assertEqual(codeList.items, {"test1": code1, "test2": code2}, "CodeList items not correctly initiated")

        codeList = itemScheme.CodeList()
        self.assertEqual(codeList.annotations, [], "CodeList not correctly initiated without arguments")
    
    def test_append(self):
        codeList = itemScheme.CodeList()
        code = itemScheme.Code(id_="test")
        concept = itemScheme.Concept()

        codeList.append(code)
        self.assertEqual(codeList.items, {"test": code} , "Error appending a code to a codelist")
        self.assertEqual(code.scheme, codeList, "Error appending a code to a codelist. The property scheme of the code has not changed")

        codeList.append(code)
        self.assertEqual(codeList.items, {"test": code}, "Error, the same code appended twice to a codelist")

        with self.assertRaises(TypeError):
            codeList.append(concept)
            
class AgencyListCase(unittest.TestCase):
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
        agency1 = itemScheme.Agency(id_="test1")
        agency2 = itemScheme.Agency(id_="test2")
        agencyList = itemScheme.AgencyList(id_ = "id1",
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
                                            maintainer = None,
                                            items=[agency1, agency2])

        self.assertEqual(agencyList.id, "id1", "AgencyList id not correctly initiated")
        self.assertEqual(agencyList.uri, "uri", "AgencyList uri not correctly initiated")
        self.assertEqual(agencyList.annotations, [self.annotation], "AgencyList annotations not correctly initiated")
        self.assertEqual(agencyList.name, self.i_string, "AgencyList name not correctly initiated")
        self.assertEqual(agencyList.description, self.i_string, "AgencyList description not correctly initiated")
        self.assertEqual(agencyList.version, "1", "AgencyList version not correctly initiated")
        self.assertEqual(agencyList.validFrom, datetime(year=2020, month=4, day=29), "AgencyList validFrom not correctly initiated")
        self.assertEqual(agencyList.validTo, datetime(year=2020, month=4, day=29), "AgencyList validTo not correctly initiated")
        self.assertEqual(agencyList.isFinal, True, "AgencyList isFinal not correctly initiated")
        self.assertEqual(agencyList.isExternalReference, False, "AgencyList isExternalReference not correctly initiated")
        self.assertEqual(agencyList.serviceUrl, "ServiceURL", "AgencyList serviceUrl not correctly initiated")
        self.assertEqual(agencyList.structureUrl, "StructureURK", "AgencyList structureUrl not correctly initiated")
        self.assertEqual(agencyList.maintainer, None, "AgencyList maintainer not correctly initiated")
        self.assertEqual(agencyList.items, {"test1": agency1, "test2": agency2}, "AgencyList items not correctly initiated")

        agencyList = itemScheme.AgencyList()
        self.assertEqual(agencyList.annotations, [], "AgencyList not correctly initiated without arguments")
    
    def test_append(self):
        agencyList = itemScheme.AgencyList()
        agency = itemScheme.Agency(id_="test")
        concept = itemScheme.Concept()

        agencyList.append(agency)
        self.assertEqual(agencyList.items, {"test": agency}, "Error appending an agency to an agency list")
        self.assertEqual(agency.scheme, agencyList, "Error appending an agency to an agency list. The property scheme of the agency has not changed")

        agencyList.append(agency)
        self.assertEqual(agencyList.items, {"test": agency}, "Error, the same agency appended twice to an agency list")

        with self.assertRaises(TypeError):
            agencyList.append(concept)

class ConceptTestCase(unittest.TestCase):
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
        concept = itemScheme.Concept(id_ = "id1",
                                uri = "uri",
                                annotations = [self.annotation],
                                name = self.i_string,
                                description = self.i_string,
                                isPartial= True)

        self.assertEqual(concept.id, "id1", "Concept id not correctly initiated")
        self.assertEqual(concept.uri, "uri", "Concept uri not correctly initiated")
        self.assertEqual(concept.annotations, [self.annotation], "Concept annotations not correctly initiated")
        self.assertEqual(concept.name, self.i_string, "Concept name not correctly initiated")
        self.assertEqual(concept.description, self.i_string, "Concept description not correctly initiated")
        self.assertEqual(concept.isPartial, True, "Concept isPartial not correctly initiated")
        
        concept = itemScheme.Concept()
        self.assertEqual(concept.annotations, [], "Concept not correctly initiated without arguments")

    def test_schemeSetter(self):
        concept = itemScheme.Concept()
        conceptScheme = itemScheme.ConceptScheme()
        conceptScheme2 = itemScheme.ConceptScheme()
        codeList = itemScheme.CodeList()

        concept.scheme = conceptScheme
        self.assertEqual(concept.scheme, conceptScheme, "concept scheme not correctly set")
        concept.scheme = conceptScheme2
        self.assertEqual(concept.scheme, conceptScheme2, "concept scheme not correctly set when changed from another scheme")

        with self.assertRaises(TypeError):
            concept.scheme = codeList

    def test_parentSetter(self):
        conceptParent = itemScheme.Concept()
        conceptChild = itemScheme.Concept()
        code = itemScheme.Code()

        conceptChild.parent = conceptParent
        self.assertEqual(conceptChild.parent, conceptParent, "concept parent not correctly set")
        self.assertEqual(conceptParent.childs, [conceptChild], "The child was not added to the parent childs")

        with self.assertRaises(TypeError):
            conceptChild.parent = code

    def test_addChild(self):
        conceptParent = itemScheme.Concept()
        conceptChild = itemScheme.Concept()
        code = itemScheme.Code()

        conceptParent.addChild(conceptChild)
        self.assertEqual(conceptParent.childs, [conceptChild], "The child was not added to the parent childs")
        self.assertEqual(conceptChild.parent, conceptParent, "concept parent not correctly set from addChild")

        with self.assertRaises(TypeError):
            conceptParent.addChild(code)

class CodeTestCase(unittest.TestCase):
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
        code = itemScheme.Code(id_ = "id1",
                                uri = "uri",
                                annotations = [self.annotation],
                                name = self.i_string,
                                description = self.i_string,
                                isPartial= True)

        self.assertEqual(code.id, "id1", "Code id not correctly initiated")
        self.assertEqual(code.uri, "uri", "Code uri not correctly initiated")
        self.assertEqual(code.annotations, [self.annotation], "Code annotations not correctly initiated")
        self.assertEqual(code.name, self.i_string, "Code name not correctly initiated")
        self.assertEqual(code.description, self.i_string, "Code description not correctly initiated")
        self.assertEqual(code.isPartial, True, "Code isPartial not correctly initiated")
        
        code = itemScheme.Code()
        self.assertEqual(code.annotations, [], "Code not correctly initiated without arguments")

    def test_schemeSetter(self):
        code = itemScheme.Code()
        codeList = itemScheme.CodeList()
        codeList2 = itemScheme.CodeList()
        conceptScheme= itemScheme.ConceptScheme()

        code.scheme = codeList
        self.assertEqual(code.scheme, codeList, "codelist not correctly set")
        code.scheme = codeList2
        self.assertEqual(code.scheme, codeList2, "codelist not correctly set when changed from another scheme")

        with self.assertRaises(TypeError):
            code.scheme = conceptScheme

    def test_parentSetter(self):
        codeParent = itemScheme.Code()
        codeChild = itemScheme.Code()
        concept = itemScheme.Concept()

        codeChild.parent = codeParent
        self.assertEqual(codeChild.parent, codeParent, "code parent not correctly set")
        self.assertEqual(codeParent.childs, [codeChild], "The child was not added to the parent childs")

        with self.assertRaises(TypeError):
            codeChild.parent = concept

    def test_addChild(self):
        codeParent = itemScheme.Code()
        codeChild = itemScheme.Code()
        concept = itemScheme.Concept()

        codeParent.addChild(codeChild)
        self.assertEqual(codeParent.childs, [codeChild], "The child was not added to the parent childs")
        self.assertEqual(codeChild.parent, codeParent, "concept parent not correctly set from addChild")

        with self.assertRaises(TypeError):
            codeParent.addChild(concept)

class AgencyTestCase(unittest.TestCase):
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
        agency = itemScheme.Agency(id_ = "id1",
                                uri = "uri",
                                annotations = [self.annotation],
                                name = self.i_string,
                                description = self.i_string,
                                isPartial= True)

        self.assertEqual(agency.id, "id1", "Agency id not correctly initiated")
        self.assertEqual(agency.uri, "uri", "Agency uri not correctly initiated")
        self.assertEqual(agency.annotations, [self.annotation], "Agency annotations not correctly initiated")
        self.assertEqual(agency.name, self.i_string, "Agency name not correctly initiated")
        self.assertEqual(agency.description, self.i_string, "Agency description not correctly initiated")
        self.assertEqual(agency.isPartial, True, "Agency isPartial not correctly initiated")
        
        agency = itemScheme.Agency()
        self.assertEqual(agency.annotations, [], "Agency not correctly initiated without arguments")

    def test_schemeSetter(self):
        agency = itemScheme.Agency()
        agencyList = itemScheme.AgencyList()
        agencyList2 = itemScheme.AgencyList()
        conceptScheme= itemScheme.ConceptScheme()

        agency.scheme = agencyList
        self.assertEqual(agency.scheme, agencyList, "codelist not correctly set")
        agency.scheme = agencyList2
        self.assertEqual(agency.scheme, agencyList2, "codelist not correctly set when changed from another scheme")

        with self.assertRaises(TypeError):
            agency.scheme = conceptScheme

if __name__ == '__main__':
    unittest.main()