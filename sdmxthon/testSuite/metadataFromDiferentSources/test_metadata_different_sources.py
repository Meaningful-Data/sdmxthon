"""
Metadata from Different Sources Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class MetadataDifferent(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'bis.xml'
        reference = 'bis.txt'
        dsd_name = 'BIS:BIS_DER(1.0)'

        self.metadata_compare(reference, data, dsd_name)

    def test_2(self):
        data = 'ecb.xml'
        reference = 'ecb.txt'

        dsd_name = 'IMF:BOP(1.9)'

        self.metadata_compare(reference, data, dsd_name)

    def test_3(self):
        data = 'estat.xml'
        reference = 'estat.txt'

        dsd_name = 'ESTAT:HLTH_RS_PRSHP1(7.0)'

        self.metadata_compare(reference, data, dsd_name)

    def test_4(self):
        data = 'imf.xml'
        reference = 'imf.txt'

        dsd_name = 'IMF:ALT_FISCAL_DSD(1.0)'

        self.metadata_compare(reference, data, dsd_name)

    def test_5(self):
        data = 'wb.xml'
        reference = 'wb.txt'

        dsd_name = 'WB:WDI(1.0)'

        self.metadata_compare(reference, data, dsd_name)


if __name__ == '__main__':
    unittest.main(verbosity=1)
