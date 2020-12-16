import numpy as np
from pandas import DataFrame

from ..model.structure import DataStructureDefinition, Dimension


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
        if record.relatedTo is not None:
            if isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                data.append(record.id)

    return data


def validate_obs(data: DataFrame, dsd: DataStructureDefinition, validation_list, mandatory_attributes: list = None):
    if 'OBS_VALUE' not in data.keys():
        validation_list.append('SS02: Missing OBS_VALUE for dataset %s' % dsd.id)

    if mandatory_attributes is None:
        mandatory_attributes = get_mandatory_attributes(dsd)

    codelist_values: dict = get_codelist_values(dsd)

    iterations = len(data)

    for i in dsd.dimensionCodes:
        if i not in data.keys():
            validation_list.append('SS01: Missing dimension %s on dataset %s' % (i, dsd.id))

    for j in mandatory_attributes:
        if j not in data.keys():
            validation_list.append('SS03: Missing attribute %s on dataset %s' % (j, dsd.id))

    for k in data.keys():
        df = data[k]
        if k not in dsd.dimensionCodes and k not in dsd.attributeCodes:
            continue
        for row in range(iterations):
            aux = df[row]

            if aux == np.nan:
                row_data = ':'.join(map(str, data.loc[row, :].values.tolist()))
                if k in mandatory_attributes:
                    validation_list.append(
                        'SS06: Missing value for attribute %s on row %s for dataset %s' % (k, row_data, dsd.id))
                elif k in dsd.attributeCodes:
                    validation_list.append(
                        'SS04: Missing value for attribute %s on row %s for dataset %s' % (k, row_data, dsd.id))
                elif k == 'OBS_VALUE':
                    validation_list.append(
                        'SS02: Missing value for OBS_VALUE on row %s for dataset %s' % (row_data, dsd.id))
                else:
                    validation_list.append(
                        'SS05: Missing value for dimension %s on row %s for dataset %s' % (k, row_data, dsd.id))

            elif k in codelist_values.keys() and aux not in codelist_values[k]:
                row_data = ':'.join(map(str, data.loc[row, :].values.tolist()))
                if k in mandatory_attributes:
                    validation_list.append('SS06: Wrong value "%s" for attribute %s on row %s for dataset %s' %
                                           (aux, k, row_data, dsd.id))
                elif k in dsd.attributeCodes:
                    validation_list.append('SS04: Wrong value "%s" for attribute %s on row %s for dataset %s' %
                                           (aux, k, row_data, dsd.id))
                else:
                    validation_list.append('SS05: Wrong value "%s" for dimension %s on row %s for dataset %s' %
                                           (aux, k, row_data, dsd.id))
