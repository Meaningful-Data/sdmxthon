import re
from datetime import datetime

import numpy as np
import pandas as pd
from pandas import DataFrame

from sdmxthon.model.definitions import DataStructureDefinition

error_level_facets = 'WARNING'


def get_codelist_values(dsd: DataStructureDefinition) -> dict:
    data = {}

    if dsd.dimension_descriptor.components is not None:

        for element in dsd.dimension_descriptor.components.values():
            if (element.representation is not None and
                    element.representation.codelist is not None and
                    not isinstance(element.representation.codelist, str)):
                data[element.id] = list(element.representation.codelist.
                                        items.keys())

    if (dsd.attribute_descriptor is not None and
            dsd.attribute_descriptor.components is not None):
        for record in dsd.attribute_descriptor.components.values():
            if (record.representation is not None and
                    record.representation.codelist is not None and
                    not isinstance(record.representation.codelist, str)):
                data[record.id] = list(record.representation.codelist.
                                       items.keys())

    return data


def get_mandatory_attributes(dsd: DataStructureDefinition) -> list:
    data = []

    if (dsd.attribute_descriptor is None or
            dsd.attribute_descriptor.components is None):
        return []

    for record in dsd.attribute_descriptor.components.values():
        if (record.related_to is not None and
                record.assignment_status == "Mandatory"):
            data.append(record.id)

    return data


def validate_data(data: DataFrame, dsd: DataStructureDefinition):
    """
        Data validations stands for the next schema:

        .. list-table:: Data validations
            :widths: 20 80
            :header-rows: 1

            * - Code
              - Description
            * - SS01
              - Check if all dimensions of the DSD exist in the dataframe
            * - SS02
              - Check if the measure code exists in the dataframe
            * - SS03
              - Check if all mandatory attributes exist in the dataframe
            * - SS04
              - Check if an attribute/dimension value that is associated \
                to a Codelist is valid
            * - SS05
              - Check that all dimensions have values for every record of a \
                dataframe
            * - SS06
              - Check that all mandatory attributes have values for every \
                record of a dataset
            * - SS07
              - Check if two datapoints have the same values
            * - SS08
              - Check that the value inputted is compliant with Facets \
                for the referred Representation
            * - SS09
              - Check if the value is compliant with the desired Time Format
            * - SS10
              - Check if an attribute/dimension value associated to a \
                Cube Region Constraint is valid
            * - SS11
              - Check if each row is compliant with the Series Constraints
    """

    mandatory = get_mandatory_attributes(dsd)
    codelist_values = get_codelist_values(dsd)

    errors = []

    faceted, types = dsd._facet_type

    cubes, series_const = dsd._format_constraints

    process_measure_errors(dsd, data, errors, faceted, types)

    grouping_keys = []

    all_codes = dsd.dimension_codes + dsd.attribute_codes

    for k in dsd.dataset_attribute_codes:
        if k in all_codes:
            all_codes.remove(k)

    man_codes = dsd.dimension_codes + mandatory

    for k in all_codes:
        if k not in data.keys() or data[k].isnull().values.all():
            if k in mandatory:
                errors.append(
                    {'Code': 'SS03', 'ErrorLevel': 'CRITICAL',
                     'Component': f'{k}', 'Type': 'Attribute', 'Rows': None,
                     'Message': f'Missing {k}'})
            elif k in dsd.dimension_codes:
                errors.append(
                    {'Code': 'SS01', 'ErrorLevel': 'CRITICAL',
                     'Component': f'{k}', 'Type': 'Dimension', 'Rows': None,
                     'Message': f'Missing {k}'})
            continue
        else:
            process_errors_by_column(data, dsd, errors, k, man_codes,
                                     grouping_keys,
                                     faceted, types, codelist_values, cubes)

    if len(series_const) > 0:
        error_SS11(data, series_const, errors)

    if len(grouping_keys) > 0:
        duplicated = data[data.duplicated(subset=grouping_keys, keep=False)]
        if len(duplicated) > 0:
            indexes = list(duplicated.index)
            duplicated_dict = duplicated.to_dict(orient="records")
            rows = dict(zip(indexes, duplicated_dict))
            duplicated.groupby(by=grouping_keys).apply(
                lambda x: create_error_SS07(x, rows, errors, grouping_keys)
            )
            del indexes
            del duplicated_dict
            del rows
        del duplicated

    return errors


# Time validations

# Monthly
regex_monthly = r'(19|[2-9][0-9])\d{2}(-(0[1-9]|1[012]))?'
match_monthly = re.compile(regex_monthly)

