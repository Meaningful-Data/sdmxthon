import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.submission import SubmissionResult
from sdmxthon.utils.handlers import first_element_dict

pytestmark = mark.input_path(Path(__file__).parent / "data")


# Test parsing SDMX Registry Interface Submission Response
@mark.parametrize("filename, action, status", [
    ('append_response.xml', 'Append', 'Success'),
])
def test_submission_result(data_path, filename, action, status):
    file_path = os.path.join(data_path, filename)
    message = read_sdmx(file_path, validate=False)

    assert len(message.payload) > 0
    submission_result = first_element_dict(message.payload)
    assert isinstance(submission_result, SubmissionResult)
    assert submission_result.action == action
    assert submission_result.status == status
    assert submission_result.full_id == list(message.payload.keys())[0]
