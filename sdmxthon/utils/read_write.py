import logging
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd

from ..common.dataSet import DataSet
from ..message.generic import GenericDataType, StructureSpecificDataType
from ..utils.enums import DatasetType
from ..utils.parsers import id_creator
from ..utils.xml_base import GdsCollector_, get_required_ns_prefix_defs, parsexml_, makeWarnings

try:
    from lxml import etree as etree_, etree
except ImportError:
    from xml.etree import ElementTree as etree_, etree

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
    if datasetType == DatasetType.GenericDataSet:
        rootTag = 'GenericData'
        rootClass = GenericDataType
    elif datasetType == DatasetType.StructureDataSet:
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


def sdmxStrToPandas(xmlObj, dsd_dict) -> []:
    dataSetList = []
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
        item = DataSet()
        obsDict = {}

        # Setting structureRef attributes
        item.code = strRef
        item.version = dsd.version
        item.agencyID = dsd.agencyId

        # Default Attributes
        item.dataset_attributes['reportingBegin'] = None
        item.dataset_attributes['reportingEnd'] = None
        item.dataset_attributes['dataExtractionDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        item.dataset_attributes['validFrom'] = None
        item.dataset_attributes['validTo'] = None
        item.dataset_attributes['publicationYear'] = None
        item.dataset_attributes['publicationPeriod'] = None

        item.dataset_attributes['action'] = e._action
        item.dataset_attributes['setId'] = dsd.id

        dimObs = ''
        """
        for j in xmlObj.Header._structure:
            if j.gds_element_tree_node_.attrib['structureID'] == strRef \
                    and j.gds_element_tree_node_.attrib['dimensionAtObservation']:
                dimObs = j.gds_element_tree_node_.attrib['dimensionAtObservation']
        """
        if dimObs == '':
            item.dataset_attributes['dimensionAtObservation'] = 'AllDimensions'
        else:
            item.dataset_attributes['dimensionAtObservation'] = dimObs

        for key, value in e.gds_element_tree_node_.attrib.items():
            if key in attached_attributes_keys:
                item.attached_attributes[key] = value
            elif key in dataset_attributes_keys:
                item.dataset_attributes[key] = value

        if len(e._Series) > 0:
            series = {}
            obs_attributes_keys = []
            for record in dsd.attributeCodes:
                if record not in dsd.dimensionCodes:
                    obs_attributes_keys.append(record)
            for i in e._Series:
                series_key = {}
                for key, value in i.gds_element_tree_node_.attrib.items():
                    series_key[key] = value
                for k in i._obs:
                    list_keys = []
                    for key, value in series_key.items():
                        list_keys.append(key)
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
            item.obs = pd.DataFrame.from_dict(series)
        elif len(e._obs) > 0:
            for i in e._obs:
                for key, value in i.gds_element_tree_node_.attrib.items():
                    if key in obsDict.keys():
                        obsDict[key].append(value)
                    else:
                        obsDict[key] = [value]
            item.obs = pd.DataFrame.from_dict(obsDict.copy())
        dataSetList.append(item)

    return dataSetList


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
    dataSetList = []
    refs_data = {}

    for i in xmlObj.Header._structure:
        refs_data[i.gds_element_tree_node_.attrib['structureID']] = id_creator(i._ref._agencyID, i._ref._id,
                                                                               i._ref._version)
    for e in xmlObj.DataSet:
        if refs_data[e._structureRef] not in dsd_dict:
            # TODO Warning DSD not found
            continue
        dsd = dsd_dict[refs_data[e._structureRef]]
        item = DataSet()

        item.code = e._structureRef

        attached_attributes_keys = dsd.datasetAttributeCodes

        # Default Attributes
        item.version = dsd.version
        item.agencyID = dsd.agencyId

        item.dataset_attributes['reportingBegin'] = e._reportingBeginDate
        item.dataset_attributes['reportingEnd'] = e._reportingEndDate
        item.dataset_attributes['dataExtractionDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        item.dataset_attributes['validFrom'] = e._validFromDate
        item.dataset_attributes['validTo'] = e._validToDate
        item.dataset_attributes['publicationYear'] = e._publicationYear
        item.dataset_attributes['publicationPeriod'] = e._publicationPeriod

        item.dataset_attributes['action'] = e._action
        item.dataset_attributes['setId'] = dsd.id
        dimObs = ''
        """
        for j in xmlObj.Header._structure:
            if j.gds_element_tree_node_.attrib['structureID'] == e._structureRef and j.gds_element_tree_node_.attrib[
                'dimensionAtObservation']:
                dimObs = j.gds_element_tree_node_.attrib['dimensionAtObservation']
        """
        if dimObs == '':
            item.dataset_attributes['dimensionAtObservation'] = 'AllDimensions'
        else:
            item.dataset_attributes['dimensionAtObservation'] = dimObs

        if e._Attributes is not None:
            for i in e._Attributes.Value:
                key = i.gds_element_tree_node_.attrib.get('id')
                value = i.gds_element_tree_node_.attrib.get('value')
                if key in attached_attributes_keys:
                    item.attached_attributes[key] = value

        if len(e._Series) > 0:
            series = {}
            obs_attributes_keys = []
            for record in dsd.attributeCodes:
                if record not in dsd.dimensionCodes:
                    obs_attributes_keys.append(record)

            for i in e._Series:
                series_key = {}

                if i._Attributes is not None:
                    for m in i._Attributes.Value:
                        key = m.gds_element_tree_node_.attrib.get('id')
                        value = m.gds_element_tree_node_.attrib.get('value')
                        if key in obs_attributes_keys:
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

                    key = item.dataset_attributes['dimensionAtObservation']
                    value = k.ObsDimension.gds_element_tree_node_.attrib.get('value')
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
            item.obs = pd.DataFrame.from_dict(series)
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
                        if o in dsd.dimensionCodes:
                            # TODO Warning missing dimension information
                            print(j)
                        if o in obsDict.keys():
                            obsDict[o].append(text)
                        else:
                            obsDict[o] = [text]
            check_empty(obsDict)
            item.obs = pd.DataFrame.from_dict(obsDict.copy())
        dataSetList.append(item)

    return dataSetList
