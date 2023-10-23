"""
Datasets Validation Tests
"""
import json
import os
from pathlib import Path

from pytest import mark

from sdmxthon.api.api import get_datasets

pytestmark = mark.input_path(Path(__file__).parent / "data")

validations_params = [
    ("valid.xml", "metadata.xml", None),
    ("invalid.xml", "metadata.xml", "errors_test_2.json"),
]


@mark.parametrize("data_filename, metadata_filename, reference_filename",
                  validations_params)
def test_datasets_validation(data_filename, metadata_filename,
                             reference_filename, data_path, reference_path,
                             metadata_path):
    # Single dataset or dict of datasets
    dataset = get_datasets(os.path.join(data_path, data_filename),
                           os.path.join(metadata_path, metadata_filename))
    sv_result = dataset.structural_validation()
    if reference_filename is None:
        reference_dict = []
    else:
        with open(os.path.join(reference_path, reference_filename)) as f:
            reference_dict = json.loads(f.read())
        sv_result = json.loads(json.dumps(sv_result).replace("NaN",
                                                             'null'))
        sv_result = sorted(sv_result, key=lambda i: i['Code'])
        reference_dict = sorted(reference_dict, key=lambda i: i['Code'])

    assert sv_result == reference_dict
