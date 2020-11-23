"""
Created on 15 jul. 2020

@author: ruben
"""
import logging
from datetime import datetime
from io import StringIO

import pandas as pd

from SDMXThon.common.dataSet import DataSet
from SDMXThon.message.generic import GenericDataType, StructureSpecificDataType
from SDMXThon.utils.enums import DatasetType
from SDMXThon.utils.parsers import get_dataset_attributes, get_agency_id, get_version
from SDMXThon.utils.xml_base import GdsCollector_, get_required_ns_prefix_defs, parsexml_, makeWarnings

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
        return
    rootObj = rootClass.factory()
    rootObj.original_tag_name_ = rootTag
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    rootObj._namespace_def = namespacedefs
    makeWarnings(print_warnings, gds_collector)

    return rootObj


def save_AllDimensions(message, path='', print_warnings=True):
    if path == '':
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


def sdmxStrToPandas(xmlObj, path_to_metadata, index='DMID') -> []:
    dataSetList = []
    root = etree.parse(path_to_metadata)
    for e in xmlObj.DataSet:
        attached_attributes_keys = get_dataset_attributes(root, e._structureRef).keys()
        dataset_attributes_keys = ['reportingBegin', 'reportingEnd', 'dataExtractionDate', 'validFrom',
                                   'validTo', 'publicationYear', 'publicationPeriod']
        item = DataSet()
        obsDict = {}

        # Setting structureRef attributes
        item.code = e._structureRef
        item.version = get_version(root, item.code)
        item.agencyID = str(get_agency_id(root))

        # Default Attributes
        item.dataset_attributes['reportingBegin'] = None
        item.dataset_attributes['reportingEnd'] = None
        item.dataset_attributes['dataExtractionDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        item.dataset_attributes['validFrom'] = None
        item.dataset_attributes['validTo'] = None
        item.dataset_attributes['publicationYear'] = None
        item.dataset_attributes['publicationPeriod'] = None

        item.dataset_attributes['action'] = e._action
        item.dataset_attributes['setId'] = e._structureRef
        item.dataset_attributes['dimensionAtObservation'] = 'AllDimensions'

        length = -1
        for key, value in e.gds_element_tree_node_.attrib.items():
            if key in attached_attributes_keys:
                item.attached_attributes[key] = value
            elif key in dataset_attributes_keys:
                item.dataset_attributes[key] = value
        for i in e._obs:
            if length == -1:
                length = len(i.gds_element_tree_node_.attrib)
            else:
                if len(i.gds_element_tree_node_.attrib) != length:
                    print("Wrong number of attributes in index: %s" % (i.gds_element_tree_node_.attrib[index]))
                    return []
            for key, value in i.gds_element_tree_node_.attrib.items():
                if key in obsDict.keys():
                    obsDict[key].append(value)
                else:
                    obsDict[key] = [value]

        item.obs = pd.DataFrame.from_dict(obsDict.copy())
        dataSetList.append(item)

    return dataSetList


def sdmxGenToPandas(xmlObj, path_to_metadata, index="DMID") -> []:
    dataSetList = []
    root = etree.parse(path_to_metadata)
    for e in xmlObj.DataSet:
        item = DataSet()
        obsDict = {}

        item.code = e._structureRef

        attached_attributes_keys = get_dataset_attributes(root, e._structureRef).keys()

        # Default Attributes
        item.version = get_version(root, item.code)
        item.agencyID = str(get_agency_id(root))

        item.dataset_attributes['reportingBegin'] = e._reportingBeginDate
        item.dataset_attributes['reportingEnd'] = e._reportingEndDate
        item.dataset_attributes['dataExtractionDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        item.dataset_attributes['validFrom'] = e._validFromDate
        item.dataset_attributes['validTo'] = e._validToDate
        item.dataset_attributes['publicationYear'] = e._publicationYear
        item.dataset_attributes['publicationPeriod'] = e._publicationPeriod

        item.dataset_attributes['action'] = e._action
        item.dataset_attributes['setId'] = e._structureRef
        if e._Attributes is not None:
            for i in e._Attributes.Value:
                key = i.gds_element_tree_node_.attrib.get('id')
                value = i.gds_element_tree_node_.attrib.get('value')
                if key in attached_attributes_keys:
                    item.attached_attributes[key] = value

        if len(e._Series) > 0:
            series = {}
            for i in e._Series:
                series_key = {}
                for j in i.SeriesKey.Value:
                    key = j.gds_element_tree_node_.attrib.get('id')
                    value = j.gds_element_tree_node_.attrib.get('value')
                    series_key[key] = value

                for k in i._obs:
                    for key, value in series_key.items():
                        if key in series.keys():
                            series[key].append(value)
                        else:
                            series[key] = [value]
                    # Change for dimensionAtObservation
                    key = 'OBS_DIMENSION'
                    value = k.ObsDimension.gds_element_tree_node_.attrib.get('value')
                    if key in series.keys():
                        series[key].append(value)
                    else:
                        series[key] = [value]
                    key = 'OBS_VALUE'
                    value = k.ObsValue.gds_element_tree_node_.attrib.get('value')
                    if key in series.keys():
                        series[key].append(value)
                    else:
                        series[key] = [value]

            item.obs = pd.DataFrame.from_dict(series)
        elif len(e._obs) > 0:
            for j in e._obs:
                for k in j._Attributes.Value:
                    key = k._id
                    value = k._value
                    if key in obsDict.keys():
                        obsDict[key].append(value)
                    else:
                        obsDict[key] = [value]
                for n in j.ObsKey.Value:
                    key = n._id
                    value = n._value
                    if key in obsDict.keys():
                        obsDict[key].append(value)
                    else:
                        obsDict[key] = [value]
                if j.ObsValue is not None:
                    for key, value in j.ObsValue.gds_element_tree_node_.attrib.items():
                        key = 'OBS_VALUE'
                        if key in obsDict.keys():
                            obsDict[key].append(value)
                        else:
                            obsDict[key] = [value]

            item.obs = pd.DataFrame.from_dict(obsDict)
        dataSetList.append(item)

    return dataSetList
