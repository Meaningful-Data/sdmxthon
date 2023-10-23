"""
API methods Tests
"""
import os
from io import StringIO
from pathlib import Path

import pandas as pd
import pytest
from pytest import mark

from sdmxthon.api.api import read_sdmx, get_pandas_df, xml_to_csv

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
    dataframe: pd.DataFrame = dict_dataframe[key].astype('str')
    assert_with_reference(dataframe, reference_path)


# Test: xml to csv
@mark.parametrize("filename", filenames)
def test_xml_to_csv(filename, data_path, reference_path):
    text_csv = xml_to_csv(os.path.join(data_path, filename),
                          sep=',', encoding='utf-8', index=False,
                          header=True)
    dataframe = pd.read_csv(StringIO(text_csv)).astype('str')
    assert_with_reference(dataframe, reference_path)
