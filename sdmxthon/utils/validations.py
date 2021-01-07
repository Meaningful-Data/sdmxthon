import re

import numpy as np
from pandas import DataFrame

from ..model.structure import DataStructureDefinition, Dimension, Facet


def get_codelist_values(dsd: DataStructureDefinition) -> dict:
    data = {}

    if dsd.dimensionDescriptor.components is not None:

        for element in dsd.dimensionDescriptor.components.values():
            if element.localRepresentation.codeList is not None:
                data[element.id] = element.localRepresentation.codeList.items.keys()

    if dsd.attributeDescriptor is not None and dsd.attributeDescriptor.components is not None:
        for record in dsd.attributeDescriptor.components.values():
            if record.localRepresentation.codeList is not None:
                data[record.id] = record.localRepresentation.codeList.items.keys()

    return data


def get_mandatory_attributes(dsd: DataStructureDefinition) -> list:
    data = []

    if dsd.attributeDescriptor is None or dsd.attributeDescriptor.components is None:
        return []

    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None and record.usageStatus == "Mandatory":
            if isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                data.append(record.id)

    return data


def check_facets(facets: list, value, dsd: DataStructureDefinition, obj_id, obj_type):
    error_list = []

    isSequence = None
    start = None
    end = None
    interval = None
    for f in facets:
        f: Facet
        if f.facetType is not None:

            if f.facetType == 'minLength' and len(value) < int(f.facetValue):
                error_list.append(f'Value {value} is not compliant with {f.facetType} : {f.facetValue} '
                                  f'on {obj_type} {obj_id} in dataset {dsd.id}')
            if f.facetType == 'maxLength' and len(value) > int(f.facetValue):
                error_list.append(f'Value {value} is not compliant with {f.facetType} : {f.facetValue} '
                                  f'on {obj_type} {obj_id} in dataset {dsd.id}')
            if f.facetType == 'minValue' and int(value) < int(f.facetValue):
                error_list.append(f'Value {value} is not compliant with {f.facetType} : {f.facetValue} '
                                  f'on {obj_type} {obj_id} in dataset {dsd.id}')
            if f.facetType == 'maxValue' and int(value) > int(f.facetValue):
                error_list.append(f'Value {value} is not compliant with {f.facetType} : {f.facetValue} '
                                  f'on {obj_type} {obj_id} in dataset {dsd.id}')

            if f.facetType == 'pattern':
                if re.fullmatch(str(f.facetValue).encode('unicode-escape').decode(), value) is None:
                    error_list.append(f'Value {value} is not compliant with {f.facetType} : {f.facetValue} '
                                      f'on {obj_type} {obj_id} in dataset {dsd.id}')

            if f.facetType is 'isSequence':
                if f.facetValue.upper() is 'TRUE':
                    isSequence = True
                elif f.facetValue.upper() is 'FALSE':
                    isSequence = False
            if f.facetType is 'startValue':
                start = int(f.facetValue)
            if f.facetType is 'endValue':
                end = int(f.facetValue)
            if f.facetType is 'interval':
                interval = int(f.facetValue)

    if isSequence is not None and start is not None and interval is not None:
        if int(value) < start:
            error_list.append(f'Value {value} is not compliant with startValue : {start} '
                              f'on {obj_type} {obj_id} in dataset {dsd.id}')

        if end is not None and int(value) > end:
            error_list.append(f'Value {value} is not compliant with endValue : {end} '
                              f'on {obj_type} {obj_id} in dataset {dsd.id}')
        else:
            result = int(value) - start

            if result % interval != 0:
                error_list.append(f'Value {value} is not compliant with startValue : {start} '
                                  f'in dataset {dsd.id}')

    return error_list


def parse_datapoint(row, dsd):
    string = ''
    for k, v in row.items():
        if k != 'OBS_VALUE':
            string += ' (' + str(k) + ' : ' + str(v) + ') '
    return f'Duplicated data point{string}for dataset {dsd.id}'


