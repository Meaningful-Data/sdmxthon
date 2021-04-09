"""
Metadata Validation Tests
"""
import os
import unittest

from SDMXThon.testSuite import TestHelper


class MetadataValidation(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        path_to_data = 'test_errors.xml'
        reference_filename = 'errors_metadata_test_1.json'

        self.metadata_test(reference_filename, path_to_data)

    def test_2(self):
        path_to_data = 'test_nodsd.xml'
        reference_filename = 'errors_metadata_test_2.json'

        self.metadata_test(reference_filename, path_to_data)

    def test_3(self):
        path_to_data = 'test_MX.xml'
        reference_filename = 'errors_metadata_test_3.json'

        self.metadata_test(reference_filename, path_to_data)

    def test_4(self):
        path_to_data = 'test_valid.xml'
        self.metadata_valid_test(path_to_data)


if __name__ == '__main__':
    unittest.main(verbosity=1)
