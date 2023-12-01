import os
from datetime import datetime
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.header import Header
from sdmxthon.parsers.writer_aux import write_from_header
from sdmxthon.utils.enums import MessageTypeEnum


# Load reference text from a file
def load_reference_text(reference_filename, pathToReference):
    with open(os.path.join(pathToReference, reference_filename), 'r',
              encoding="utf-8") as f:
        reference_text = f.read()
    return reference_text


# Extract and compare metadata
def compare_metadata(reference_filename, data_filename, metadata_key,
                     metadata_name, data_path, reference_path,
                     label_key):
    obj_ = read_sdmx(os.path.join(data_path, data_filename))
    metadata_obj = obj_.payload[metadata_key][metadata_name]
    if hasattr(metadata_obj, 'to_xml'):
        prepared = datetime.fromisoformat('2021-04-08T17:27:28')
        result = metadata_obj.to_xml(prettyprint=True, prepared=prepared)
    else:
        result = metadata_obj._parse_XML(indent='', label=label_key)

    expected_result = load_reference_text(reference_filename, reference_path)
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

dataflows_params = [
    ('bis.xml', 'bis.txt', 'BIS:WEBSTATS_DER_DATAFLOW(1.0)'),
]

constraints_params = [
    ('cube.xml', 'cube.txt', 'MD:Test_cube(1.0)'),
    ('series.xml', 'series.txt', 'MD:Test_series(1.0)')]

organisations_params = [
    ('bis.xml', 'bis.txt', 'SDMX:AGENCIES(1.0)'),
    ('imf.xml', 'imf.txt', 'SDMX:AGENCIES(1.0)')]


# Parametrized test functions with custom input path
@mark.input_path(Path(__file__).parent / "Codelist" / "data")
@mark.parametrize("data_filename, reference_filename, metadata_name",
                  codelists_params)
def test_codelists_comparison(data_filename, reference_filename, metadata_name,
                              data_path, reference_path):
    metadata_key, label_key = 'Codelists', 'str:Codelist'
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        data_path, reference_path, label_key)
    assert expected_result == result


@mark.input_path(Path(__file__).parent / "Concept" / "data")
@mark.parametrize("data_filename, reference_filename, metadata_name",
                  concepts_params)
def test_concepts_comparison(data_filename, reference_filename, metadata_name,
                             data_path, reference_path):
    metadata_key, label_key = 'Concepts', 'str:ConceptScheme'
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        data_path, reference_path, label_key)
    assert expected_result == result


@mark.input_path(Path(__file__).parent / "DataStructureDefinition" / "data")
@mark.parametrize("data_filename, reference_filename, metadata_name",
                  dsd_params)
def test_dsd_comparison(data_filename, reference_filename, metadata_name,
                        data_path, reference_path):
    metadata_key, label_key = 'DataStructures', 'str:DataStructure'
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        data_path, reference_path, label_key)
    assert expected_result == result


@mark.input_path(Path(__file__).parent / "DataFlow" / "data")
@mark.parametrize("data_filename, reference_filename, metadata_name",
                  dataflows_params)
def test_dataflow_comparison(data_filename, reference_filename, metadata_name,
                             data_path, reference_path):
    metadata_key, label_key = 'Dataflows', 'str:DataFlow'
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        data_path, reference_path, label_key)
    assert expected_result == result


@mark.input_path(Path(__file__).parent / "Constraint" / "data")
@mark.parametrize("data_filename, reference_filename, metadata_name",
                  constraints_params)
def test_constraint_comparison(data_filename, reference_filename,
                               metadata_name, data_path, reference_path):
    metadata_key, label_key = 'Constraints', 'str:ContentConstraint'
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        data_path, reference_path, label_key)
    assert expected_result == result


@mark.input_path(Path(__file__).parent / "Organisations" / "data")
@mark.parametrize("data_filename, reference_filename, metadata_name",
                  organisations_params)
def test_agency_scheme_comparison(data_filename, reference_filename,
                                  metadata_name, data_path, reference_path):
    metadata_key, label_key = 'OrganisationSchemes', 'str:AgencyScheme'
    expected_result, result = compare_metadata(
        reference_filename, data_filename, metadata_key, metadata_name,
        data_path, reference_path, label_key)
    assert expected_result == result


# Parameterized test for comparing header data
header_params = [('header_test.xml', 'header.txt')]


@mark.input_path(Path(__file__).parent / "Header" / "data")
@mark.parametrize("data_filename, reference_filename", header_params)
# General test function for comparing header data
def test_header_comparison(data_filename, reference_filename, reference_path):
    header = Header(Prepared=datetime.fromisoformat('2021-04-08T17:27:28'))
    result = write_from_header(header, prettyprint=False,
                               type_=MessageTypeEnum.Metadata)
    expected_result = load_reference_text(reference_filename, reference_path)
    assert expected_result == result
