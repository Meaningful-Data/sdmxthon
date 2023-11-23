"""
Metadata from Different Sources Tests
"""
import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx

pytestmark = mark.input_path(Path(__file__).parent / "data")

params = [
    ("bis.xml", "bis.txt", "BIS:BIS_DER(1.0)"),
    ("estat.xml", "estat.txt", "ESTAT:HLTH_RS_PRSHP1(7.0)"),
    ("imf.xml", "imf.txt", "IMF:ALT_FISCAL_DSD(1.0)"),
    ("wb.xml", "wb.txt", "WB:WDI(1.0)"),
]


@mark.parametrize("data_filename, reference_filename, dsd_name", params)
def test_metadata_compare(data_filename, reference_filename, dsd_name,
                          data_path, reference_path):
    obj_ = read_sdmx(os.path.join(data_path, data_filename))
    content = {'content': obj_.content,
               'items': obj_.payload['DataStructures'][dsd_name].content,
               'representation': obj_.payload['DataStructures'][
                   dsd_name].measure_descriptor.components[
                   'OBS_VALUE'].representation}
    with open(str(Path(reference_path) / reference_filename), 'r') as f:
        reference = f.read()

    assert str(content) == reference
