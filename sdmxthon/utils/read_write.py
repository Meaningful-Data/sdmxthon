import logging
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd

from ..common.dataSet import DataSet
from ..message.generic import GenericDataType, StructureSpecificDataType
from ..model.structure import PrimaryMeasure
from ..utils.creators import id_creator
from ..utils.enums import DatasetType
from ..utils.xml_base import GdsCollector_, get_required_ns_prefix_defs, parsexml_, makeWarnings

try:
    from lxml import etree as etree
except ImportError:
    from xml.etree import ElementTree as etree

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)


def load_AllDimensions(inFileName, print_warnings=True, datasetType=DatasetType.GenericDataSet):
    # TODO Check if the message has been loaded correctly

    global CapturedNsmap_
    gds_collector = GdsCollector_()

    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    if datasetType == DatasetType.GenericDataSet or datasetType == DatasetType.GenericTimeSeriesDataSet:
        rootTag = 'GenericData'
        rootClass = GenericDataType
    elif datasetType == DatasetType.StructureDataSet or datasetType == DatasetType.StructureTimeSeriesDataSet:
        rootTag = 'StructureSpecificData'
        rootClass = StructureSpecificDataType
    else:
        return None
    rootObj = rootClass.factory()
    rootObj.original_tag_name_ = rootTag
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    rootObj._namespace_def = namespacedefs
    makeWarnings(print_warnings, gds_collector)

    return rootObj


def save_AllDimensions(message, path='', print_warnings=True):
    if path != '':
        f = open(path, "w")
        message.export(f, 0, pretty_print=True, has_parent=False)
        gds_collector = message.gds_collector_
        makeWarnings(print_warnings, gds_collector)
        f.close()
        return None
    else:
        f = StringIO()
        message.export(f, 0, pretty_print=True, has_parent=False)
        return f


