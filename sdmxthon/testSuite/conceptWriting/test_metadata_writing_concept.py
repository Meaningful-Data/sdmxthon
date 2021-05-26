"""
Concept writing Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class ConceptWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'bis.xml'
        reference = 'bis.txt'
        concept_name = 'BIS:BIS_CONCEPT_SCHEME(1.0)'

        self.metadata_concept_writing(reference, data, concept_name)

    def test_2(self):
        data = 'estat.xml'
        reference = 'estat.txt'
        concept_name = 'ESTAT:HLTH_RS_PRSHP1(7.0)'

        self.metadata_concept_writing(reference, data, concept_name)

    def test_3(self):
        data = 'wb.xml'
        reference = 'wb.txt'
        concept_name = 'WB:WDI_CONCEPT(1.0)'

        self.metadata_concept_writing(reference, data, concept_name)

    def test_4(self):
        data = 'imf.xml'
        reference = 'imf.txt'
        concept_name = 'IMF:ECOFIN_CONCEPTS(1.0)'

        self.metadata_concept_writing(reference, data, concept_name)


if __name__ == '__main__':
    unittest.main(verbosity=1)
