import json
import os
import pickle
import sqlite3
import unittest

import pandas as pd

from SDMXThon.parsers.metadata_validations import getMetadata
from ..api import DataSet, readXML, MetadataType, setReferences, readSDMX


def query_to_db(sqlite_db, limit):
    return f'SELECT * from {sqlite_db} LIMIT {limit}'


class TestHelper(unittest.TestCase):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def load_input_data(self, sqlite_db, sqlite_filename, limit, pkl_filename):
        conn = sqlite3.connect(os.path.join(self.pathToDB, sqlite_filename))
        df = pd.read_sql(query_to_db(sqlite_db, limit), conn).astype('category')

        with open(os.path.join(self.pathToMetadata, pkl_filename), 'rb') as f:
            dsd = pickle.loads(f.read())

        return DataSet(structure=dsd, data=df)

    def load_reference_data(self, reference_filename):
        with open(os.path.join(self.pathToReference, reference_filename)) as f:
            return json.loads(f.read())

    def load_reference_pickle(self, reference_filename):
        with open(os.path.join(self.pathToReference, reference_filename), 'rb') as f:
            return pickle.loads(f.read())

    def reading_test(self, data_filename):
        metadata_filename = os.path.join(self.pathToMetadata, "metadata.xml")
        message = readSDMX(os.path.join(self.pathToDB, data_filename), metadata_filename)
        with open(os.path.join(self.pathToDB, "df.pickle"), 'rb') as f:
            reference = pickle.loads(f.read())
        dataframe = message.payload['BIS:BIS_DER(1.0)'].data.astype('str')
        pd.testing.assert_frame_equal(dataframe.replace('nan', ''), reference.replace('nan', ''), check_like=True)

    def semantic_test(self, sqlite_db, sqlite_filename, limit, pkl_filename, reference_filename):
        dataset = self.load_input_data(sqlite_db, sqlite_filename, limit, pkl_filename)
        errors = dataset.semanticValidation()
        reference_dict = self.load_reference_data(reference_filename)
        self.assert_equal_validation(json.loads(json.dumps(errors).replace("NaN", 'null')), reference_dict)

    def semantic_valid_test(self, sqlite_db, sqlite_filename, limit, pkl_filename):
        dataset = self.load_input_data(sqlite_db, sqlite_filename, limit, pkl_filename)
        errors = dataset.semanticValidation()
        self.assert_equal_validation(errors, [])

    def metadata_test(self, reference_filename, path_to_data):
        obj_ = getMetadata(os.path.join(self.pathToMetadata, path_to_data))
        reference = self.load_reference_data(reference_filename)
        errors = obj_.structures.errors
        if errors is None:
            errors = []
        self.assert_equal_validation(errors, reference)

    def metadata_valid_test(self, path_to_data):
        obj_ = readXML(os.path.join(self.pathToMetadata, path_to_data))
        if isinstance(obj_, MetadataType):
            setReferences(obj_)
        errors = obj_.structures.errors
        if errors is None:
            errors = []
        self.assert_equal_validation(errors, [])

    def metadata_compare(self, reference_filename, data_filename):
        obj_ = getMetadata(os.path.join(self.pathToDB, data_filename))
        reference = self.load_reference_pickle(reference_filename)
        self.assertEqual(obj_.structures == reference, True)

    def assert_equal_validation(self, result, reference):
        if len(result) == len(reference):
            self.assertCountEqual(result, reference)
        else:
            self.assertEqual(result, reference)


if __name__ == '__main__':
    pass
