import os

import pytest

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.message import Message


# Fixture to provide the path to the data files
@pytest.fixture
def file_reader():
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    return pathToDB


# Test reading and validation of SDMX files
@pytest.mark.parametrize("filename", ['gen_all.xml', 'gen_ser.xml',
                                      'str_all.xml', 'str_ser.xml'])
def test_reading_validation(file_reader, filename):
    file_path = os.path.join(file_reader, filename)
    result = read_sdmx(file_path, validate=True)
    assert result is not None
    data = result.content['BIS:BIS_DER(1.0)'].data
    num_rows = len(data)
    num_columns = data.shape[1]
    assert num_rows > 0
    assert num_columns > 0
    expected_num_rows = 1000
    expected_num_columns = 20
    assert num_rows == expected_num_rows
    assert num_columns == expected_num_columns


# Test reading of dataflow SDMX file
def test_dataflow(file_reader):
    filename = 'dataflow.xml'
    file_path = os.path.join(file_reader, filename)
    result = read_sdmx(file_path, validate=True)
    data_dataflow = result.content['BIS:WEBSTATS_DER_DATAFLOW(1.0)'].data
    num_rows = len(data_dataflow)
    num_columns = data_dataflow.shape[1]
    assert isinstance(result, Message)
    assert num_rows > 0
    assert num_columns > 0
    expected_num_rows = 1000
    expected_num_columns = 20
    assert num_rows == expected_num_rows
    assert num_columns == expected_num_columns
    assert 'BIS:WEBSTATS_DER_DATAFLOW(1.0)' in result.content
    assert 'AVAILABILITY' in data_dataflow.columns
    assert 'DER_CURR_LEG1' in data_dataflow.columns
