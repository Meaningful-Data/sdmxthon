import warnings
from datetime import datetime

import pandas as pd

from .gdscollector import GdsCollector
from .message_parsers import GenericDataType, StructureSpecificDataType, MetadataType
from .metadata_validations import setReferences
from ..model.component import PrimaryMeasure
from ..model.dataSet import DataSet
from ..model.message import Message
from ..utils.enums import MessageTypeEnum
from ..utils.xml_base import get_required_ns_prefix_defs, parse_xml, makeWarnings

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

GenericDataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}GenericData'
StructureDataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}StructureSpecificData'
MetadataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure'


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


def sdmxStrToDataset(xmlObj, dsds, dataflows) -> []:
    datasets = {}
    for e in xmlObj.dataset:
        if e.structureRef in xmlObj.header.structure.keys():
            str_dict = xmlObj.header.structure[e.structureRef]
            if dsds is not None and str_dict['type'] == 'DataStructure' and str_dict['ID'] in dsds.keys():
                dsd = dsds[str_dict['ID']]
                item = DataSet(structure=dsd)
            elif dataflows is not None and str_dict['type'] == 'DataFlow':
                if str_dict['ID'] in dataflows.keys():
                    dataflow = dataflows[str_dict['ID']]
                    dsd = dataflow.structure
                    item = DataSet(structure=dsd, describedBy=dataflow)
                else:
                    warnings.warn(f'DataFlow {str_dict["ID"]} not found')
                    continue
            else:
                warnings.warn(f'DSD {str_dict["ID"]} not found')
                continue
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

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


def sdmxGenToDataSet(xmlObj, dsds, dataflows) -> []:
    datasets = {}

    for e in xmlObj.dataset:
        if e.structureRef in xmlObj.header.structure.keys():
            str_dict = xmlObj.header.structure[e.structureRef]
            if dsds is not None and str_dict['type'] == 'DataStructure' and str_dict['ID'] in dsds.keys():
                dsd = dsds[str_dict['ID']]
                item = DataSet(structure=dsd)
            elif dataflows is not None and str_dict['type'] == 'DataFlow':
                if str_dict['ID'] in dataflows.keys():
                    dataflow = dataflows[str_dict['ID']]
                    dsd = dataflow.structure
                    item = DataSet(structure=dsd, describedBy=dataflow)
                else:
                    warnings.warn(f'DataFlow {str_dict["ID"]} not found')
                    continue
            else:
                warnings.warn(f'DSD {str_dict["ID"]} not found')
                continue
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

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


def sdmxToDataFrame(xmlObj):
    dataframes = []

    for e in xmlObj.dataset:
        if e.structureRef in xmlObj.header.structure.keys():
            str_dict = xmlObj.header.structure[e.structureRef]
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

        dim_obs = str_dict['dimAtObs']

        if len(e.data) > 0:
            temp = pd.DataFrame(e.data)
            if dim_obs == 'AllDimensions':
                dataframes.append(temp)
            else:
                dataframes.append(temp.rename(columns={'ObsDimension': dim_obs}))

    del xmlObj

    if len(dataframes) == 1:
        return dataframes[0]
    else:
        return dataframes


def getMetadata(pathToMetadata):
    metadata = readXML(pathToMetadata)
    if isinstance(metadata, MetadataType):
        setReferences(metadata)
        return Message(payload=metadata.structures, message_type=MessageTypeEnum.Metadata, header=metadata.header)
    else:
        raise TypeError('Need a Structure file to be parsed')
