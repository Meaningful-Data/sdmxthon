import json
import os
import sqlite3
import unittest
from datetime import datetime
from io import StringIO, BytesIO

import pandas as pd

from sdmxthon.api.api import _read_xml, MetadataType, _set_references, \
    read_sdmx, \
    get_datasets, get_pandas_df, xml_to_csv
from sdmxthon.model.dataset import Dataset
from sdmxthon.model.message import Message
from sdmxthon.parsers.new_read import read_xml
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict


def query_to_db(sqlite_db, limit):
    return f'SELECT * from {sqlite_db} LIMIT {limit}'


class TestHelper(unittest.TestCase):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def load_input_data(self, sqlite_db, sqlite_filename, limit, meta_file):
        conn = sqlite3.connect(os.path.join(self.pathToDB, sqlite_filename))
        df = pd.read_sql(query_to_db(sqlite_db, limit), conn).astype(
            'category')

        dsd = read_sdmx(os.path.join(self.pathToMetadata, meta_file)). \
            payload.dsds['BIS:BIS_DER(1.0)']

        return Dataset(structure=dsd, data=df)

    def load_reference_data(self, reference_filename):
        with open(os.path.join(self.pathToReference, reference_filename)) as f:
            return json.loads(f.read())

    def load_reference_text(self, reference_filename):
        with open(os.path.join(self.pathToReference, reference_filename), 'r',
                  encoding="utf-8") as f:
            return f.read().replace('\n', '').replace("\\'", '\'')

    def reading_test(self, data_filename):
        metadata_filename = os.path.join(self.pathToMetadata, "metadata.xml")
        dataset = get_datasets(os.path.join(self.pathToDB, data_filename),
                               metadata_filename)
        reference = pd.read_json(os.path.join(self.pathToReference, "df.json"),
                                 orient='records').astype('str')
        dataframe: pd.DataFrame = dataset.data.astype('str')
        pd.testing.assert_frame_equal(dataframe.fillna('').replace('nan', ''),
                                      reference.replace('nan', ''),
                                      check_like=True)

    def semantic_test(self, sqlite_db, sqlite_filename, limit, meta_file,
                      reference_filename):
        dataset = self.load_input_data(sqlite_db, sqlite_filename, limit,
                                       meta_file)
        errors = dataset.semantic_validation()
        reference_dict = self.load_reference_data(reference_filename)
        self.assert_equal_validation(
            json.loads(json.dumps(errors).replace("NaN", 'null')),
            reference_dict)

    def semantic_valid_test(self, sqlite_db, sqlite_filename, limit,
                            pkl_filename):
        dataset = self.load_input_data(sqlite_db, sqlite_filename, limit,
                                       pkl_filename)
        errors = dataset.semantic_validation()
        self.assert_equal_validation(errors, [])

    def metadata_test(self, reference_filename, path_to_data):
        obj_ = read_sdmx(os.path.join(self.pathToMetadata, path_to_data),
                         validate=False)
        reference = self.load_reference_data(reference_filename)
        errors = obj_.payload.errors
        if errors is None:
            errors = []
        self.assert_equal_validation(errors, reference)

    def metadata_valid_test(self, path_to_data):
        obj_ = _read_xml(os.path.join(self.pathToMetadata, path_to_data))
        if isinstance(obj_, MetadataType):
            _set_references(obj_)
        errors = obj_.structures.errors
        if errors is None:
            errors = []
        self.assert_equal_validation(errors, [])

    def metadata_compare(self, reference_filename, data_filename, dsd_name):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))
        content = {'content': obj_.content,
                   'items': obj_.payload.dsds[dsd_name].content,
                   'representation': obj_.payload.dsds[
                       dsd_name].measure_descriptor.components[
                       'OBS_VALUE'].representation,
                   'errors': obj_.payload.errors}

        self.assertEqual(f'{content}',
                         self.load_reference_text(reference_filename))

    def metadata_equality(self, data_filename):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))
        obj_2 = read_sdmx(os.path.join(self.pathToDB, data_filename))

        self.assertEqual(obj_2 == obj_, True)

    def metadata_inequality(self):
        obj_ = read_sdmx(os.path.join(self.pathToDB, 'bis.xml'))
        obj_2 = read_sdmx(os.path.join(self.pathToDB, 'wb.xml'))

        self.assertEqual(obj_2 != obj_, True)

    def datasets_validation(self, data_filename, metadata_filename,
                            reference_filename=None):
        dataset = get_datasets(os.path.join(self.pathToDB, data_filename),
                               os.path.join(self.pathToMetadata,
                                            metadata_filename))
        if reference_filename is None:
            self.assertEqual(dataset.semantic_validation(), [])
        else:
            reference_dict = self.load_reference_data(reference_filename)
            self.assert_equal_validation(json.loads(
                json.dumps(dataset.semantic_validation()).replace("NaN",
                                                                  'null')),
                reference_dict)

    def header_writing(self, reference_filename):
        obj_ = Message(message_type=MessageTypeEnum.Metadata, payload={})

        result = obj_.to_xml('', prepared=datetime.fromisoformat(
            '2021-04-08T17:27:28'), prettyprint=False).getvalue()

        self.assertEqual(result, self.load_reference_text(reference_filename))

    def data_writing(self, dtype: MessageTypeEnum, series=False):
        message = read_sdmx(os.path.join(self.pathToMetadata, 'bis.xml'))
        path = os.path.join(self.pathToDB, "df.json")
        dataset = Dataset(data=pd.read_json(path, orient='records'),
                          structure=message.payload.dsds['BIS:BIS_DER(1.0)'])

        dataset.data = dataset.data.astype('str')

        if series:
            dataset.set_dimension_at_observation('TIME_PERIOD')

        result = dataset.to_xml(dtype, '', prepared=datetime.fromisoformat(
            '2000-01-01T00:00:01'), prettyprint=False).getvalue()

        df = first_element_dict(
            get_pandas_df(BytesIO(bytes(result, encoding='UTF-8'))))

        pd.testing.assert_frame_equal(
            df.fillna('').replace('nan', ''),
            dataset.data.replace('nan', ''),
            check_like=True)

    def metadata_agency_scheme_writing(self, reference_filename,
                                       data_filename):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))

        result = obj_.payload.organisations. \
            _parse_XML(indent='', label='str:AgencyScheme')

        self.assertEqual(result, self.load_reference_text(reference_filename))

    def metadata_codelist_writing(self, reference_filename, data_filename,
                                  codelist_name):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))

        result = obj_.payload.codelists[codelist_name]. \
            _parse_XML(indent='', label='str:Codelist')

        self.assertEqual(result, self.load_reference_text(reference_filename))

    def metadata_concept_writing(self, reference_filename, data_filename,
                                 concept_name):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))

        result = obj_.payload.concepts[concept_name] \
            ._parse_XML(indent='', label='str:ConceptScheme')

        self.assertEqual(result, self.load_reference_text(reference_filename))

    def metadata_constraint_writing(self, reference_filename, data_filename):
        obj_ = read_xml(os.path.join(self.pathToDB, data_filename),
                        validate=True)

        result = first_element_dict(obj_['Constraints'])._parse_XML(
            indent='', label='str:ContentConstraint')

        self.assertEqual(result, self.load_reference_text(reference_filename))

    def metadata_dataflow_writing(self, reference_filename, data_filename,
                                  dataflow_name):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))

        result = obj_.payload.dataflows[dataflow_name]. \
            _parse_XML(indent='', label='str:Dataflow')

        self.assertEqual(result, self.load_reference_text(reference_filename))

    def metadata_dsd_writing(self, reference_filename, data_filename,
                             dsd_name):
        obj_ = read_sdmx(os.path.join(self.pathToDB, data_filename))

        result = obj_.payload.dsds[dsd_name]. \
            _parse_XML(indent='', label='str:DataStructure')

        self.assertEqual(result.replace('\n', ''),
                         self.load_reference_text(reference_filename))

    def read_sdmx_data(self, data_filename):
        message = read_sdmx(os.path.join(self.pathToDB, data_filename))
        reference = pd.read_json(
            os.path.join(self.pathToReference, "df.json"),
            orient='records').astype('str')
        dataframe: pd.DataFrame = message.payload['BIS_DER'].data.astype('str')
        pd.testing.assert_frame_equal(
            dataframe.fillna('').replace('nan', ''),
            reference.replace('nan', ''),
            check_like=True)

    def get_pandas_df_data(self, data_filename):
        dict_dataframe = get_pandas_df(
            os.path.join(self.pathToDB, data_filename))
        reference = pd.read_json(
            os.path.join(self.pathToReference, "df.json"),
            orient='records').astype('str')
        dataframe: pd.DataFrame = dict_dataframe['BIS:BIS_DER(1.0)'].astype(
            'str')
        pd.testing.assert_frame_equal(
            dataframe.fillna('').replace('nan', ''),
            reference.replace('nan', ''),
            check_like=True)

    def xml_to_csv_data(self, data_filename):
        text_csv = xml_to_csv(os.path.join(self.pathToDB, data_filename),
                              sep=',', encoding='utf-8', index=False,
                              header=True)
        dataframe = pd.read_csv(StringIO(text_csv)).astype('str')
        reference = pd.read_json(
            os.path.join(self.pathToReference, "df.json"),
            orient='records').astype('str')
        pd.testing.assert_frame_equal(
            dataframe.fillna('').replace('nan', ''),
            reference.replace('nan', ''),
            check_like=True)

    def assert_equal_validation(self, result, reference):
        if len(result) == len(reference):
            self.assertCountEqual(result, reference)
        else:
            self.assertEqual(result, reference)


if __name__ == '__main__':
    pass
