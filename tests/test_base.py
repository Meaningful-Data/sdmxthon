import unittest
from datetime import datetime
from model import base

class LocalisedStringTestCase(unittest.TestCase):
    def test_constructor(self):
        ls = base.LocalisedString(locale = "en", label = "test string")
        self.assertEqual(ls.locale, "en", "Error in LocalisedConstructor for locale")
        self.assertEqual(ls.label, "test string", "Error in LocalisedConstructor for label")

    def test_locale_non_string(self):
        with self.assertRaises(TypeError):
            base.LocalisedString(locale = 5, label = "test string")
            

    def test_label_non_string(self):
        with self.assertRaises(TypeError):
            base.LocalisedString(locale = "en", label = 5)

class InternationalStringTestCase(unittest.TestCase):
    def setUp(self):
        self.ls_en = base.LocalisedString(locale="en", label="test string")
        self.ls_es = base.LocalisedString(locale="es", label="String de prueba")
        self.i_string = base.InternationalString([self.ls_en, self.ls_es])

    def test_constructor(self):
        i_string = base.InternationalString([self.ls_en])
        self.assertEqual(i_string.localisedStrings, [self.ls_en], "InternationalString not correctly initiated with one argument")
        
        i_string = base.InternationalString()
        self.assertEqual(i_string.localisedStrings, [], "InternationalString not correctly initiated without arguments")

    def test_add_localisedString(self):
        i_string = base.InternationalString()
        i_string.addLocalisedString(self.ls_es)
        self.assertEqual(i_string.localisedStrings, [self.ls_es], "InternationalString addLocalisedString method not working")

    def test_getLocalisedString(self):
        self.assertEqual(self.i_string.getLocalisedString("en"), "test string", "InternationalString getLocalisedString method not working")

    def test_getLocales(self):
        self.assertEqual(self.i_string.getLocales(), {"es", "en"}, "InternationalString getLocales method not working")

class AnnotationTestCase(unittest.TestCase):
    def setUp(self):
        ls_en = base.LocalisedString(locale="en", label="test string")
        ls_es = base.LocalisedString(locale="es", label="String de prueba")
        self.i_string = base.InternationalString([ls_en, ls_es])
    
    def test_constructor(self):
        annotation = base.Annotation(id_ = "AnnotationIDtest", 
                                         title = "Test title", 
                                         type_ = "Test type",
                                         url = "Test url", 
                                         text = self.i_string)
        
        self.assertEqual(annotation.id, "AnnotationIDtest", "Error in Annotation constructor for id")
        self.assertEqual(annotation.title, "Test title", "Error in Annotation constructor for title")
        self.assertEqual(annotation.type, "Test type", "Error in Annotation constructor for type")
        self.assertEqual(annotation.url, "Test url", "Error in Annotation constructor for url")
        self.assertEqual(annotation.text, self.i_string, "Error in Annotation constructor for text")

class AnnotableArtefactTestCase(unittest.TestCase):
    def setUp(self):
        ls_en = base.LocalisedString(locale="en", label="test string")
        ls_es = base.LocalisedString(locale="es", label="String de prueba")
        i_string = base.InternationalString([ls_en, ls_es])
        self.annotation1 = base.Annotation(id_ = "AnnotationIDtest", 
                                              title = "Test title", 
                                              type_ = "Test type",
                                              url = "Test url", 
                                              text = i_string)
        self.annotation2 = base.Annotation(id_ = "Annotation2ID test", 
                                              title = "Test 2 title", 
                                              type_ = "Test 2 type",
                                              url = "Test 2 url", 
                                              text = i_string)

    def test_constructor(self):
        annotable = base.AnnotableArtefact([self.annotation1, self.annotation2])
        self.assertEqual(annotable.annotations, [self.annotation1, self.annotation2], "AnnotableArtefact not correctly initiated with one list as argument")
        
        annotable = base.AnnotableArtefact()
        self.assertEqual(annotable.annotations, [], "AnnotableArtefact not correctly initiated without arguments")

    def test_addAnnotation(self):
        annotable = base.AnnotableArtefact()
        annotable.addAnnotation(self.annotation1)
        self.assertEqual(annotable.annotations, [self.annotation1], "AnnotableArtefact addLocalisedString method not working")

class IdentifiableArtefactTestCase(unittest.TestCase):
    def setUp(self):
        ls_en = base.LocalisedString(locale="en", label="test string")
        ls_es = base.LocalisedString(locale="es", label="String de prueba")
        i_string = base.InternationalString([ls_en, ls_es])
        self.annotation = base.Annotation(id_ = "AnnotationIDtest", 
                                        title = "Test title", 
                                        type_ = "Test type",
                                        url = "Test url", 
                                        text = i_string)
        
    def test_constructor(self):
        identifiable = base.IdentifiableArtefact(id_ = "id1",
                                                     uri = "uri",
                                                     annotations = [self.annotation])
        self.assertEqual(identifiable.id, "id1", "IdentifiableArtefact id not correctly initiated")
        self.assertEqual(identifiable.uri, "uri", "IdentifiableArtefact uri not correctly initiated")
        self.assertEqual(identifiable.annotations, [self.annotation], "IdentifiableArtefact annotations not correctly initiated")
        
        identifiable = base.IdentifiableArtefact()
        self.assertEqual(identifiable.annotations, [], "AnnotableArtefact not correctly initiated without arguments")

