import numpy as np
import pandas as pd
from lxml import etree

from SDMXThon import getMetadata, DataSet
from SDMXThon.model.structure import DataStructureDefinition


def read_Generic(pathData, pathMetadata):
    dsds = getMetadata(pathMetadata)

    listRef = {}
    context = etree.iterparse(pathData, tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure')
    for event, elem in context:
        structureRef = elem.attrib['structureID']
        dimObs = elem.attrib['dimensionAtObservation']
        if elem[0].tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Structure':
            if elem[0][0].tag == 'Ref':
                data = elem[0][0]
                listRef[structureRef] = [f'{data.attrib["agencyID"]}:{data.attrib["id"]}({data.attrib["version"]})',
                                         dimObs]

    datasets = {}

    for event, elem in etree.iterparse(pathData,
                                       tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet'):
        if elem.attrib['structureRef'] not in listRef.keys():
            # TODO Structure not found from structureRef
            continue

        id_ = listRef.get(elem.attrib['structureRef'])[0]
        dimObs = listRef.get(elem.attrib['structureRef'])[1]
        if id_ not in dsds.keys():
            # TODO DSD not found for id_
            continue

        dataset = DataSet(dsds[id_])
        attachedAtData = {}
        valuesDict = {}
        for child in elem:
            if child.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes':
                for data in child.getchildren():
                    k = data.attrib['id']
                    v = data.attrib['value']
                    attachedAtData[k] = v
                dataset.attachedAttributes = attachedAtData
            elif child.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs':
                for obs in child.getchildren():
                    if len(obs.attrib) > 0:
                        k = 'OBS_VALUE'
                        v = obs.attrib['value']
                        if k in valuesDict.keys():
                            valuesDict[k] = np.append(valuesDict[k], v)
                        else:
                            valuesDict[k] = np.array(v)
                    else:
                        for data in obs.getchildren():
                            k = data.attrib['id']
                            v = data.attrib['value']
                            if k in valuesDict.keys():
                                valuesDict[k] = np.append(valuesDict[k], v)
                            else:
                                valuesDict[k] = np.array(v)
                            data.clear()

                    obs.clear()
            elif dimObs != 'AllDimensions' and child.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series':
                for series in child.getchildren():
                    if series.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs':
                        for data in series.getchildren():
                            if data.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue':
                                k = 'OBS_VALUE'
                                v = data.attrib['value']
                                if k in valuesDict.keys():
                                    valuesDict[k] = np.append(valuesDict[k], v)
                                else:
                                    valuesDict[k] = np.array(v)
                            elif data.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension':
                                k = dimObs
                                v = data.attrib['value']
                                if k in valuesDict.keys():
                                    valuesDict[k] = np.append(valuesDict[k], v)
                                else:
                                    valuesDict[k] = np.array(v)
                            elif data.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes':
                                for attr in data.getchildren():
                                    k = attr.attrib['id']
                                    v = attr.attrib['value']
                                    if k in valuesDict.keys():
                                        valuesDict[k] = np.append(valuesDict[k], v)
                                    else:
                                        valuesDict[k] = np.array(v)
                            data.clear()
                    elif series.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes' or series.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}SeriesKey':
                        for data in series.getchildren():
                            k = data.attrib['id']
                            v = data.attrib['value']
                            if k in valuesDict.keys():
                                valuesDict[k] = np.append(valuesDict[k], v)
                            else:
                                valuesDict[k] = np.array(v)
                            data.clear()

            child.clear()
        if len(valuesDict) > 0:
            dataset.data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in valuesDict.items()]))
            del valuesDict
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

    listRef = {}
    context = etree.iterparse(pathData, tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure')
    for event, elem in context:
        structureRef = elem.attrib['structureID']
        dimObs = elem.attrib['dimensionAtObservation']
        if elem[0].tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Structure':
            if elem[0][0].tag == 'Ref':
                data = elem[0][0]
                listRef[structureRef] = [f'{data.attrib["agencyID"]}:{data.attrib["id"]}({data.attrib["version"]})',
                                         dimObs]

    datasets = {}

    for event, elem in etree.iterparse(pathData,
                                       tag='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet'):
        if elem.attrib['structureRef'] not in listRef.keys():
            # TODO Structure not found from structureRef
            continue

        id_ = listRef.get(elem.attrib['structureRef'])[0]
        dimObs = listRef.get(elem.attrib['structureRef'])[1]
        if id_ not in dsds.keys():
            # TODO DSD not found for id_
            continue
        dsd: DataStructureDefinition = dsds[id_]
        dataset = DataSet(dsd)
        attachedAtData = {}
        valuesDict = {}
        for k, v in dict(elem.attrib).items():
            if k in dsd.datasetAttributeCodes:
                attachedAtData[k] = v

        for child in elem:
            if dimObs != 'AllDimensions' and child.tag == 'Series':
                seriesKey = {}
                for k, v in dict(child.attrib).items():
                    if k not in seriesKey.keys():
                        seriesKey[k] = v
                    else:
                        # TODO Two dimensions specified on series (structure validations)
                        continue
                for data in child:
                    for k, v in seriesKey.items():
                        if k in valuesDict.keys():
                            valuesDict[k] = np.append(valuesDict[k], v)
                        else:
                            valuesDict[k] = np.array(v)
                    for k, v in dict(data.attrib).items():
                        if k in valuesDict.keys():
                            valuesDict[k] = np.append(valuesDict[k], v)
                        else:
                            valuesDict[k] = np.array(v)

            elif child.tag == 'Obs':
                for k, v in dict(child.attrib).items():
                    if k in valuesDict.keys():
                        valuesDict[k] = np.append(valuesDict[k], v)
                    else:
                        valuesDict[k] = np.array(v)

        if len(valuesDict) > 0:
            dataset.data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in valuesDict.items()]))
            del valuesDict
            datasets[dataset.structure.id] = dataset

    if len(datasets) == 1:
        values_view = datasets.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        return first_value
    else:
        return datasets
