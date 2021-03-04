"""
Semantic Validation Tests
"""
import os
import unittest

from .. import TestHelper


class SemanticValidation(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        sqlite_db = 'BIS_DER'
        sqlite_filename = 'BIS_DER_OUTS.db'
        limit = 10
        pkl_filename = 'dsd1.pickle'
        reference_filename = 'errors_test_1.json'

        self.semantic_test(sqlite_db, sqlite_filename, limit, pkl_filename, reference_filename)

    def test_2(self):
        sqlite_db = 'BIS_DER'
        sqlite_filename = 'BIS_DER_OUTS.db'
        limit = 10
        pkl_filename = 'dsd1.pickle'
        self.semantic_valid_test(sqlite_db, sqlite_filename, limit, pkl_filename)

    def test_3(self):
        sqlite_db = 'BIS_DER_facets'
        sqlite_filename = 'BIS_DER_OUTS.db'
        limit = 100
        pkl_filename = 'dsd1.pickle'
        reference_filename = 'errors_test_3.json'
        self.semantic_test(sqlite_db, sqlite_filename, limit, pkl_filename, reference_filename)


if __name__ == '__main__':
    unittest.main(verbosity=1)