def validate_obs(data: DataFrame, dsd: DataStructureDefinition):
    mandatory = get_mandatory_attributes(dsd)
    codelist_values: dict = get_codelist_values(dsd)

    """
        Validations stands for the next schema:
        
        SS01: Check if all dimensions of a DSD exist in the dataset
        SS02: Check if  OBS_VALUE exists in the datasets
        SS03: Check if all mandatory attributes exit in the datasets
        SS04: Check if an attribute/dimension value that is associated to a Codelist is valid
        SS05: Check that all dimensions have values for every record of a dataset
        SS06: Check that all mandatory attributes have values for every record of a dataset
        SS07: Check if two OBS_VALUE are the same for each Serie
        SS08: Check that the value inputted is compliant with Facets for the referred Representation
    """

    list_ss01 = []
    list_ss02 = []
    list_ss03 = []
    list_ss04 = []
    list_ss05 = []
    list_ss06 = []
    list_ss07 = []
    list_ss08 = []

    if 'OBS_VALUE' not in data.keys():
        list_ss02.append(f'Missing OBS_VALUE for dataset {dsd.id}')
    elif data['OBS_VALUE'].isnull().values.any():
        df = data[data['OBS_VALUE'] == np.nan]
        list_ss02 += df[:].apply(lambda row: f'Missing value for OBS_VALUE on row {":".join(map(str, row.values))}'
                                             f' for dataset {dsd.id}', axis=1).tolist()

    if dsd.measureDescriptor is not None and dsd.measureCode is not None:
        if dsd.measureDescriptor.components[dsd.measureCode].localRepresentation is not None and \
                len(dsd.measureDescriptor.components[dsd.measureCode].localRepresentation.facets) > 0:
            values = data['OBS_VALUE'].unique()
            for e in values:
                list_ss08 += check_facets(dsd.measureDescriptor.components['OBS_VALUE'].localRepresentation.facets, e,
                                          dsd, 'OBS_VALUE', 'Measure')

    facets = False

    for k in dsd.dimensionCodes:
        if k not in data.keys():
            list_ss01.append(f'Missing dimension {k} on dataset {dsd.id}')
            continue

        if dsd.dimensionDescriptor.components[k].localRepresentation is not None:
            if len(dsd.dimensionDescriptor.components[k].localRepresentation.facets) > 0:
                facets = True

        values = data[k].unique()
        for e in values:

            if facets:
                list_ss08 += check_facets(dsd.dimensionDescriptor.components[k].localRepresentation.facets, e, dsd,
                                          k, 'Dimension')

            if e == np.nan or str(e) == 'nan' or str(e) == 'None':
                df = data[data[k] == np.nan]
                list_ss05 += df[:].apply(lambda row: f'Missing value "{e}" for dimension {k} on '
                                                     f'row {":".join(map(str, row.values))} for dataset {dsd.id}',
                                         axis=1).tolist()
            elif k in codelist_values.keys() and str(e) not in codelist_values[k]:
                df = data[data[k] == e]
                list_ss04 += df[:].apply(lambda row: f'Wrong value "{e}" for dimension {k} '
                                                     f'on row {":".join(map(str, row.values))} for dataset {dsd.id}',
                                         axis=1).tolist()

        facets = False

    for k in dsd.attributeCodes:

        if dsd.attributeDescriptor.components[k].localRepresentation is not None:
            if len(dsd.attributeDescriptor.components[k].localRepresentation.facets) > 0:
                facets = True

        if k not in data.keys():
            if k in mandatory:
                list_ss03.append(f'Missing attribute {k} on dataset {dsd.id}')
            continue
        values = data[k].unique()
        for e in values:
            if facets:
                list_ss08 += check_facets(dsd.attributeDescriptor.components[k].localRepresentation.facets, e, dsd,
                                          k, 'Attribute')

            if e is np.nan or e is 'nan' or e is 'None' or e is None:
                if k in mandatory:
                    df = data[data[k] == np.nan]
                    list_ss06 += df[:].apply(lambda row: f'Missing value for attribute {k} on row '
                                                         f'{":".join(map(str, row.values))} for dataset {dsd.id}',
                                             axis=1).tolist()
            elif k in codelist_values.keys() and str(e) not in codelist_values[k]:
                df = data[data[k] == e]
                list_ss04 += df[:].apply(lambda row: f'Wrong value "{e}" for attribute {k} '
                                                     f'on row {":".join(map(str, row.values))} for dataset {dsd.id}',
                                         axis=1).tolist()

    grouping_keys = []
    for e in dsd.dimensionCodes:
        if e in data.keys():
            grouping_keys.append(e)

    grouping_keys.append('OBS_VALUE')
    duplicateRowsDF = data[data.duplicated(subset=grouping_keys)][grouping_keys]

    if len(duplicateRowsDF) > 0:
        list_ss07 += duplicateRowsDF[grouping_keys].apply(lambda row: parse_datapoint(row, dsd), axis=1).tolist()

    # Dictionary creation with key as each code and value the list of errors related
    errors = {}
    if len(list_ss01) > 0:
        errors['SS01'] = list_ss01
    if len(list_ss02) > 0:
        errors['SS02'] = list_ss02
    if len(list_ss03) > 0:
        errors['SS03'] = list_ss03
    if len(list_ss04) > 0:
        errors['SS04'] = list_ss04
    if len(list_ss05) > 0:
        errors['SS05'] = list_ss05
    if len(list_ss06) > 0:
        errors['SS06'] = list_ss06
    if len(list_ss07) > 0:
        errors['SS07'] = list_ss07
    if len(list_ss08) > 0:
        errors['SS08'] = list_ss08
    return errors
