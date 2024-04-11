import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.message import Message
from sdmxthon.utils.handlers import first_element_dict

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


filename = [
    "gen_ser.xml", "ecb.xml", "ilo.xml", "oecd.xml",
]


@mark.parametrize("data_filename", filename)
def test_metadata_from_ws(data_filename, data_path):
    message = read_sdmx(os.path.join(data_path, data_filename))
    structure = first_element_dict(message.payload).structure
    dataflow = first_element_dict(message.payload).dataflow
    assert structure is not None or dataflow is not None
