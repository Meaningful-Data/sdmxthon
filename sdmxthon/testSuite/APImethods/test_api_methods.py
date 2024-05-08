"""
API methods Tests
"""
import os
from io import StringIO
from pathlib import Path

import pandas as pd
import pytest
from pytest import mark
from requests.exceptions import ConnectionError

from sdmxthon.api.api import get_pandas_df, read_sdmx, upload_metadata_to_fmr, \
    xml_to_csv, get_datasets

pytestmark = pytest.mark.input_path(Path(__file__).parent / "data")


def assert_with_reference(dataframe, reference_path):
    reference = pd.read_json(os.path.join(reference_path, "df.json"),
                             orient='records').astype('str')

    pd.testing.assert_frame_equal(
        dataframe.fillna('').replace('nan', ''),
        reference.replace('nan', ''),
        check_like=True)


filenames = ["gen_all.xml", "gen_ser.xml", "str_all.xml", "str_ser.xml"]


# Test: Read sdmx (data files)
@mark.parametrize("filename", filenames)
def test_read_sdmx(filename, data_path, reference_path):
    message = read_sdmx(os.path.join(data_path, filename))
    key = 'BIS:BIS_DER(1.0)'
    dataframe: pd.DataFrame = message.payload[key].data.astype('str')
    assert_with_reference(dataframe, reference_path)


# Test: Get pandas df
@mark.parametrize("filename", filenames)
def test_get_pandas_df(filename, data_path, reference_path):
    dict_dataframe = get_pandas_df(os.path.join(data_path, filename))
    key = 'BIS:BIS_DER(1.0)'
    if key not in dict_dataframe:
        raise AssertionError(f"Key {key} not found in result")
    dataframe: pd.DataFrame = dict_dataframe[key].astype('str')
    assert_with_reference(dataframe, reference_path)


@mark.parametrize("filename", filenames)
def test_use_dataset_id(filename, data_path, reference_path):
    dict_dataframe = get_pandas_df(os.path.join(data_path, filename),
                                   use_dataset_id=True)
    key = 'TEST_KEY'
    assert key in dict_dataframe
    dict_dataframe = read_sdmx(os.path.join(data_path, filename),
                               use_dataset_id=True)
    assert key in dict_dataframe.content


# Test: xml to csv
@mark.parametrize("filename", filenames)
def test_xml_to_csv(filename, data_path, reference_path):
    text_csv = xml_to_csv(os.path.join(data_path, filename),
                          sep=',', encoding='utf-8', index=False,
                          header=True)
    dataframe = pd.read_csv(StringIO(text_csv)).astype('str')
    assert_with_reference(dataframe, reference_path)


metadata_filenames = ["metadata.xml"]


@mark.parametrize("filename", metadata_filenames)
def test_upload_metadata_to_fmr(filename, metadata_path):
    file_path = os.path.join(metadata_path, filename)
    try:
        upload_metadata_to_fmr(file_path)
    except ConnectionError as e:
        assert e.args[0] == ('Unable to connect to FMR '
                             'at http://localhost:8080')
    except Exception as e:
        assert e.args[1] == 304
        assert e.args[2] == ('Either no structures were submitted, '
                             'or the submitted structures contain '
                             'no changes from the ones currently '
                             'stored in the system')


csv_filenames = ["data_v1.csv", "data_v2.csv"]


# Test: Get pandas df with SDMX-CSV
@mark.parametrize("csv_filename", csv_filenames)
def test_get_pandas_df_with_sdmx_csv(data_path, csv_filename):
    dict_dataframe = get_pandas_df(os.path.join(data_path, csv_filename))
    key = 'BIS:BIS_DER(1.0)'
    assert key in dict_dataframe, f"Key {key} not found in result"
    dataframe = dict_dataframe[key].astype('str')
    assert dataframe.shape == (1000, 20), ('The Dataframe does not have '
                                           'the expected shape')
