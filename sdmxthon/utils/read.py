import logging
from datetime import datetime

import numpy as np
import pandas as pd

from ..common.dataSet import DataSet
from ..message.generic import GenericDataType, StructureSpecificDataType, MetadataType
from ..model.structure import PrimaryMeasure
from ..utils.metadata_parsers import id_creator
from ..utils.xml_base import GdsCollector, get_required_ns_prefix_defs, parse_xml, makeWarnings

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

GenericDataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}GenericData'
StructureDataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}StructureSpecificData'
MetadataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure'

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)


def readXML(inFileName, print_warning=True):
    # TODO Check if the message has been loaded correctly

    global CapturedNsmap_
    gds_collector = GdsCollector()

    parser = None
    doc = parse_xml(inFileName, parser)
    root_node = doc.getroot()
    if root_node.tag == GenericDataConstant:
        root_tag = 'GenericData'
        root_class = GenericDataType
    elif root_node.tag == StructureDataConstant:
        root_tag = 'StructureSpecificData'
        root_class = StructureSpecificDataType
    elif root_node.tag == MetadataConstant:
        root_tag = 'Structure'
        root_class = MetadataType
    else:
        return None
    root_obj = root_class.factory()
    root_obj.original_tag_name_ = root_tag
    root_obj.build(root_node, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(root_node)
    root_obj._namespace_def = namespacedefs
    makeWarnings(print_warning, gds_collector)

    return root_obj


def sdmxStrToDataset(xmlObj, dsd_dict) -> []:
    datasets = {}
    refs_data = {}

    for i in xmlObj.header.structure:
        refs_data[i.gds_element_tree_node_.attrib['structureID']] = id_creator(i.ref.agencyID, i.ref.id_,
                                                                               i.ref.version)

    for e in xmlObj.dataset:
        str_ref = e.structureRef

        if str_ref is None:
            str_ref = e.gds_element_tree_node_.attrib[
                '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific}structureRef']
            if str_ref is None:
                # TODO Warning Structure Ref not found
                continue
        if refs_data[str_ref] not in dsd_dict:
            continue
        dsd = dsd_dict[refs_data[str_ref]]
        item = DataSet(dsd)

        dataset_attributes = {'reportingBegin': e.reporting_begin_date, 'reportingEnd': e.reporting_end_date,
                              'dataExtractionDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                              'validFrom': e.valid_from_date,
                              'validTo': e.valid_to_date, 'publicationYear': e.publication_year,
                              'publicationPeriod': e.publication_period, 'action': e.action,
                              'setId': dsd.id}

        # Default Attributes

        dim_obs = ''

        for j in xmlObj.header.structure:
            if j.gds_element_tree_node_.attrib['structureID'] == str_ref \
                    and j.gds_element_tree_node_.attrib['dimensionAtObservation']:
                dim_obs = j.gds_element_tree_node_.attrib['dimensionAtObservation']

        if dim_obs == '':
            dataset_attributes['dimensionAtObservation'] = 'AllDimensions'
        else:
            dataset_attributes['dimensionAtObservation'] = dim_obs

        item.datasetAttributes = dataset_attributes.copy()

        attached_attributes = {}

        for k, v in e.any_attributes.items():
            if k in dsd.datasetAttributeCodes:
                attached_attributes[k] = v

        item.attachedAttributes = attached_attributes

        obs_attributes_keys = []
        for record in dsd.attributeDescriptor.components.values():
            if record.relatedTo is not None and isinstance(record.relatedTo, PrimaryMeasure):
                obs_attributes_keys.append(record.id)

        if len(e.data) > 0:
            item.data = pd.DataFrame(e.data)
        datasets[dsd.id] = item
    del xmlObj
    return datasets


def check_empty(series: dict):
    temp_series = series.copy()
    for key, list_ in temp_series.items():
        if all(e is np.nan for e in list_):
            series.pop(key)


def check_length(series: dict):
    length = -1
    key_ref = ''
    for key, list_ in series.items():
        if length == -1:
            length = len(list_)
            key_ref = key
        elif length != len(list_):
            # All series must be on same size
            print('Key: %s ---- length: %d ---- expected length: %d from key %s' % (key, len(list_), length, key_ref))


def sdmxGenToDataSet(xmlObj, dsd_dict) -> []:
    datasets = {}

    for e in xmlObj.dataset:
        if xmlObj.header.structure[e.structureRef]['DSDID'] not in dsd_dict:
            # TODO Warning DSD not found
            continue

        dsd = dsd_dict[xmlObj.header.structure[e.structureRef]['DSDID']]
        item = DataSet(dsd)

        dataset_attributes = {'reportingBegin': e.reportingBeginDate, 'reportingEnd': e.reportingEndDate,
                              'dataExtractionDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                              'validFrom': e.validFromDate, 'validTo': e.validToDate,
                              'publicationYear': e.publicationYear, 'publicationPeriod': e.publicationPeriod,
                              'action': e.action, 'setId': dsd.id}

        dim_obs = xmlObj.header.structure[e.structureRef]['dimAtObs']

        dataset_attributes['dimensionAtObservation'] = dim_obs

        item.datasetAttributes = dataset_attributes.copy()

        attached_attributes = {}
        if e.Attributes is not None:
            attached_attributes = e.Attributes.value_

        item.attachedAttributes = attached_attributes.copy()

        if len(e.data) > 0:
            temp = pd.DataFrame(e.data)
            if dim_obs == 'AllDimensions':
                item.data = temp.rename(columns={'OBS_VALUE': dsd.measureCode})
            else:
                item.data = temp.rename(columns={'ObsDimension': dim_obs, 'OBS_VALUE': dsd.measureCode})
        datasets[dsd.id] = item
    del xmlObj
    return datasets
