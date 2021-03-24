import re
import warnings

import numpy as np
import pandas.api.types
from pandas import DataFrame

from SDMXthon.model.component import DataStructureDefinition


def get_codelist_values(dsd: DataStructureDefinition) -> dict:
    data = {}

    if dsd.dimensionDescriptor.components is not None:

        for element in dsd.dimensionDescriptor.components.values():
            if element.local_representation is not None and element.local_representation.codelist is not None:
                if not isinstance(element.local_representation.codelist, str):
                    data[element.id] = list(element.local_representation.codelist.items.keys())
            elif element.concept_identity is not None:
                if not isinstance(element.concept_identity, dict):
                    if element.concept_identity.coreRepresentation is not None and \
                            element.concept_identity.coreRepresentation.codelist is not None:
                        data[element.id] = list(element.concept_identity.coreRepresentation.codelist.items.keys())

    if dsd.attributeDescriptor is not None and dsd.attributeDescriptor.components is not None:
        for record in dsd.attributeDescriptor.components.values():
            if record.local_representation is not None and record.local_representation.codelist is not None:
                if not isinstance(record.local_representation.codelist, str):
                    data[record.id] = list(record.local_representation.codelist.items.keys())
            elif record.concept_identity is not None:
                if not isinstance(record.concept_identity, dict):
                    if record.concept_identity.coreRepresentation is not None and \
                            record.concept_identity.coreRepresentation.codelist is not None:
                        data[record.id] = list(record.concept_identity.coreRepresentation.codelist.items.keys())

    return data


def get_mandatory_attributes(dsd: DataStructureDefinition) -> list:
    data = []

    if dsd.attributeDescriptor is None or dsd.attributeDescriptor.components is None:
        return []

    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None and record.usageStatus == "Mandatory":
            data.append(record.id)

    return data


def facet_error(error_level, obj_id, obj_type, rows, value, facetType, facetValue) -> dict:
    return {'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{obj_id}', 'Type': f'{obj_type}',
            'Rows': rows.copy(), 'Message': f'Value {value} is not compliant with {facetType} : {facetValue}'}


def parse_datapoint(row):
    string = ''
    for k, v in row.items():
        if k != 'OBS_VALUE':
            string += f' ( {str(k)} : {str(v) if str(v) != "nan" else ""} ) '
    return string


def format_row(row):
    string = ''
    for k, v in row.items():
        string += f' ( {str(k)} : {str(v) if str(v) != "nan" else ""} ) '
    return string


def trunc_dec(x):
    return x.rstrip('0').rstrip('.') if '.' in x else x


def check_num_facets(facets, data_column, key, type_):
    error_level = 'WARNING'
    errors = []
    is_sequence = None
    start = None
    end = None
    interval = None
    for f in facets:
        values = []
        if f.facetType == 'maxLength' or f.facetType == 'minLength':
            temp = data_column.astype('str')
            temp = temp[np.isin(temp, ['nan', 'None'], invert=True)]
            format_temp = np.vectorize(trunc_dec)
            length_checker = np.vectorize(len)
            arr_len = length_checker(format_temp(temp))
            if f.facetType == 'maxLength':
                max_ = int(f.facetValue)
                values = temp[arr_len > max_]
            else:
                min_ = int(f.facetValue)
                values = temp[arr_len < min_]

        elif f.facetType == 'maxValue':
            max_ = int(f.facetValue)
            values = data_column[data_column > max_]
        elif f.facetType == 'minValue':
            min_ = int(f.facetValue)
            values = data_column[data_column < min_]
        elif f.facetType is 'isSequence':
            if f.facetValue.upper() is 'TRUE':
                is_sequence = True
        elif f.facetType is 'startValue':
            start = int(f.facetValue)
        elif f.facetType is 'endValue':
            end = int(f.facetValue)
        elif f.facetType is 'interval':
            interval = int(f.facetValue)
        else:
            continue

        if len(values) > 0:
            for v in values:
                errors.append({'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{key}', 'Type': f'{type_}',
                               'Rows': None, 'Message': f'Value {v} not compliant with '
                                                        f'{f.facetType} : {f.facetValue}'})

    if is_sequence is not None and start is not None and interval is not None:
        data_column = np.sort(data_column)
        control = True
        if int(data_column[0]) < start:
            control = False
            values = data_column[data_column < start].tolist()
            if len(values) > 0:
                for v in values:
                    errors.append({'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{key}', 'Type': f'{type_}',
                                   'Rows': None, 'Message': f'Value {v} not compliant with startValue : {start}'})

        if end is not None and int(data_column[-1]) > end:
            control = False
            values = data_column[data_column > end].tolist()
            if len(values) > 0:
                for v in values:
                    errors.append({'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{key}', 'Type': f'{type_}',
                                   'Rows': None, 'Message': f'Value {v} not compliant with endValue : {end}'})

        if control:
            values = data_column[(data_column - start) % interval != 0]
            if len(values) > 0:
                for v in values:
                    if end is not None:
                        errors.append(
                            {'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{key}', 'Type': f'{type_}',
                             'Rows': None,
                             'Message': f'Value {v} in {key} not compliant '
                                        f'with sequence : {start}-{end} (interval: {interval})'})
                    else:
                        errors.append(
                            {'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{key}', 'Type': f'{type_}',
                             'Rows': None,
                             'Message': f'Value {v} in {key} '
                                        f'not compliant with sequence : '
                                        f'{start}-infinite (interval: {interval})'})

    return errors


