import os
import re
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.error import SDMXError

pytestmark = mark.input_path(Path(__file__).parent / "data")


# Test parsing SDMX Error messages
@mark.parametrize("filename, code, text", [
    ('error_304.xml', 304, ('Either no structures were submitted, '
                            'or the submitted structures contain no changes '
                            'from the ones currently stored in the system'))
])
def test_error_message(data_path, filename, code, text):
    file_path = os.path.join(data_path, filename)
    message = read_sdmx(file_path, validate=False)
    error = message.payload
    assert isinstance(error, SDMXError)
    assert error.code == code
    error_text = re.sub(' +', ' ', error.text.replace('\n', ''))
    assert error_text == text.replace('\n', '')
