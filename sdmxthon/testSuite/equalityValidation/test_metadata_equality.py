"""
Metadata Equality Tests
"""
import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx

pytestmark = mark.input_path(Path(__file__).parent / "data")

filenames = ["bis.xml", "estat.xml", "imf.xml", "wb.xml"]


# Test: Metadata equality
@mark.parametrize("filename", filenames)
def test_metadata_equality(filename, data_path):
    obj_ = read_sdmx(os.path.join(data_path, filename))
    obj_2 = read_sdmx(os.path.join(data_path, filename))

    assert obj_2 == obj_


# Test: Metadata inequality
def test_metadata_inequality(data_path):
    obj_ = read_sdmx(os.path.join(data_path, 'bis.xml'))
    obj_2 = read_sdmx(os.path.join(data_path, 'wb.xml'))

    assert obj_2 != obj_
