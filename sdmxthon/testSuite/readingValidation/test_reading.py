"""
Reading Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class ReadingValidation(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data_filename = 'gen_all.xml'

        self.reading_test(data_filename)

    def test_2(self):
        data_filename = 'gen_ser.xml'

        self.reading_test(data_filename)

    def test_3(self):
        data_filename = 'str_all.xml'

        self.reading_test(data_filename)

    def test_4(self):
        data_filename = 'str_ser.xml'

        self.reading_test(data_filename)

    def test_5(self):
        data_filename = 'dataflow.xml'

        self.reading_test(data_filename)


if __name__ == '__main__':
    unittest.main(verbosity=1)
