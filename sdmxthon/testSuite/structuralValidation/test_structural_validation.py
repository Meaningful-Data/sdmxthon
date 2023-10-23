import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx, get_datasets
from sdmxthon.model.dataset import Dataset
from sdmxthon.utils.handlers import first_element_dict

pytestmark = mark.input_path(Path(__file__).parent / "data")


# Function to set up the dataset and metadata for testing
def get_test_dataset(data_path, metadata_path, metadata_file):
    dataset = get_datasets(os.path.join(data_path, "data.xml"),
                           os.path.join(metadata_path, metadata_file))
    return dataset


# Test: Correct dataset should have no semantic validation errors
@mark.parametrize("filename", ['metadata.xml', 'test_valid.xml'])
def test_correct(data_path, metadata_path, filename):
    dataset: Dataset = get_test_dataset(data_path, metadata_path,
                                        filename)
    assert len(dataset.structural_validation()) == 0


# Test: Compare captured metadata errors with expected message
def test_metadata_errors(data_path, metadata_path):
    try:
        get_test_dataset(data_path, metadata_path,
                         'metadata_errors.xml')
    except Exception as e:
        elements = e.args[0].splitlines()
        elements = sorted(elements)

        assert "TEST_ERROR" in elements[0]
        assert "Duplicate key-sequence" in elements[1]


# Test: Checking for specific error codes (using custom structure)
def test_metadata_valid(data_path, metadata_path):
    content = read_sdmx(os.path.join(data_path, 'data.xml')).content
    dataset = first_element_dict(content)
    metadata = read_sdmx(os.path.join(metadata_path, 'metadata_valid.xml'))
    dataset.structure = metadata.content['DataStructures']['MD:DS1(1.0)']

    validation_errors = dataset.structural_validation()

    error_code_count = {}
    for error in validation_errors:
        error_code = error['Code']
        if error_code in error_code_count:
            error_code_count[error_code] += 1
        else:
            error_code_count[error_code] = 1

    ss01_code_occurrences = error_code_count.get('SS01', 0)
    ss07_code_occurrences = error_code_count.get('SS07', 0)
    assert ss01_code_occurrences == 2
    assert ss07_code_occurrences == 28


# Test: Validation error should occur when DSD is not found
def test_nodsd(data_path, metadata_path):
    file_path_test_nodsd = os.path.join(metadata_path, 'test_nodsd.xml')
    result_test_nodsd = read_sdmx(file_path_test_nodsd, validate=False)
    validation_errors = result_test_nodsd.content['errors']
    expected_errors = [
        {'Code': 'MS01',
         'ErrorLevel': 'CRITICAL',
         'Message': 'Not found any DSD in this file',
         'ObjectID': None,
         'ObjectType': 'DSD'}]
    assert validation_errors == expected_errors
