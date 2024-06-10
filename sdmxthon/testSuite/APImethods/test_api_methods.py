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
    xml_to_csv
from sdmxthon.utils.handlers import first_element_dict
from sdmxthon.model.message import Message

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
    dataframe: pd.DataFrame = message.payload.data.astype('str')
    assert_with_reference(dataframe, reference_path)


# Test: Get pandas df
@mark.parametrize("filename", filenames)
def test_get_pandas_df(filename, data_path, reference_path):
    dataframe_dict = get_pandas_df(os.path.join(data_path, filename))
    dataframe: pd.DataFrame = first_element_dict(dataframe_dict).astype('str')
    assert_with_reference(dataframe, reference_path)


@mark.parametrize("filename", filenames)
def test_use_dataset_id(filename, data_path, reference_path):
    dict_dataframe = get_pandas_df(os.path.join(data_path, filename),
                                   use_dataset_id=True)
    key = 'TEST_KEY'
    assert key in dict_dataframe
    message = read_sdmx(os.path.join(data_path, filename),
                        use_dataset_id=True)
    assert key in message.content['datasets']


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


urls = [
         ("https://data-api.ecb.europa.eu/service/data/AME/all/all",
          "https://data-api.ecb.europa.eu/service/datastructure/all/ECB_AME1/latest"),
         ("https://data-api.ecb.europa.eu/service/data/PDD/all/all",
          "https://data-api.ecb.europa.eu/service/datastructure/all/ECB_PAY3/latest"),
         ("https://data-api.ecb.europa.eu/service/data/JDF_PSS_PAYMENTS_N_NEA/all/all",
          "https://data-api.ecb.europa.eu/service/datastructure/all/ECB_PSS1/latest"),
         # data and metadata (DataStructures) urls from European Central Bank (ECB)
         ("https://stats.bis.org/api/v1/data/WS_CPMI_PARTICIP/all/all",
          "https://stats.bis.org/api/v1/dataflow/all/WS_CPMI_PARTICIP/latest"),
         ("https://stats.bis.org/api/v1/data/WS_CPP/all/all",
          "https://stats.bis.org/api/v1/dataflow/all/WS_CPP/latest"),
         ("https://stats.bis.org/api/v1/data/WS_LONG_CPI/all/all",
          "https://stats.bis.org/api/v1/dataflow/all/WS_LONG_CPI/latest"),
         # data and metadata(Dataflows) urls from Bank for International Settlements (BIS)
         ("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/MED_PS422/",
          "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/all/MED_PS422/latest"),
         ("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/HSW_AW_NNASV/",
          "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/all/HSW_AW_NNASV/latest"),
         ("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/GBV_DV_OCC/",
          "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/all/GBV_DV_OCC/latest"),
         # data and metadata(Dataflows) urls from Eurostat (ESTAT)
         ("https://sdmx.oecd.org/public/rest/data/DSD_FUA_ECO@DF_ECONOMY/all/all",
          "https://sdmx.oecd.org/public/rest/dataflow/all/DSD_FUA_ECO@DF_ECONOMY/latest"),
         ("https://sdmx.oecd.org/public/rest/data/DSD_KIIBIH@DF_B12/all/all",
          "https://sdmx.oecd.org/public/rest/dataflow/all/DSD_KIIBIH@DF_B12/latest"),
         ("https://sdmx.oecd.org/public/rest/data/DSD_PRICES@DF_PRICES_N_CP045_0722/all/all",
          "https://sdmx.oecd.org/public/rest/dataflow/all/DSD_PRICES@DF_PRICES_N_CP045_0722/latest"),
         # data and metadata(Dataflows) urls from Organisation for Economic Co-operation and Development (OECD)
         ("https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/CAUSE_OF_DEATH/all/all",
          "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow/all/CAUSE_OF_DEATH/latest"),
         ("https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/WASH_SCHOOLS/all/all",
          "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow/all/WASH_SCHOOLS/latest"),
         ("https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/CME_TEST_COUNTRY_PROFILES_DATA/all/all",
          "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow/all/CME_TEST_COUNTRY_PROFILES_DATA/latest")
         # data and metadata(Dataflows) urls from United Nations Children's Fund (UNICEF)
       ]


@mark.parametrize("data_url, metadata_url", urls)
def test_metadata_download_from_data(data_url, metadata_url):
    data_message = read_sdmx(data_url, validate=True)
    metadata_message = read_sdmx(metadata_url, validate=True)
    assert data_message is not None, "Failed to download data message"
    assert metadata_message is not None, "Failed to download metadata message"

    structure = data_message.payload.structure
    dataflow = data_message.payload.dataflow
    structure_type = data_message.payload.structure_type
    Dataflows = metadata_message.payload.get('Dataflows')
    DataStructures = metadata_message.payload.get('DataStructures')

    assert structure_type in ['datastructure', 'dataflow'], "Invalid structure type"
    assert structure is not None or dataflow is not None, \
        "Both structure and dataflow are None"

    if DataStructures is not None:
        assert isinstance(DataStructures, dict), "DataStructures should be a dictionary"
        assert len(DataStructures) > 0, "DataStructures is empty"

    if Dataflows is not None:
        assert isinstance(Dataflows, dict), "Dataflows should be a dictionary"
        assert len(Dataflows) > 0, "Dataflows is empty"