# Duration
regex_duration = r'(-?)P(?=.)((\d+)Y)?((\d+)M)?((\d+)D)?(T(?=.)((\d+)H)?((' \
                 r'\d+)M)?(\d*(\.\d+)?S)?)? '
match_duration = re.compile(regex_duration)

# semester, quarter and trimester
regex_specials = r'(19|[2-9][0-9])\d{2}-(A[1]|S[1-2]|Q[1-4]|T[' \
                 r'1-3]|M(0[1-9]|1[012])|W(5[0-3]|[1-4][0-9]|[' \
                 r'1-9])|D((00[1-9]|0[1-9][0-9])?|[12][0-9][0-9]|3[' \
                 r'0-5][0-9]|36[0-5]))'
match_specials = re.compile(regex_specials)

# Dictionaries

time_periods = ['ObservationalTimePeriod', 'ReportingTimePeriod',
                'GregorianTimePeriod', 'BasicTimePeriod', "StandardTimePeriod"]

gregorian_periods = {'GregorianDay': "%Y-%m-%d", 'GregorianYearMonth': "%Y-%m",
                     'GregorianYear': "%Y"}

reporting_periods = {'ReportingYear': "A[1]", 'ReportingSemester': "S[1-2]",
                     'ReportingTrimester': "T[1-3]",
                     'ReportingQuarter': "Q[1-4]",
                     "ReportingMonth": "M(0[1-9]|1[012])",
                     "ReportingWeek": "W(5[0-3]|[1-4][0-9]|[1-9])",
                     "ReportingDay": "D((00[1-9]|0[1-9][0-9])?"
                                     "|[12][0-9][0-9]|3[0-5][0-9]|36[0-5])"
                     }


def check_date(e, format_: str):
    try:
        res = datetime.strptime(e, format_)
        if not 1900 < res.year <= 9999:
            return False
    except ValueError:
        return False

    return True


def check_reporting(e, format_):
    # Matching semester, quarter and trimester
    match_reporting = re.compile(format_)

    try:
        res = match_reporting.fullmatch(e)
        if not res:
            return False
    except (TypeError, ValueError):
        return False
    return True


def validate_daily_iso(dt_str, type_):
    # Matching daily and iso format
    duration = ""
    control_changed = False
    if ((type_ == "ObservationalTimePeriod" or
         type_ == "StandardTimePeriod" or
         type_ == "BasicTimePeriod") and '/' in dt_str):
        duration = dt_str.split('/', maxsplit=1)[1]
        dt_str = dt_str.split('/', maxsplit=1)[0]

        # Matching duration
        try:
            res = match_duration.fullmatch(duration)
            if not res:
                dt_str += '/' + duration
                return False
        except (TypeError, ValueError):
            dt_str += '/' + duration
            return False
        control_changed = True
    try:
        res = match_specials.fullmatch(dt_str)
        if res:
            return True
    except (TypeError, ValueError):
        return False

    try:
        res = datetime.strptime(dt_str, '%Y-%m-%d')
        if res:
            return True
    except (TypeError, ValueError):
        return False

    try:
        res = datetime.fromisoformat(dt_str)
        if not 1900 < res.year <= 9999:
            if control_changed:
                dt_str += '/' + duration
            return False
    except (TypeError, ValueError):
        if control_changed:
            dt_str += '/' + duration
        return False
    if control_changed:
        dt_str += '/' + duration


def process_global_time_format(dt_str, type_):
    control_special = False
    for letter in ['A', 'Q', 'W', 'D']:
        if letter in dt_str:
            control_special = True

    if 'M' in dt_str and ':' not in dt_str:
        control_special = True

    if control_special:
        return process_special_time_format(dt_str)

    return process_common_time_format(dt_str, type_)


def process_common_time_format(dt_str, type_):
    # Matching year and monthly
    try:
        res = match_monthly.fullmatch(dt_str)
        if res:
            return True
    except (TypeError, ValueError):
        return False

    # Checks for datetime string in GregorianTimePeriod type
    if 'T' in dt_str and type_ == "GregorianTimePeriod":
        return False

    return validate_daily_iso(dt_str, type_)


def process_special_time_format(dt_str):
    try:
        res = match_specials.fullmatch(dt_str)
        return bool(res)
    except (TypeError, ValueError):
        return False


def time_period_valid(dt_str: str, type_: str):
    """Validates any time period"""

    if type_ in ["ObservationalTimePeriod", "StandardTimePeriod"]:
        return process_global_time_format(dt_str, type_)
    if type_ in ["GregorianTimePeriod", "BasicTimePeriod"]:
        return process_common_time_format(dt_str, type_)

    return process_special_time_format(dt_str)


