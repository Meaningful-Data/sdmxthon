"""
Metadata from Different Sources Tests
"""
import os
import unittest

from .. import TestHelper


class MetadataDifferent(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'bis.xml'
        reference = 'bis.pickle'

        self.metadata_compare(reference, data)

    def test_2(self):
        data = 'ecb.xml'
        reference = 'ecb.pickle'

        self.metadata_compare(reference, data)

    def test_3(self):
        data = 'estat.xml'
        reference = 'estat.pickle'

        self.metadata_compare(reference, data)

    def test_4(self):
        data = 'imf.xml'
        reference = 'imf.pickle'

        self.metadata_compare(reference, data)

    def test_5(self):
        data = 'wb.xml'
        reference = 'wb.pickle'

        self.metadata_compare(reference, data)


if __name__ == '__main__':
    unittest.main(verbosity=1)
