"""
Metadata Equality Tests
"""
import os
import unittest

from SDMXThon.testSuite import TestHelper


class MetadataEquality(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")

    def test_1(self):
        data = 'bis.xml'

        self.metadata_equality(data)

    def test_2(self):
        data = 'estat.xml'

        self.metadata_equality(data)

    def test_3(self):
        data = 'imf.xml'

        self.metadata_equality(data)

    def test_4(self):
        data = 'wb.xml'
        self.metadata_equality(data)

    def test_6(self):
        self.metadata_inequality()


if __name__ == '__main__':
    unittest.main(verbosity=1)