def check_str_facets(facets, data_column, key, type_):
    data_column = data_column[np.isin(data_column, ['nan', 'None'], invert=True)].astype('str')

    error_level = 'WARNING'
    errors = []

    for f in facets:
        if f.facetType == 'maxLength' or f.facetType == 'maxValue':
            max_ = int(f.facetValue)
            if f.facetType == 'maxLength':
                length_checker = np.vectorize(len)
                arr_len = length_checker(data_column)
                values = data_column[arr_len > max_]
            else:
                values = data_column[int(data_column) > max_]
        elif f.facetType == 'minLength' or f.facetType == 'minValue':
            min_ = int(f.facetValue)
            if f.facetType == 'minLength':
                length_checker = np.vectorize(len)
                arr_len = length_checker(data_column)
                values = data_column[arr_len < min_]
            else:
                values = data_column[int(data_column) < min_]

        elif f.facetType == 'pattern':
            r = re.compile(str(f.facetValue).encode('unicode-escape').decode())
            vec = np.vectorize(lambda x: bool(not r.fullmatch(x)))
            values = data_column[vec(data_column)]
        else:
            continue

        if len(values) > 0:
            for v in values:
                errors.append({'Code': 'SS08', 'ErrorLevel': error_level, 'Component': f'{key}', 'Type': f'{type_}',
                               'Rows': None, 'Message': f'Value {v} not compliant with '
                                                        f'{f.facetType} : {f.facetValue}'})
    return errors