def sdmxStrToDataset(xmlObj, dsd_dict) -> []:
    datasets = {}
    refs_data = {}

    for i in xmlObj.Header._structure:
        refs_data[i.gds_element_tree_node_.attrib['structureID']] = id_creator(i._ref._agencyID, i._ref._id,
                                                                               i._ref._version)

    for e in xmlObj.DataSet:
        strRef = e._structureRef

        if strRef is None:
            strRef = e.gds_element_tree_node_.attrib[
                '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific}structureRef']
            if strRef is None:
                # TODO Warning Structure Ref not found
                continue
        if refs_data[strRef] not in dsd_dict:
            # TODO Warning DSD not found
            print(refs_data[strRef])
            print(dsd_dict.keys())
            continue
        dsd = dsd_dict[refs_data[strRef]]

        attached_attributes_keys = dsd.datasetAttributeCodes

        dataset_attributes_keys = ['reportingBegin', 'reportingEnd', 'dataExtractionDate', 'validFrom',
                                   'validTo', 'publicationYear', 'publicationPeriod']
        item = DataSet(dsd)
        obsDict = {}

        dataset_attributes = {}

        # Default Attributes
        dataset_attributes['reportingBegin'] = None
        dataset_attributes['reportingEnd'] = None
        dataset_attributes['dataExtractionDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        dataset_attributes['validFrom'] = None
        dataset_attributes['validTo'] = None
        dataset_attributes['publicationYear'] = None
        dataset_attributes['publicationPeriod'] = None

        dataset_attributes['action'] = e._action
        dataset_attributes['setId'] = dsd.id

        dimObs = ''

        for j in xmlObj.Header._structure:
            if j.gds_element_tree_node_.attrib['structureID'] == strRef \
                    and j.gds_element_tree_node_.attrib['dimensionAtObservation']:
                dimObs = j.gds_element_tree_node_.attrib['dimensionAtObservation']

        if dimObs == '':
            dataset_attributes['dimensionAtObservation'] = 'AllDimensions'
        else:
            dataset_attributes['dimensionAtObservation'] = dimObs

        item.datasetAttributes = dataset_attributes.copy()

        attached_attributes = {}

        for key, value in e.gds_element_tree_node_.attrib.items():
            if key in attached_attributes_keys:
                attached_attributes[key] = value
            elif key in dataset_attributes_keys:
                dataset_attributes[key] = value

        item.attachedAttributes = attached_attributes

        obs_attributes_keys = []
        for record in dsd.attributeDescriptor.components.values():
            if record.relatedTo is not None and isinstance(record.relatedTo, PrimaryMeasure):
                obs_attributes_keys.append(record.id)

        if len(e._Series) > 0:
            series = {}
            for i in e._Series:
                series_key = {}
                for key, value in i.gds_element_tree_node_.attrib.items():
                    series_key[key] = value
                for k in i._obs:
                    list_keys = []
                    for key, value in series_key.items():
                        if key in series.keys():
                            series[key].append(value)
                        else:
                            series[key] = [value]
                    for key, value in k.gds_element_tree_node_.attrib.items():
                        list_keys.append(key)
                        if key in series.keys():
                            series[key].append(value)
                        else:
                            series[key] = [value]
                    for o in obs_attributes_keys:
                        if o not in list_keys:
                            text = np.nan
                            if o in series.keys():
                                series[o].append(text)
                            else:
                                series[o] = [text]
            check_empty(series)
            item.data = pd.DataFrame.from_dict(series)
        elif len(e._obs) > 0:
            for i in e._obs:
                list_keys = []
                for key, value in i.gds_element_tree_node_.attrib.items():
                    list_keys.append(key)
                    if key in obsDict.keys():
                        obsDict[key].append(value)
                    else:
                        obsDict[key] = [value]

                for o in obs_attributes_keys:
                    if o not in list_keys:
                        text = np.nan
                        if o in obsDict.keys():
                            obsDict[o].append(text)
                        else:
                            obsDict[o] = [text]
            check_empty(obsDict)
            item.data = pd.DataFrame.from_dict(obsDict.copy())
        datasets[dsd.id] = item
    del xmlObj
    return datasets


def check_empty(series: dict):
    temp_series = series.copy()
    for key, list in temp_series.items():
        if all(e is np.nan for e in list):
            series.pop(key)


def check_length(series: dict):
    length = -1
    key_ref = ''
    for key, list in series.items():
        if length == -1:
            length = len(list)
            key_ref = key
        elif length != len(list):
            # All series must be on same size
            print('Key: %s ---- length: %d ---- expected length: %d from key %s' % (key, len(list), length, key_ref))


def sdmxGenToDataSet(xmlObj, dsd_dict) -> []:
    datasets = {}
    refs_data = {}

    for i in xmlObj.Header._structure:
        refs_data[i.gds_element_tree_node_.attrib['structureID']] = id_creator(i._ref._agencyID, i._ref._id,
                                                                               i._ref._version)
    for e in xmlObj.DataSet:
        if refs_data[e._structureRef] not in dsd_dict:
            # TODO Warning DSD not found
            continue
        dsd = dsd_dict[refs_data[e._structureRef]]
        item = DataSet(dsd)

        attached_attributes_keys = dsd.datasetAttributeCodes

        dataset_attributes = {}

        dataset_attributes['reportingBegin'] = e._reportingBeginDate
        dataset_attributes['reportingEnd'] = e._reportingEndDate
        dataset_attributes['dataExtractionDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        dataset_attributes['validFrom'] = e._validFromDate
        dataset_attributes['validTo'] = e._validToDate
        dataset_attributes['publicationYear'] = e._publicationYear
        dataset_attributes['publicationPeriod'] = e._publicationPeriod

        dataset_attributes['action'] = e._action
        dataset_attributes['setId'] = dsd.id
        dimObs = ''

        for j in xmlObj.Header._structure:
            if j.gds_element_tree_node_.attrib['structureID'] == e._structureRef and j.gds_element_tree_node_.attrib[
                'dimensionAtObservation']:
                dimObs = j.gds_element_tree_node_.attrib['dimensionAtObservation']

        if dimObs == '':
            dataset_attributes['dimensionAtObservation'] = 'AllDimensions'
        else:
            dataset_attributes['dimensionAtObservation'] = dimObs

        item.datasetAttributes = dataset_attributes.copy()

        attached_attributes = {}
        if e._Attributes is not None:
            for i in e._Attributes.Value:
                key = i.gds_element_tree_node_.attrib.get('id')
                value = i.gds_element_tree_node_.attrib.get('value')
                if key in attached_attributes_keys:
                    attached_attributes[key] = value

        item.attachedAttributes = attached_attributes.copy()

        if len(e._Series) > 0:
            obs_attributes_keys = []
            for record in dsd.attributeDescriptor.components.values():
                if record.relatedTo is not None and isinstance(record.relatedTo, PrimaryMeasure):
                    obs_attributes_keys.append(record.id)
            series = {}
            for i in e._Series:
                series_key = {}

                if i._Attributes is not None:
                    for m in i._Attributes.Value:
                        key = m.gds_element_tree_node_.attrib.get('id')
                        value = m.gds_element_tree_node_.attrib.get('value')
                        series_key[key] = value

                for j in i.SeriesKey.Value:
                    key = j.gds_element_tree_node_.attrib.get('id')
                    value = j.gds_element_tree_node_.attrib.get('value')
                    series_key[key] = value
                for k in i._obs:
                    list_keys = []

                    for key, value in series_key.items():
                        list_keys.append(key)
                        if key in series.keys():
                            series[key].append(value)
                        else:
                            series[key] = [value]

                    key = 'OBS_VALUE'
                    value = k.ObsValue.gds_element_tree_node_.attrib.get('value')
                    list_keys.append(key)
                    if key in series.keys():
                        series[key].append(value)
                    else:
                        series[key] = [value]

                    for m in k._Attributes.Value:
                        key = m.gds_element_tree_node_.attrib.get('id')
                        value = m.gds_element_tree_node_.attrib.get('value')
                        list_keys.append(key)
                        if key in series.keys():
                            series[key].append(value)
                        else:
                            series[key] = [value]

                    for o in obs_attributes_keys:
                        if o not in list_keys:
                            text = np.nan
                            if o in series.keys():
                                series[o].append(text)
                            else:
                                series[o] = [text]
            check_empty(series)
            item.data = pd.DataFrame.from_dict(series)
        elif len(e._obs) > 0:
            obsDict = {}
            obs_attributes_keys = []
            for record in dsd.attributeCodes:
                if record not in dsd.dimensionCodes:
                    obs_attributes_keys.append(record)
            for j in e._obs:
                list_keys = []
                for k in j._Attributes.Value:
                    key = k._id
                    value = k._value
                    list_keys.append(key)
                    if key in obsDict.keys():
                        obsDict[key].append(value)
                    else:
                        obsDict[key] = [value]
                for n in j.ObsKey.Value:
                    key = n._id
                    value = n._value
                    list_keys.append(key)

                    if key in obsDict.keys():
                        obsDict[key].append(value)
                    else:
                        obsDict[key] = [value]
                if j.ObsValue is not None:
                    for key, value in j.ObsValue.gds_element_tree_node_.attrib.items():
                        key = 'OBS_VALUE'
                        list_keys.append(key)
                        if key in obsDict.keys():
                            obsDict[key].append(value)
                        else:
                            obsDict[key] = [value]
                for o in obs_attributes_keys:
                    if o not in list_keys:
                        text = np.nan
                        if o in obsDict.keys():
                            obsDict[o].append(text)
                        else:
                            obsDict[o] = [text]
            check_empty(obsDict)
            item.data = pd.DataFrame.from_dict(obsDict.copy())
        datasets[dsd.id] = item
    del xmlObj
    return datasets
