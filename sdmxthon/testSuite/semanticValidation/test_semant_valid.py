import os

import pytest

from sdmxthon.api.api import read_sdmx

# Mapping of test names to corresponding DSD identifiers
dsd_map = {
    'test_correct': 'BIS:BIS_DER(1.0)',
    'test_metadata_errors': 'MD:DS1(1.0)',
    'test_metadata_valid': 'MD:DS1(1.0)',
    'test_valid': 'BIS:BIS_DER(1.0)'
}


# Fixture for setting up the file paths
@pytest.fixture
def file_reader_fixture():
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToMetadata = os.path.join(os.path.join(path, "data"), "metadata")
    file_dataset = 'str_all.xml'
    file_path = os.path.join(pathToDB, file_dataset)
    return file_path, pathToMetadata


# Function to read and validate an SDMX file
def read_and_validate(file_path):
    result = read_sdmx(file_path, validate=True)
    return result


# Function to get the dataset from the SDMX result
def get_dataset(file_path):
    result_dataset = read_and_validate(file_path)
    dataset = result_dataset.payload['BIS:BIS_DER(1.0)']
    return dataset


# Function to set up the dataset and metadata for testing
def setup_dataset_and_metadata(file_reader_fixture, test_name, metadata_file):
    path, pathToMetadata = file_reader_fixture
    dataset = get_dataset(path)
    file_path_metadata = os.path.join(pathToMetadata, metadata_file)
    result_metadata = read_and_validate(file_path_metadata)
    dsd = result_metadata.content['DataStructures'][dsd_map[test_name]]
    dataset.structure = dsd
    return dataset


# Test: Correct dataset should have no semantic validation errors
def test_correct(file_reader_fixture):
    dataset = setup_dataset_and_metadata(file_reader_fixture, 'test_correct',
                                         'metadata.xml')
    assert len(dataset.semantic_validation()) == 0


# Test: Compare captured metadata errors with expected message
def test_metadata_errors(file_reader_fixture):
    try:
        setup_dataset_and_metadata(file_reader_fixture, 'test_metadata_errors',
                                   'metadata_errors.xml')
    except Exception as e:
        captured_error = str(e)

        # Compare the complete error message
        expected_error = (
            "Element 'Ref', attribute 'id': The value 'TEST_ERROR' does not match the fixed value constraint "
            "'OBS_VALUE'.;\n"
            "Element '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}DataStructure': Duplicate "
            "key-sequence ['DS2', 'MD', '1.0'] in unique identity-constraint '{"
            "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}UniqueDataStructure'."
        )
        assert captured_error == expected_error, f"Unexpected error: {captured_error}"


# Test: Metadata should be valid, checking for specific error codes
def test_metadata_valid(file_reader_fixture):
    dataset = setup_dataset_and_metadata(file_reader_fixture,
                                         'test_metadata_valid',
                                         'metadata_valid.xml')
    validation_errors = dataset.semantic_validation()

    error_code_count = {}
    for error in validation_errors:
        error_code = error['Code']
        error_code_count[error_code] = error_code_count.get(error_code, 0) + 1

    ss01_code_occurrences = error_code_count.get('SS01', 0)
    ss07_code_occurrences = error_code_count.get('SS07', 0)
    assert ss01_code_occurrences == 2
    assert ss07_code_occurrences == 28


# Test: Validation error should occur when DSD is not found
def test_nodsd(file_reader_fixture):
    path, pathToMetadata = file_reader_fixture
    file_test_nods = 'test_nodsd.xml'
    file_path_test_nodsd = os.path.join(pathToMetadata, file_test_nods)
    result_test_nodsd = read_sdmx(file_path_test_nodsd, validate=False)
    validation_errors = result_test_nodsd.content['errors']
    expected_errors = [
        {'Code': 'MS01',
         'ErrorLevel': 'CRITICAL',
         'Message': 'Not found any DSD in this file',
         'ObjectID': None,
         'ObjectType': 'DSD'}]
    assert validation_errors == expected_errors


# Test: Valid dataset should have no semantic validation errors
def test_valid(file_reader_fixture):
    dataset = setup_dataset_and_metadata(file_reader_fixture, 'test_valid',
                                         'test_valid.xml')
    assert len(dataset.semantic_validation()) == 0
