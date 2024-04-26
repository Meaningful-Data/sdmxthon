import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.message import Message

pytestmark = mark.input_path(Path(__file__).parent / "data")


# Test reading and validation of SDMX files
@mark.parametrize("filename", ['gen_all.xml', 'gen_ser.xml',
                               'str_all.xml', 'str_ser.xml',
                               'str_ser_group.xml',
                               'data_v1.csv', 'data_v2.csv'])
def test_reading_validation(data_path, filename):
    file_path = os.path.join(data_path, filename)
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
def test_dataflow(data_path):
    filename = 'dataflow.xml'
    file_path = os.path.join(data_path, filename)
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


# Test reading of dataflow SDMX file from URL (KeyError: 'Obs')

def test_reading_missing_obs_key():
    # SDMX file URL
    url = 'https://stats.bis.org/api/v1/data/WS_CPMI_PARTICIPANTS/all/all'
    result = read_sdmx(url, validate=True)
    data = result.content['BIS:WS_CPMI_PARTICIPANTS(1.0)'].data
    num_rows = len(data)
    num_columns = data.shape[1]
    assert isinstance(result, Message)
    assert num_rows > 0
    assert num_columns > 0


# Test reading of dataflow SDMX file from URL
def test_reading_with_dataflow():
    # SDMX file URL
    url = 'https://stats.bis.org/api/v1/data/WS_CBPOL_D/all/all'
    result = read_sdmx(url, validate=True)
    data = result.content['BIS:WS_CBPOL_D(1.0)'].data
    structure_type = result.content['BIS:WS_CBPOL_D(1.0)'].structure_type
    num_rows = len(data)
    num_columns = data.shape[1]
    assert isinstance(result, Message)
    assert num_rows > 0
    assert num_columns > 0
    assert structure_type == 'dataflow'


# Test reading of dataflow SDMX file from URL (structure_type: 'datastructure')
def test_reading_structure_type_datastructure():
    # SDMX file URL
    url = 'https://data-api.ecb.europa.eu/service/data/AME/all/all'
    result = read_sdmx(url, validate=True)
    data = result.content['ECB:ECB_AME1(1.0)'].data
    structure_type = result.content['ECB:ECB_AME1(1.0)'].structure_type
    num_rows = len(data)
    num_columns = data.shape[1]
    assert isinstance(result, Message)
    assert num_rows > 0
    assert num_columns > 0
    assert structure_type == 'datastructure'
