import logging

import numpy as np
from pandas import DataFrame

from ..model.structure import DataStructureDefinition, Dimension

logger = logging.getLogger("logger")


def get_codelist_values(dsd: DataStructureDefinition) -> dict:
    data = {}

    if dsd.dimensionDescriptor.components is not None:

        for element in dsd.dimensionDescriptor.components.values():
            if element.localRepresentation.codeList is not None:
                data[element.id] = element.localRepresentation.codeList.items.keys()

    if dsd.attributeDescriptor.components is not None:
        for record in dsd.attributeDescriptor.components.values():
            if record.localRepresentation.codeList is not None:
                data[record.id] = record.localRepresentation.codeList.items.keys()

    return data


def get_mandatory_attributes(dsd: DataStructureDefinition) -> list:
    data = []

    if dsd.attributeDescriptor.components is None:
        return []

    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None and record.usageStatus == "Mandatory":
            if isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                data.append(record.id)

    return data


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
    """

    list_SS01 = []
    list_SS02 = []
    list_SS03 = []
    list_SS04 = []
    list_SS05 = []
    list_SS06 = []

    if 'OBS_VALUE' not in data.keys():
        list_SS02.append(f'Missing OBS_VALUE for dataset {dsd.id}')
    else:
        if data['OBS_VALUE'].isnull().values.any():
            # list_SS02.append(f'Missing values for OBS_VALUE for dataset {dsd.id}')
            df = data[data['OBS_VALUE'] == np.nan]
            list_SS02 += df[:].apply(lambda row: f'Missing value for OBS_VALUE on row {":".join(map(str, row.values))}'
                                                 f' for dataset {dsd.id}', axis=1).tolist()

    for k in dsd.dimensionCodes:
        if k not in data.keys():
            list_SS01.append(f'Missing dimension {k} on dataset {dsd.id}')
            continue
        values = data[k].unique()
        for e in values:
            if e == np.nan or str(e) == 'nan' or str(e) == 'None':
                # list_SS05.append(f'Missing values for dimension {k} for dataset {dsd.id}')
                df = data[data[k] == np.nan]
                list_SS05 += df[:].apply(lambda row: f'Missing value "{e}" for dimension {k} on '
                                                     f'row {":".join(map(str, row.values))} for dataset {dsd.id}',
                                         axis=1).tolist()
            elif k in codelist_values.keys() and str(e) not in codelist_values[k]:
                list_SS04.append(f'Wrong value "{e}" for dimension {k} for dataset {dsd.id}')
                df = data[data[k] == e]
                list_SS04 += df[:].apply(lambda row: f'Wrong value "{e}" for dimension {k} '
                                                     f'on row {":".join(map(str, row.values))} for dataset {dsd.id}',
                                         axis=1).tolist()

    for k in dsd.attributeCodes:
        if k not in data.keys():
            if k in mandatory:
                list_SS03.append(f'Missing attribute {k} on dataset {dsd.id}')
            continue
        values = data[k].unique()
        for e in values:
            if e is np.nan or e is 'nan' or e is 'None' or e is None:
                if k in mandatory:
                    # list_SS06.append(f'Missing values for attribute {k} for dataset {dsd.id}')
                    df = data[data[k] == np.nan]
                    list_SS06 += df[:].apply(lambda row: f'Missing value for attribute {k} on row '
                                                         f'{":".join(map(str, row.values))} for dataset {dsd.id}',
                                             axis=1).tolist()
            elif k in codelist_values.keys() and str(e) not in codelist_values[k]:
                # list_SS04.append(f'Wrong value "{e}" for attribute {k} for dataset {dsd.id}')
                df = data[data[k] == e]
                list_SS04 += df[:].apply(lambda row: f'Wrong value "{e}" for attribute {k} '
                                                     f'on row {":".join(map(str, row.values))} for dataset {dsd.id}',
                                         axis=1).tolist()

    # Dictionary creation with key as each code and value the list of errors related
    errors = {'SS01': list_SS01, 'SS02': list_SS02, 'SS03': list_SS03, 'SS04': list_SS04, 'SS05': list_SS05,
              'SS06': list_SS06}

    return errors
