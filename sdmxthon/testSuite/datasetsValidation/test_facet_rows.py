"""
SS08 facet-validation errors must populate `Rows` with the input records that
triggered them, mirroring SS02/SS04/SS05/SS06/SS07/SS10/SS11.

These exercise the facet helpers directly: they take the full `data` frame plus
the column key, and reverse-look-up each offending value back to its rows.
"""
import pandas as pd

from sdmxthon.model.representation import Facet
from sdmxthon.parsers.data_validations import (check_num_facets,
                                               check_str_facets)


def test_str_facet_pattern_populates_all_matching_rows():
    # 'xx' fails the 2-uppercase pattern and appears on two rows.
    data = pd.DataFrame({
        'DIM': ['AB', 'xx', 'CD', 'xx'],
        'OBS_VALUE': ['1', '2', '3', '4'],
    })
    facets = [Facet(facetType='pattern', facetValue='[A-Z]{2}')]
    # process_errors_by_column feeds the facet checks the *unique* values.
    data_column = data['DIM'].unique().astype('str')

    errors = check_str_facets(data, facets, data_column, 'DIM', 'Dimension')

    ss08 = [e for e in errors if e['Code'] == 'SS08']
    assert len(ss08) == 1
    assert ss08[0]['Rows'] is not None
    assert len(ss08[0]['Rows']) == 2
    assert {r['OBS_VALUE'] for r in ss08[0]['Rows']} == {'2', '4'}


def test_num_facet_maxvalue_populates_rows_with_numeric_fallback():
    # Stored as the string '99'; the offending value is the float 99.0, so the
    # match must fall back to a numeric comparison.
    data = pd.DataFrame({'OBS_VALUE': ['4', '2', '99']})
    facets = [Facet(facetType='maxValue', facetValue='10')]
    data_column = data['OBS_VALUE'].astype('float64')

    errors = check_num_facets(data, facets, data_column, 'OBS_VALUE', 'Measure')

    ss08 = [e for e in errors if e['Code'] == 'SS08']
    assert len(ss08) == 1
    assert ss08[0]['Rows'] is not None
    assert [r['OBS_VALUE'] for r in ss08[0]['Rows']] == ['99']


def test_num_facet_recovers_zero_padded_rows():
    # '04.0' and '2' are both < 10; the float offending values (4.0, 2.0) must
    # map back to their original zero-padded / plain string cells.
    data = pd.DataFrame({'OBS_VALUE': ['04.0', '2', '99']})
    facets = [Facet(facetType='minValue', facetValue='10')]
    data_column = data['OBS_VALUE'].astype('float64')

    errors = check_num_facets(data, facets, data_column, 'OBS_VALUE', 'Measure')

    ss08 = [e for e in errors if e['Code'] == 'SS08']
    assert len(ss08) == 2
    recovered = {r['OBS_VALUE'] for e in ss08 for r in (e['Rows'] or [])}
    assert recovered == {'04.0', '2'}


def test_sequence_violation_populates_rows():
    # interval 2 from start 0 -> '3' is off-sequence; check_num_facets delegates
    # to check_sequence, which must also receive `data` to populate Rows.
    data = pd.DataFrame({'DIM': ['0', '2', '3'], 'OBS_VALUE': ['a', 'b', 'c']})
    facets = [Facet(facetType='isSequence', facetValue='true'),
              Facet(facetType='startValue', facetValue='0'),
              Facet(facetType='interval', facetValue='2')]
    data_column = data['DIM'].astype('float64')

    errors = check_num_facets(data, facets, data_column, 'DIM', 'Dimension')

    ss08 = [e for e in errors if e['Code'] == 'SS08']
    assert ss08
    assert all(e['Rows'] is not None for e in ss08)
    assert any(r['OBS_VALUE'] == 'c' for e in ss08 for r in e['Rows'])
