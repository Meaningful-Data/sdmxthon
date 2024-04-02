import os
from pathlib import Path

from pytest import mark

from sdmxthon import Dataset
from sdmxthon.api.api import read_sdmx
from sdmxthon.model.definitions import DataStructureDefinition, DataFlowDefinition
from sdmxthon.model.itemScheme import AgencyScheme, Codelist, ConceptScheme
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


def test_msg_get_organisationSchemes(metadata_path):
    metadata_filename = 'metadata.xml'
    message = read_sdmx(os.path.join(metadata_path, metadata_filename))
    assert message is not None
    organisationSchemes = message.get_organisationschemes()
    assert isinstance(organisationSchemes, (dict, AgencyScheme))
    if isinstance(organisationSchemes, dict):
        uid = first_element_dict(organisationSchemes).unique_id
    else:
        uid = organisationSchemes.unique_id
    organisationScheme = message.get_organisationscheme_by_uid(uid)
    assert isinstance(organisationScheme, AgencyScheme)


def test_msg_get_codelists(metadata_path):
    metadata_filename = 'metadata.xml'
    message = read_sdmx(os.path.join(metadata_path, metadata_filename))
    assert message is not None
    codelists = message.get_codelists()
    assert isinstance(codelists, (dict, Codelist))
    if isinstance(codelists, dict):
        uid = first_element_dict(codelists).unique_id
    else:
        uid = codelists.unique_id
    codelist = message.get_codelist_by_uid(uid)
    assert isinstance(codelist, Codelist)


def test_msg_get_concepts(metadata_path):
    metadata_filename = 'metadata.xml'
    message = read_sdmx(os.path.join(metadata_path, metadata_filename))
    assert message is not None
    concepts = message.get_concepts()
    assert isinstance(concepts, (dict, ConceptScheme))
    if isinstance(concepts, dict):
        uid = first_element_dict(concepts).unique_id
    else:
        uid = concepts.unique_id
    concept = message.get_concept_by_uid(uid)
    assert isinstance(concept, ConceptScheme)


def test_msg_get_datastructures(metadata_path):
    metadata_filename = 'metadata.xml'
    message = read_sdmx(os.path.join(metadata_path, metadata_filename))
    assert message is not None
    datastructures = message.get_datastructures()
    assert isinstance(datastructures, (dict, DataStructureDefinition))
    if isinstance(datastructures, dict):
        uid = first_element_dict(datastructures).unique_id
    else:
        uid = datastructures.unique_id
    datastructure = message.get_datastructure_by_uid(uid)
    assert isinstance(datastructure, DataStructureDefinition)


def test_msg_get_dataflows(metadata_path):
    metadata_filename = 'metadata.xml'
    message = read_sdmx(os.path.join(metadata_path, metadata_filename))
    assert message is not None
    dataflows = message.get_dataflows()
    assert isinstance(dataflows, (dict, DataFlowDefinition))
    if isinstance(dataflows, dict):
        uid = first_element_dict(dataflows).unique_id
    else:
        uid = dataflows.unique_id
    dataflow = message.get_dataflow_by_uid(uid)
    assert isinstance(dataflow, DataFlowDefinition)

def test_msg_get_datasets(data_path):
    data_filename = 'dataflow.xml'
    message = read_sdmx(os.path.join(data_path, data_filename))
    assert message is not None
    datasets = message.get_datasets()
    assert isinstance(datasets, (dict, Dataset))
    if isinstance(datasets, dict):
        uid = first_element_dict(datasets).unique_id
    else:
        uid = datasets.unique_id
    dataset = message.get_dataset_by_uid(uid)
    assert isinstance(dataset, Dataset)

