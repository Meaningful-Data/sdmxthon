"""
Codelist writing Tests
"""
import os
import unittest

from SDMXThon.testSuite import TestHelper


class CodelistWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'bis.xml'
        reference = 'bis.txt'
        codelist_name = 'BIS:CL_AVAILABILITY(1.0)'

        self.metadata_codelist_writing(reference, data, codelist_name)

    def test_2(self):
        data = 'estat.xml'
        reference = 'estat.txt'
        codelist_name = 'ESTAT:FREQ(1.5)'

        self.metadata_codelist_writing(reference, data, codelist_name)

    def test_3(self):
        data = 'imf.xml'
        reference = 'imf.txt'
        codelist_name = 'IMF:CL_ALT_FISCAL_INDICATOR(1.0)'

        self.metadata_codelist_writing(reference, data, codelist_name)

    def test_4(self):
        data = 'wb.xml'
        reference = 'wb.txt'
        codelist_name = 'WB:CL_REF_AREA_WDI(1.0)'

        self.metadata_codelist_writing(reference, data, codelist_name)


if __name__ == '__main__':
    unittest.main(verbosity=1)
