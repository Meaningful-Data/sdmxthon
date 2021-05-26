"""
Datasets Validation Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class DatasetsValidation(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'valid.xml'
        metadata = 'metadata.xml'
        self.datasets_validation(data, metadata)

    def test_2(self):
        data = 'invalid.xml'
        metadata = 'metadata.xml'
        reference_filename = "errors_test_2.json"
        self.datasets_validation(data, metadata, reference_filename)


if __name__ == '__main__':
    unittest.main(verbosity=1)