def error_SS09(k, time_types, data_column, errors, role):
    if time_types[k] in time_periods:
        create_error_SS09(data_column, time_types[k], time_types[k], k,
                          role, errors, time_period_valid)
    elif time_types[k] in gregorian_periods:
        format_ = gregorian_periods[time_types[k]]
        create_error_SS09(data_column, format_, time_types[k], k,
                          role, errors, check_date)

    elif time_types[k] in reporting_periods:

        format_ = r'(19|[2-9][0-9])\d{2}-' + reporting_periods[time_types[k]]

        create_error_SS09(data_column, format_, time_types[k], k,
                          role, errors, time_period_valid)

    elif time_types[k].lower() == "datetime" or time_types[k] == "TimeRange":
        for e in data_column:
            invalid_date = False
            duration = ""
            control_changed = False
            if time_types[k] == "TimeRange" and '/' not in e:
                invalid_date = True
            elif time_types[k] == "TimeRange":
                duration = e.split('/', maxsplit=1)[1]
                e = e.split('/', maxsplit=1)[0]

                try:
                    res = match_duration.fullmatch(duration)
                    if not res:
                        invalid_date = True
                except (TypeError, ValueError):
                    invalid_date = True
                duration = '/' + duration
                control_changed = True

            try:
                res = datetime.fromisoformat(e)
                if not 1900 < res.year <= 9999:
                    invalid_date = True
            except (TypeError, ValueError):
                invalid_date = True

            if invalid_date:
                errors.append(
                    {'Code': 'SS09', 'ErrorLevel': "CRITICAL",
                     'Component': f'{k}',
                     'Type': f'{role}',
                     'Rows': None,
                     'Message': f'Value {e + duration} not compliant '
                                f'with type : {time_types[k]}'})
            if control_changed:
                e += duration


# Facets
def trunc_dec(x):
    return x.rstrip('0').rstrip('.') if '.' in x else x


def check_sequence(data_column, errors, key, type_, start, interval, end):
    data_column = np.sort(data_column)
    control = True
    if int(data_column[0]) < start:
        control = False
        values = data_column[data_column < start].tolist()
        if len(values) > 0:
            for v in values:
                errors.append(
                    {'Code': 'SS08', 'ErrorLevel': error_level_facets,
                     'Component': f'{key}', 'Type': f'{type_}',
                     'Rows': None,
                     'Message': f'Value {v} not compliant '
                                f'with startValue : {start}'})

    if end is not None and int(data_column[-1]) > end:
        control = False
        values = data_column[data_column > end].tolist()
        if len(values) > 0:
            for v in values:
                errors.append(
                    {'Code': 'SS08', 'ErrorLevel': error_level_facets,
                     'Component': f'{key}', 'Type': f'{type_}',
                     'Rows': None,
                     'Message': f'Value {v} not compliant '
                                f'with endValue : {end}'})

    if control:
        values = data_column[(data_column - start) % interval != 0]
        if len(values) > 0:
            for v in values:
                if end is not None:
                    errors.append(
                        {'Code': 'SS08', 'ErrorLevel': error_level_facets,
                         'Component': f'{key}',
                         'Type': f'{type_}',
                         'Rows': None,
                         'Message': f'Value {v} in {key} not compliant '
                                    f'with sequence : {start}-{end} '
                                    f'(interval: {interval})'})
                else:
                    errors.append(
                        {'Code': 'SS08', 'ErrorLevel': error_level_facets,
                         'Component': f'{key}',
                         'Type': f'{type_}',
                         'Rows': None,
                         'Message': f'Value {v} in {key} '
                                    f'not compliant with sequence : '
                                    f'{start}-infinite '
                                    f'(interval: {interval})'})


