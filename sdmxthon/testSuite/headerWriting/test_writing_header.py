"""
Header Writing Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class HeaderWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        reference = 'header.txt'

        self.header_writing(reference)


if __name__ == '__main__':
    unittest.main(verbosity=1)
