import logging
from datetime import datetime

import pandas as pd

from .gdscollector import GdsCollector
from .message_parsers import GenericDataType, StructureSpecificDataType, MetadataType
from ..model.component import PrimaryMeasure
from ..model.dataSet import DataSet
from ..utils.xml_base import get_required_ns_prefix_defs, parse_xml, makeWarnings

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

    for e in xmlObj.dataset:
        if xmlObj.header.structure[e.structureRef]['DSDID'] not in dsd_dict:
            # TODO Warning DSD not found
            continue

        dsd = dsd_dict[xmlObj.header.structure[e.structureRef]['DSDID']]
        item = DataSet(dsd)

        dataset_attributes = {'reportingBegin': e.reporting_begin_date, 'reportingEnd': e.reporting_end_date,
                              'dataExtractionDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                              'validFrom': e.valid_from_date,
                              'validTo': e.valid_to_date, 'publicationYear': e.publication_year,
                              'publicationPeriod': e.publication_period, 'action': e.action,
                              'setId': dsd.id}

        # Default Attributes

        dim_obs = xmlObj.header.structure[e.structureRef]['dimAtObs']

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
        datasets[dsd.unique_id] = item
    del xmlObj
    return datasets


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
        datasets[dsd.unique_id] = item
    del xmlObj
    return datasets