def check_num_facets(facets, data_column, key, type_):
    errors = []
    is_sequence = None
    start = None
    end = None
    interval = None
    for f in facets:
        values = []
        if f.facet_type == 'maxLength' or f.facet_type == 'minLength':
            temp = data_column.astype('str')
            temp = temp[np.isin(temp, ['nan', 'None'], invert=True)]
            format_temp = np.vectorize(trunc_dec)
            length_checker = np.vectorize(len)
            arr_len = length_checker(format_temp(temp))
            if f.facet_type == 'maxLength':
                max_ = int(f.facet_value)
                values = temp[arr_len > max_]
            else:
                min_ = int(f.facet_value)
                values = temp[arr_len < min_]

        elif f.facet_type == 'maxValue':
            max_ = int(f.facet_value)
            values = data_column[data_column > max_]
        elif f.facet_type == 'minValue':
            min_ = int(f.facet_value)
            values = data_column[data_column < min_]
        elif f.facet_type == 'isSequence':
            if f.facet_value.upper() == 'TRUE':
                is_sequence = True
        elif f.facet_type == 'startValue':
            start = int(f.facet_value)
        elif f.facet_type == 'endValue':
            end = int(f.facet_value)
        elif f.facet_type == 'interval':
            interval = int(f.facet_value)
        else:
            continue

        if len(values) > 0:
            for v in values:
                errors.append(
                    {'Code': 'SS08', 'ErrorLevel': error_level_facets,
                     'Component': f'{key}', 'Type': f'{type_}',
                     'Rows': None,
                     'Message': f'Value {v} not compliant with '
                                f'{f.facet_type} : {f.facet_value}'})

    if is_sequence is not None and start is not None and interval is not None:
        check_sequence(data_column, errors, key, type_, start, interval, end)

    return errors


def check_str_facets(facets, data_column, key, type_):
    data_column = data_column[
        np.isin(data_column, ['nan', 'None'], invert=True)].astype('str')

    error_level = 'WARNING'
    errors = []

    for f in facets:
        if f.facet_type == 'maxLength' or f.facet_type == 'maxValue':
            max_ = int(f.facet_value)
            if f.facet_type == 'maxLength':
                length_checker = np.vectorize(len)
                arr_len = length_checker(data_column)
                values = data_column[arr_len > max_]
            else:
                values = data_column[int(data_column) > max_]
        elif f.facet_type == 'minLength' or f.facet_type == 'minValue':
            min_ = int(f.facet_value)
            if f.facet_type == 'minLength':
                length_checker = np.vectorize(len)
                arr_len = length_checker(data_column)
                values = data_column[arr_len < min_]
            else:
                values = data_column[int(data_column) < min_]

        elif f.facet_type == 'pattern':
            r = re.compile(str(f.facet_value))
            vec = np.vectorize(lambda x: bool(not r.fullmatch(x)))
            values = data_column[vec(data_column)]
        else:
            continue

        if len(values) > 0:
            for v in values:
                errors.append({'Code': 'SS08', 'ErrorLevel': error_level,
                               'Component': f'{key}', 'Type': f'{type_}',
                               'Rows': None,
                               'Message': f'Value {v} not compliant with '
                                          f'{f.facet_type} : {f.facet_value}'})
    return errors


# Processing errors

def process_measure_errors(dsd, data, errors, faceted, types):
    mc = dsd.measure_code
    type_ = 'Measure'

    if mc not in data.keys() or data[mc].isnull().values.all():
        errors.append(
            {'Code': 'SS02', 'ErrorLevel': 'CRITICAL', 'Component': f'{mc}',
             'Type': f'{type_}', 'Rows': None,
             'Message': f'Missing {mc}'})
    elif data[mc].isnull().values.any():
        if 'OBS_STATUS' in data.keys():

            rows = data[
                (data[mc].isna()) & (data['OBS_STATUS'] != 'M')].to_dict(
                'records')
            if len(rows) > 0:
                errors.append({'Code': 'SS02', 'ErrorLevel': 'CRITICAL',
                               'Component': f'{mc}', 'Type': f'{type_}',
                               'Rows': rows.copy(),
                               'Message': f'Missing value in '
                                          f'{type_.lower()} {mc}'})
        else:
            rows = data[data[mc].isna()].to_dict('records')
            if len(rows) > 0:
                errors.append({'Code': 'SS02', 'ErrorLevel': 'CRITICAL',
                               'Component': f'{mc}', 'Type': f'{type_}',
                               'Rows': rows.copy(),
                               'Message': f'Missing value in '
                                          f'{type_.lower()} {mc}'})

    if mc in data.keys() and mc in faceted:
        facets = faceted[mc]
        try:
            data_column = data[mc].astype('float64')
            errors += check_num_facets(facets, data_column, mc, type_)
        except (TypeError, ValueError):
            data_column = data[mc].astype('str')
            errors += check_str_facets(facets, data_column, mc, type_)

        del data_column


