"""
Data Writing Tests
"""
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
from pytest import mark

from sdmxthon.api.api import read_sdmx, get_pandas_df
from sdmxthon.model.dataset import Dataset
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict

pytestmark = mark.input_path(Path(__file__).parent / "data")

data_types_params = [
    (MessageTypeEnum.GenericDataSet, False),
    (MessageTypeEnum.GenericDataSet, True),
    (MessageTypeEnum.StructureSpecificDataSet, False),
    (MessageTypeEnum.StructureSpecificDataSet, True)
]


@mark.parametrize("data_type,series", data_types_params)
def test_data_writing(data_type, series, data_path, metadata_path):
    message = read_sdmx(os.path.join(metadata_path, 'metadata.xml'))
    data_path = os.path.join(data_path, "df.json")
    dataset = Dataset(data=pd.read_json(data_path, orient='records'),
                      structure=message.payload['DataStructures']
                      ['BIS:BIS_DER(1.0)'])

    dataset.data = dataset.data.astype('str')

    if series:
        dataset.set_dimension_at_observation('TIME_PERIOD')

    prepared_time = datetime.fromisoformat('2000-01-01T00:00:01')

    result = dataset.to_xml(data_type, '',
                            prepared=prepared_time,
                            prettyprint=False)

    df = first_element_dict(get_pandas_df(BytesIO(bytes(result,
                                                        encoding='UTF-8'))))

    pd.testing.assert_frame_equal(
        df.fillna('').replace('nan', ''),
        dataset.data.replace('nan', ''),
        check_like=True)


@mark.parametrize("sdmx_version", [1, 2])
def test_to_sdmx_csv_writing(data_path, metadata_path, sdmx_version):
    message = read_sdmx(os.path.join(metadata_path, 'metadata.xml'))
    data_path = os.path.join(data_path, "df.json")
    dataset = Dataset(data=pd.read_json(data_path, orient='records'),
                      structure=message.payload['DataStructures']
                      ['BIS:BIS_DER(1.0)'])
    dataset.data = dataset.data.astype('str')
    result_sdmx_csv = dataset.to_sdmx_csv(sdmx_version)
    message_sdmx_csv = read_sdmx(result_sdmx_csv)
    dataset_sdmx_csv = first_element_dict(message_sdmx_csv.payload)
    pd.testing.assert_frame_equal(
        dataset_sdmx_csv.data.fillna('').replace('nan', ''),
        dataset.data.replace('nan', ''),
        check_like=True)