class NameableArtefactTestCase(unittest.TestCase):
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
        nameable = base.NameableArtefact(id_ = "id1",
                                             uri = "uri",
                                             annotations = [self.annotation],
                                             name = self.i_string,
                                             description = self.i_string)

        self.assertEqual(nameable.id, "id1", "NameableArtefact id not correctly initiated")
        self.assertEqual(nameable.uri, "uri", "NameableArtefact uri not correctly initiated")
        self.assertEqual(nameable.annotations, [self.annotation], "NameableArtefact annotations not correctly initiated")
        self.assertEqual(nameable.name, self.i_string, "NameableArtefact name not correctly initiated")
        self.assertEqual(nameable.description, self.i_string, "NameableArtefact description not correctly initiated")
        
        nameable = base.NameableArtefact()
        self.assertEqual(nameable.annotations, [], "NameableArtefact not correctly initiated without arguments")

class VersionableArtefactTestCase(unittest.TestCase):
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
        versionable = base.VersionableArtefact(id_ = "id1",
                                                    uri = "uri",
                                                    annotations = [self.annotation],
                                                    name = self.i_string,
                                                    description = self.i_string,
                                                    version = "1",
                                                    validFrom=datetime(year=2020, month=4, day=29),
                                                    validTo=datetime(year=2020, month=4, day=29))

        self.assertEqual(versionable.id, "id1", "VersionableArtefact id not correctly initiated")
        self.assertEqual(versionable.uri, "uri", "VersionableArtefact uri not correctly initiated")
        self.assertEqual(versionable.annotations, [self.annotation], "VersionableArtefact annotations not correctly initiated")
        self.assertEqual(versionable.name, self.i_string, "VersionableArtefact name not correctly initiated")
        self.assertEqual(versionable.description, self.i_string, "VersionableArtefact description not correctly initiated")
        self.assertEqual(versionable.version, "1", "VersionableArtefact version not correctly initiated")
        self.assertEqual(versionable.validFrom, datetime(year=2020, month=4, day=29), "VersionableArtefact valid from not correctly initiated")
        self.assertEqual(versionable.validTo, datetime(year=2020, month=4, day=29), "VersionableArtefact valid to not correctly initiated")
        
        versionable = base.VersionableArtefact()
        self.assertEqual(versionable.annotations, [], "VersionableArtefact not correctly initiated without arguments")

    def test_date_methods(self):
        versionable = base.VersionableArtefact(validFrom=datetime(year=2020, month=4, day=29), validTo=datetime(year=2020, month=4, day=29))

        self.assertEqual(versionable.getValidFromString(), "2020-04-29", "VersionableArtefact method getValidFromString not generating correct string")
        self.assertEqual(versionable.getValidToString(), "2020-04-29", "VersionableArtefact method getValidToString not generating correct string")

        versionable = base.VersionableArtefact()
        versionable.setValidFromString("2020-04-29")
        versionable.setValidToString("2020-04-29")

        self.assertEqual(versionable.validFrom, datetime(year=2020, month=4, day=29), "VersionableArtefact method setValidFromString not working")
        self.assertEqual(versionable.validTo, datetime(year=2020, month=4, day=29), "VersionableArtefact method setValidFromString not working")

class MantainableArtefactTestCase(unittest.TestCase):
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
        maintainable = base.MaintainableArtefact(id_ = "id1",
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

        self.assertEqual(maintainable.id, "id1", "MaintainableArtefact id not correctly initiated")
        self.assertEqual(maintainable.uri, "uri", "MaintainableArtefact uri not correctly initiated")
        self.assertEqual(maintainable.annotations, [self.annotation], "MaintainableArtefact annotations not correctly initiated")
        self.assertEqual(maintainable.name, self.i_string, "MaintainableArtefact name not correctly initiated")
        self.assertEqual(maintainable.description, self.i_string, "MaintainableArtefact description not correctly initiated")
        self.assertEqual(maintainable.version, "1", "MaintainableArtefact version not correctly initiated")
        self.assertEqual(maintainable.validFrom, datetime(year=2020, month=4, day=29), "MaintainableArtefact validFrom not correctly initiated")
        self.assertEqual(maintainable.validTo, datetime(year=2020, month=4, day=29), "MaintainableArtefact validTo not correctly initiated")
        self.assertEqual(maintainable.isFinal, True, "MaintainableArtefact isFinal not correctly initiated")
        self.assertEqual(maintainable.isExternalReference, False, "MaintainableArtefact isExternalReference not correctly initiated")
        self.assertEqual(maintainable.serviceUrl, "ServiceURL", "MaintainableArtefact serviceUrl not correctly initiated")
        self.assertEqual(maintainable.structureUrl, "StructureURK", "MaintainableArtefact structureUrl not correctly initiated")
        self.assertEqual(maintainable.maintainer, None, "MaintainableArtefact maintainer not correctly initiated")
        
        maintainable = base.MaintainableArtefact()
        self.assertEqual(maintainable.annotations, [], "VersionableArtefact not correctly initiated without arguments")




if __name__ == '__main__':
    unittest.main()