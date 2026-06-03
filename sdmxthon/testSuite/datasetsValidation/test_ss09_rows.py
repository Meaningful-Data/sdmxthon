"""
SS09 (invalid date / time-format value) errors must populate `Rows` with the
input records that triggered them, like the other row-level codes.

SS09 is built in two places, both of which must reverse-look-up the offending
value back to its rows:
  - create_error_SS09 (gregorian / reporting / time-period formats)
  - the inline datetime / TimeRange branch of error_SS09
"""
import pandas as pd

from sdmxthon.parsers.data_validations import create_error_SS09, error_SS09


def test_create_error_ss09_populates_all_matching_rows():
    # '2024-13' fails validation and appears on two rows.
    data = pd.DataFrame({
        'TIME_PERIOD': ['2024-01', '2024-13', '2024-13'],
        'OBS_VALUE': ['1', '2', '3'],
    })
    # process_errors_by_column feeds the check the *unique* values.
    data_column = data['TIME_PERIOD'].unique().astype('str')
    errors = []

    create_error_SS09(data, data_column, 'fmt', 'GregorianYearMonth',
                      'TIME_PERIOD', 'Dimension', errors,
                      lambda e, fmt: e != '2024-13')

    ss09 = [e for e in errors if e['Code'] == 'SS09']
    assert len(ss09) == 1
    assert ss09[0]['Rows'] is not None
    assert len(ss09[0]['Rows']) == 2
    assert {r['OBS_VALUE'] for r in ss09[0]['Rows']} == {'2', '3'}


def test_error_ss09_datetime_branch_populates_rows():
    # '2024-13-01' is an invalid datetime (month 13) -> SS09 tied to its row.
    data = pd.DataFrame({
        'TIME_PERIOD': ['2020-01-01', '2024-13-01'],
        'OBS_VALUE': ['10', '20'],
    })
    data_column = data['TIME_PERIOD'].unique().astype('str')
    errors = []

    error_SS09(data, 'TIME_PERIOD', {'TIME_PERIOD': 'datetime'},
               data_column, errors, 'Dimension')

    ss09 = [e for e in errors if e['Code'] == 'SS09']
    assert len(ss09) == 1
    assert ss09[0]['Rows'] is not None
    assert [r['OBS_VALUE'] for r in ss09[0]['Rows']] == ['20']
