import os
from datetime import datetime

import pytest

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.message import Message
from sdmxthon.utils.enums import MessageTypeEnum


# Fixture to provide file paths
def file_reader(subdirectory):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, subdirectory, "data"),
                            "data_sample")
    pathToReference = os.path.join(os.path.join(path, subdirectory, "data"),
                                   "reference")
    return pathToDB, pathToReference


# Load reference text from a file
def load_reference_text(reference_filename, pathToReference):
    with open(os.path.join(pathToReference, reference_filename), 'r',
              encoding="utf-8") as f:
        return f.read().replace('\n', '').replace("\\'", '\'')


# Extract and compare metadata
def compare_metadata(reference_filename, data_filename, metadata_key,
                     metadata_name, pathToDB, pathToReference,
                     label_key):
    obj_ = read_sdmx(os.path.join(pathToDB, data_filename))
    result = obj_.payload[metadata_key][metadata_name]._parse_XML(indent='',
                                                                  label=label_key)

    expected_result = load_reference_text(reference_filename, pathToReference)
    return expected_result, result


# Defines the parameters for parameterization
codelists_params = [
    ('bis.xml', 'bis.txt', 'BIS:CL_AVAILABILITY(1.0)'),
    ('estat.xml', 'estat.txt', 'ESTAT:FREQ(1.5)'),
    ('imf.xml', 'imf.txt', 'IMF:CL_ALT_FISCAL_INDICATOR(1.0)'),
    ('wb.xml', 'wb.txt', 'WB:CL_REF_AREA_WDI(1.0)')]

concepts_params = [
    ('bis.xml', 'bis.txt', 'BIS:BIS_CONCEPT_SCHEME(1.0)'),
    ('estat.xml', 'estat.txt', 'ESTAT:HLTH_RS_PRSHP1(7.0)'),
    ('imf.xml', 'imf.txt', 'IMF:ECOFIN_CONCEPTS(1.0)'),
    ('wb.xml', 'wb.txt', 'WB:WDI_CONCEPT(1.0)')]

dsd_params = [
    ('bis.xml', 'bis.txt', 'BIS:BIS_DER(1.0)'),
    ('estat.xml', 'estat.txt', 'ESTAT:HLTH_RS_PRSHP1(7.0)'),
    ('imf.xml', 'imf.txt', 'IMF:ALT_FISCAL_DSD(1.0)'),
    ('wb.xml', 'wb.txt', 'WB:WDI(1.0)')]

constraints_params = [
    ('cube.xml', 'cube.txt', 'MD:Test_cube(1.0)'),
    ('series.xml', 'series.txt', 'MD:Test_series(1.0)')]

organisations_params = [
    ('bis.xml', 'bis.txt', 'SDMX:AGENCIES(1.0)'),
    ('imf.xml', 'imf.txt', 'SDMX:AGENCIES(1.0)')]


# Parametrized test functions
@pytest.mark.parametrize("data_filename, reference_filename, metadata_name",
                         codelists_params)
def test_codelists_comparison(data_filename, reference_filename, metadata_name):
    metadata_key, label_key = 'Codelists', 'str:Codelist'
    path_to_db, path_to_reference = file_reader("Codelist")
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        path_to_db, path_to_reference, label_key)
    assert expected_result == result


@pytest.mark.parametrize("data_filename, reference_filename, metadata_name",
                         concepts_params)
def test_concepts_comparison(data_filename, reference_filename, metadata_name):
    metadata_key, label_key = 'Concepts', 'str:ConceptScheme'
    path_to_db, path_to_reference = file_reader("Concept")
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        path_to_db, path_to_reference, label_key)
    assert expected_result == result


@pytest.mark.parametrize("data_filename, reference_filename, metadata_name",
                         dsd_params)
def test_dsd_comparison(data_filename, reference_filename, metadata_name):
    metadata_key, label_key = 'DataStructures', 'str:DataStructure'
    path_to_db, path_to_reference = file_reader("DataStructureDefinition")
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        path_to_db, path_to_reference, label_key)
    assert expected_result == result


@pytest.mark.parametrize("data_filename, reference_filename, metadata_name",
                         constraints_params)
def test_constraint_comparison(data_filename, reference_filename,
                               metadata_name):
    metadata_key, label_key = 'Constraints', 'str:ContentConstraint'
    path_to_db, path_to_reference = file_reader("Constraint")
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        path_to_db, path_to_reference, label_key)
    assert expected_result == result


@pytest.mark.parametrize("data_filename, reference_filename, metadata_name",
                         organisations_params)
def test_agency_scheme_comparison(data_filename, reference_filename,
                                  metadata_name):
    metadata_key, label_key = 'OrganisationSchemes', 'str:AgencyScheme'
    path_to_db, path_to_reference = file_reader("Organisations")
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        path_to_db, path_to_reference, label_key)
    assert expected_result == result


# Extract header and compare with reference
def header_writing(reference_filename, pathToReference):
    obj_ = Message(message_type=MessageTypeEnum.Metadata, payload={})
    result = obj_.to_xml('',
                         prepared=datetime.fromisoformat('2021-04-08T17:27:28'),
                         prettyprint=False)
    expected_result = load_reference_text(reference_filename, pathToReference)
    return expected_result, result


# Parameterized test for comparing header data

header_params = [('header_test.xml', 'header.txt')]


@pytest.mark.parametrize("data_filename, reference_filename", header_params)
# General test function for comparing header data
def test_header_comparison(data_filename, reference_filename):
    path_to_db, path_to_reference = file_reader("Header")
    expected_result, result = header_writing(reference_filename,
                                             path_to_reference)
    assert expected_result == result
