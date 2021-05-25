"""
Data Writing Tests
"""
import os
import unittest

from SDMXThon import MessageTypeEnum
from SDMXThon.testSuite import TestHelper


class DataWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        self.data_writing(MessageTypeEnum.GenericDataSet)

    def test_2(self):
        self.data_writing(MessageTypeEnum.StructureDataSet)

    def test_3(self):
        self.data_writing(MessageTypeEnum.StructureDataSet, series=True)


if __name__ == '__main__':
    unittest.main(verbosity=1)
