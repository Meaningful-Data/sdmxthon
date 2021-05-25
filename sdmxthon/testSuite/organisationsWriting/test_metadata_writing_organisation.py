"""
Organisations writing Tests
"""
import os
import unittest

from SDMXThon.testSuite import TestHelper


class OrganisationWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'bis.xml'
        reference = 'bis.txt'

        self.metadata_agency_scheme_writing(reference, data)

    def test_2(self):
        data = 'imf.xml'
        reference = 'imf.txt'

        self.metadata_agency_scheme_writing(reference, data)


if __name__ == '__main__':
    unittest.main(verbosity=1)
