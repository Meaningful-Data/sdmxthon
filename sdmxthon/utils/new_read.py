"""
import numpy as np
import pandas as pd
from lxml import etree

from SDMXThon import getMetadata, DataSet
from SDMXThon.model.structure import DataStructureDefinition


def read_Generic(pathData, pathMetadata):
    dsds = getMetadata(pathMetadata)

    list_ref = {}
    context = etree.iterparse(pathData, tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure')
    for event, elem in context:
        structure_ref = elem.attrib['structureID']
        dim_obs = elem.attrib['dimensionAtObservation']
        if elem[0].tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Structure':
            if elem[0][0].tag == 'Ref':
                data = elem[0][0]
                list_ref[structure_ref] = [f'{data.attrib["agencyID"]}:{data.attrib["id_"]}({data.attrib["version"]})',
                                           dim_obs]

    datasets = {}

    for event, elem in etree.iterparse(pathData,
                                       tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet'):
        if elem.attrib['structureRef'] not in list_ref.keys():
            # TODO Structure not found from structureRef
            continue

        id_ = list_ref.get(elem.attrib['structureRef'])[0]
        dim_obs = list_ref.get(elem.attrib['structureRef'])[1]
        if id_ not in dsds.keys():
            # TODO DSD not found for id_
            continue

        dataset = DataSet(dsds[id_])
        attached_at_data = {}
        values_dict = {}
        for child in elem:
            if child.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes':
                for data in child.getchildren():
                    k = data.attrib['id']
                    v = data.attrib['value']
                    attached_at_data[k] = v
                dataset.attachedAttributes = attached_at_data
            elif child.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs':
                for obs in child.getchildren():
                    if len(obs.attrib) > 0:
                        k = 'OBS_VALUE'
                        v = obs.attrib['value']
                        if k in values_dict.keys():
                            values_dict[k] = np.append(values_dict[k], v)
                        else:
                            values_dict[k] = np.array(v)
                    else:
                        for data in obs.getchildren():
                            k = data.attrib['id']
                            v = data.attrib['value']
                            if k in values_dict.keys():
                                values_dict[k] = np.append(values_dict[k], v)
                            else:
                                values_dict[k] = np.array(v)
                            data.clear()

                    obs.clear()
            elif dim_obs != 'AllDimensions' \
                    and child.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series':
                for series in child.getchildren():
                    if series.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs':
                        for data in series.getchildren():
                            if data.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue':
                                k = 'OBS_VALUE'
                                v = data.attrib['value']
                                if k in values_dict.keys():
                                    values_dict[k] = np.append(values_dict[k], v)
                                else:
                                    values_dict[k] = np.array(v)
                            elif data.tag == \
                                    '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension':
                                k = dim_obs
                                v = data.attrib['value']
                                if k in values_dict.keys():
                                    values_dict[k] = np.append(values_dict[k], v)
                                else:
                                    values_dict[k] = np.array(v)
                            elif data.tag == \
                                    '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes':
                                for attr in data.getchildren():
                                    k = attr.attrib['id']
                                    v = attr.attrib['value']
                                    if k in values_dict.keys():
                                        values_dict[k] = np.append(values_dict[k], v)
                                    else:
                                        values_dict[k] = np.array(v)
                            data.clear()
                    elif series.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes' \
                            or series.tag == \
                            '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}SeriesKey':
                        for data in series.getchildren():
                            k = data.attrib['id']
                            v = data.attrib['value']
                            if k in values_dict.keys():
                                values_dict[k] = np.append(values_dict[k], v)
                            else:
                                values_dict[k] = np.array(v)
                            data.clear()

            child.clear()
        if len(values_dict) > 0:
            dataset.data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in values_dict.items()]))
            del values_dict
            datasets[dataset.structure.id] = dataset

    if len(datasets) == 1:
        values_view = datasets.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        return first_value
    else:
        return datasets


def read_Structure(pathData, pathMetadata):
    dsds = getMetadata(pathMetadata)

    list_ref = {}
    context = etree.iterparse(pathData, tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure')
    for event, elem in context:
        structure_ref = elem.attrib['structureID']
        dim_obs = elem.attrib['dimensionAtObservation']
        if elem[0].tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Structure':
            if elem[0][0].tag == 'Ref':
                data = elem[0][0]
                list_ref[structure_ref] = [f'{data.attrib["agencyID"]}:{data.attrib["id_"]}({data.attrib["version"]})',
                                           dim_obs]

    datasets = {}

    for event, elem in etree.iterparse(pathData,
                                       tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet'):
        if elem.attrib['structureRef'] not in list_ref.keys():
            # TODO Structure not found from structureRef
            continue

        id_ = list_ref.get(elem.attrib['structureRef'])[0]
        dim_obs = list_ref.get(elem.attrib['structureRef'])[1]
        if id_ not in dsds.keys():
            # TODO DSD not found for id_
            continue
        dsd: DataStructureDefinition = dsds[id_]
        dataset = DataSet(dsd)
        attached_at_data = {}
        values_dict = {}
        for k, v in dict(elem.attrib).items():
            if k in dsd.datasetAttributeCodes:
                attached_at_data[k] = v

        for child in elem:
            if dim_obs != 'AllDimensions' and child.tag == 'Series':
                series_key = {}
                for k, v in dict(child.attrib).items():
                    if k not in series_key.keys():
                        series_key[k] = v
                    else:
                        # TODO Two dimensions specified on series (structure validations)
                        continue
                for data in child:
                    for k, v in series_key.items():
                        if k in values_dict.keys():
                            values_dict[k] = np.append(values_dict[k], v)
                        else:
                            values_dict[k] = np.array(v)
                    for k, v in dict(data.attrib).items():
                        if k in values_dict.keys():
                            values_dict[k] = np.append(values_dict[k], v)
                        else:
                            values_dict[k] = np.array(v)

            elif child.tag == 'Obs':
                for k, v in dict(child.attrib).items():
                    if k in values_dict.keys():
                        values_dict[k] = np.append(values_dict[k], v)
                    else:
                        values_dict[k] = np.array(v)

        if len(values_dict) > 0:
            dataset.data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in values_dict.items()]))
            del values_dict
            datasets[dataset.structure.id] = dataset

    if len(datasets) == 1:
        values_view = datasets.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        return first_value
    else:
        return datasets
"""
