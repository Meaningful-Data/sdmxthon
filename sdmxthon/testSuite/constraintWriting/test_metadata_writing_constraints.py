"""
Constraints writing Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class ConstraintWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'series.xml'
        reference = 'series.txt'

        self.metadata_constraint_writing(reference, data)

    def test_2(self):
        data = 'cube.xml'
        reference = 'cube.txt'

        self.metadata_constraint_writing(reference, data)


if __name__ == '__main__':
    unittest.main(verbosity=1)