def validate_data(data: DataFrame, dsd: DataStructureDefinition):
    mandatory = get_mandatory_attributes(dsd)
    codelist_values = get_codelist_values(dsd)

    warnings.simplefilter(action='ignore', category=FutureWarning)

    """
        Validations stands for the next schema:
        
        SS01: Check if all dimensions of a DSD exist in the dataset
        SS02: Check if  OBS_VALUE exists in the datasets
        SS03: Check if all mandatory attributes exit in the datasets
        SS04: Check if an attribute/dimension value that is associated to a Codelist is valid
        SS05: Check that all dimensions have values for every record of a dataset
        SS06: Check that all mandatory attributes have values for every record of a dataset
        SS07: Check if two data_points are the same
        SS08: Check that the value inputted is compliant with Facets for the referred Representation
    """
    errors = []

    faceted_objects = dsd.facetedObjects

    mc = dsd.measureCode
    type_ = 'Measure'

    if mc not in data.keys() or data[mc].isnull().values.all():
        errors.append({'Code': 'SS02', 'ErrorLevel': 'CRITICAL', 'Component': f'{mc}', 'Type': f'{type_}', 'Rows': None,
                       'Message': f'Missing {mc}'})
    elif data[mc].isnull().values.any():
        if 'OBS_STATUS' in data.keys():

            rows = data[(data[mc].isna()) & (data['OBS_STATUS'] != 'M')].to_dict('records')
            if len(rows) > 0:
                errors.append({'Code': 'SS02', 'ErrorLevel': 'CRITICAL', 'Component': f'{mc}', 'Type': f'{type_}',
                               'Rows': rows.copy(), 'Message': f'Missing value in {type_.lower()} {mc}'})
        else:
            rows = data[data[mc].isna()].to_dict('records')
            if len(rows) > 0:
                errors.append({'Code': 'SS02', 'ErrorLevel': 'CRITICAL', 'Component': f'{mc}', 'Type': f'{type_}',
                               'Rows': rows.copy(), 'Message': f'Missing value in {type_.lower()} {mc}'})

        if mc in faceted_objects:
            facets = faceted_objects[mc]
            if pandas.api.types.is_numeric_dtype(data[mc]):
                data_column = data[mc].unique().astype('float64')
                errors += check_num_facets(facets, data_column, mc, type_)
            else:
                data_column = data[mc].unique().astype('str')
                errors += check_str_facets(facets, data_column, mc, type_)

    grouping_keys = []

    all_codes = dsd.dimensionCodes + dsd.attributeCodes

    for k in dsd.datasetAttributeCodes:
        if k in all_codes:
            all_codes.remove(k)

    man_codes = dsd.dimensionCodes + mandatory

    for k in all_codes:
        if k not in data.keys() or data[k].isnull().values.all():
            if k in mandatory:
                errors.append(
                    {'Code': 'SS03', 'ErrorLevel': 'CRITICAL', 'Component': f'{k}', 'Type': f'Attribute', 'Rows': None,
                     'Message': f'Missing {k}'})
            elif k in dsd.dimensionCodes:
                errors.append(
                    {'Code': 'SS01', 'ErrorLevel': 'CRITICAL', 'Component': f'{k}', 'Type': f'Dimension', 'Rows': None,
                     'Message': f'Missing {k}'})
            continue

        is_numeric = False

        if pandas.api.types.is_numeric_dtype(data[k]):
            data_column = data[k].unique().astype('float64')
            is_numeric = True
        else:
            data_column = data[k].astype('str').fillna('nan').unique()

        if k in dsd.attributeCodes:
            type_ = 'Attribute'
            code = 'SS06'
        else:
            grouping_keys.append(k)
            type_ = 'Dimension'
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
                pos = data[(data[k] == 'nan') | (data[k].isnull())].index.values
                rows = data.iloc[pos, :].to_dict('records')
                errors.append({'Code': code, 'ErrorLevel': 'CRITICAL', 'Component': f'{k}', 'Type': f'{type_}',
                               'Rows': rows.copy(), 'Message': f'Missing value in {type_.lower()} {k}'})

        if k in faceted_objects:
            facets = faceted_objects[k]
            if is_numeric:
                errors += check_num_facets(facets, data_column, k, type_)
            else:
                errors += check_str_facets(facets, data_column, k, type_)

        if is_numeric:
            data_column = data_column.astype('str')
            format_temp = np.vectorize(trunc_dec)
            data_column = format_temp(data_column)

        if k in codelist_values.keys():
            code = 'SS04'
            values = data_column[np.isin(data_column, codelist_values[k], invert=True)]
            if len(values) > 0:
                values = values[np.isin(values, ['nan', 'None', np.nan], invert=True)]
                for v in values:
                    errors.append({'Code': code, 'ErrorLevel': 'CRITICAL', 'Component': f'{k}', 'Type': f'{type_}',
                                   'Rows': None, 'Message': f'Wrong value {v} for {type_.lower()} {k}'})

    duplicated = data[data.duplicated(subset=grouping_keys, keep=False)]
    if len(duplicated) > 0:
        duplicated_indexes = duplicated[grouping_keys].drop_duplicates().index.values
        for v in duplicated_indexes:
            data_point = duplicated.loc[v, grouping_keys]
            series = duplicated[grouping_keys].apply(lambda row: np.array_equal(row.values, data_point.values), axis=1)
            pos = series[series].index.values
            rows = duplicated.loc[pos, :].to_dict('records')
            duplicated = duplicated.drop(pos)
            errors.append({'Code': 'SS07',
                           'ErrorLevel': 'WARNING',
                           'Component': f'Duplicated',
                           'Type': f'Datapoint',
                           'Rows': rows.copy(),
                           'Message': f'Duplicated datapoint {format_row(data_point)}'
                           })

    return errors