def process_errors_by_column(data, dsd, errors, k, man_codes, grouping_keys,
                             faceted, types, codelist_values, cubes):
    is_numeric = False

    data_column = data[k].unique().astype('str')

    if 'TimePeriod' not in types[k]:
        try:
            data_column = data_column.astype('float64')
            is_numeric = True
        except (TypeError, ValueError):
            pass

    if k in dsd.attribute_codes:
        role = 'Attribute'
        code = 'SS06'
    else:
        grouping_keys.append(k)
        role = 'Dimension'
        code = 'SS05'

    if k in man_codes:
        control = False
        if is_numeric:
            if np.isnan(np.sum(data_column)):
                control = True
        else:
            if 'nan' in data_column:
                control = True
        if control:
            pos = data[(data[k] == 'nan') | (data[k] == '') |
                       (data[k].isnull())].index.values
            rows = data.iloc[pos, :].to_dict('records')
            errors.append({'Code': code, 'ErrorLevel': 'CRITICAL',
                           'Component': f'{k}', 'Type': f'{role}',
                           'Rows': rows.copy(),
                           'Message': f'Missing value in '
                                      f'{role.lower()} {k}'})

    if k in types:
        error_SS09(k, types, data_column, errors, role)

    if k in faceted:
        facets = faceted[k]
        if is_numeric:
            errors += check_num_facets(facets, data_column, k, role)
        else:
            errors += check_str_facets(facets, data_column, k, role)

    if is_numeric:
        data_column = data_column.astype('str')
        format_temp = np.vectorize(trunc_dec)
        data_column = format_temp(data_column)

    if k in cubes.keys():
        code = 'SS10'
        values = data_column[
            np.isin(data_column, list(cubes[k]), invert=True)]
        if len(values) > 0:
            create_error_SS10_SS04(values, code, role, k, errors)

    elif k in codelist_values.keys():
        code = 'SS04'
        values = data_column[
            np.isin(data_column, codelist_values[k], invert=True)]
        if len(values) > 0:
            create_error_SS10_SS04(values, code, role, k, errors)


def create_error_SS10_SS04(values, code, role, k, errors):
    values = values[
        np.isin(values, ['nan', 'None', np.nan], invert=True)]
    for v in values:
        errors.append({'Code': code, 'ErrorLevel': 'CRITICAL',
                       'Component': f'{k}', 'Type': f'{role}',
                       'Rows': None,
                       'Message': f'Wrong value {v} for '
                                  f'{role.lower()} {k}'})

        
def format_row(row, grouping_keys):
    string = ''
    for k in grouping_keys:
        string += f' ( {str(k)} : ' \
                  f'{str(row[k]) if str(row[k]) != "nan" else ""} ) '
    return string


def create_error_SS07(x, rows, errors, grouping_keys):
    elems = [rows[k] for k in list(x.index)]
    errors.append({'Code': 'SS07',
                   'ErrorLevel': 'WARNING',
                   'Component': 'Duplicated',
                   'Type': 'Datapoint',
                   'Rows': elems,
                   'Message': f'Duplicated datapoint '
                              f'{format_row(elems[0], grouping_keys)}'
                   })


def create_error_SS09(data_column, format_, time_type, comp, role, errors,
                      func):
    for e in data_column:
        if not func(e, format_):
            errors.append(
                {'Code': 'SS09', 'ErrorLevel': "CRITICAL",
                 'Component': f'{comp}',
                 'Type': f'{role}',
                 'Rows': None,
                 'Message': f'Value {e} not compliant with '
                            f'type : {time_type}'})


def error_SS11(data, series_const, errors):
    lookup = pd.DataFrame(series_const).drop_duplicates() \
        .reset_index(drop=True)
    all_columns = lookup.columns.tolist()

    result = all(elem in data.columns.tolist() for elem in all_columns)

    if result:
        columns = lookup.columns[lookup.isna().any()].tolist()

        lookup['membership_series_const'] = True

        dict_wild = {}

        for e in columns:
            dict_wild[e] = lookup[lookup[e].isna()]
            dict_wild[e].pop(e)

        res = data[all_columns].merge(lookup, how="left")

        for k in dict_wild:
            res.update(data[all_columns].merge(dict_wild[k], how="left"),
                       overwrite=False)

        indexes = res[res['membership_series_const'].isna()].index.tolist()

        del res
        del dict_wild
        del lookup
        del all_columns

        if len(indexes) > 0:
            rows = data.loc[indexes, :].to_dict('records')
            errors.append({'Code': 'SS11',
                           'ErrorLevel': 'WARNING',
                           'Component': 'Series',
                           'Type': 'Constraint',
                           'Rows': rows.copy(),
                           'Message': 'Found disallowed rows'
                           })
            del rows
    else:
        del lookup
        del all_columns
