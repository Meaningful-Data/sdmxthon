import os
import warnings
from datetime import datetime

import pandas as pd
from lxml import etree as etree_
from lxml.etree import DocumentInvalid

from sdmxthon.model.dataset import Dataset
from sdmxthon.parsers.gdscollector import GdsCollector
from sdmxthon.parsers.message_parsers import GenericDataType, \
    StructureSpecificDataType, \
    MetadataType
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.xml_base import parse_xml, \
    makeWarnings

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

GenericDataConstant = '{http://www.sdmx.org/resources/sdmxml/schemas' \
                      '/v2_1/message}GenericData'
StructureDataConstant = '{http://www.sdmx.org/resources/sdmxml' \
                        '/schemas/v2_1/message}StructureSpecificData'
MetadataConstant = '{http://www.sdmx.org/resources/sdmxml' \
                   '/schemas/v2_1/message}Structure'

pathToSchema = 'schemas/SDMXMessage.xsd'


def _read_xml(inFileName, print_warning=True, validate=True):
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

    if validate:
        base_path = os.path.dirname(os.path.dirname(__file__))
        schema = os.path.join(base_path, pathToSchema)
        xmlschema_doc = etree_.parse(schema)
        xmlschema = etree_.XMLSchema(xmlschema_doc)

        if not xmlschema.validate(doc):
            try:
                xmlschema.assertValid(doc)
            except DocumentInvalid as e:
                if len(e.args) == 1 and \
                        'xsi:type' in e.args[0] or \
                        'abstract' in e.args[0]:
                    pass
                else:
                    raise e
    root_obj = root_class._factory()
    root_obj.original_tag_name_ = root_tag
    root_obj._build(root_node, gds_collector_=gds_collector)
    makeWarnings(print_warning, gds_collector)

    return root_obj


def _sdmx_str_to_dataset(xmlObj, dsds, dataflows) -> []:
    datasets = {}
    for e in xmlObj.dataset:
        if e.structureRef in xmlObj.header.structure.keys():
            str_dict = xmlObj.header.structure[e.structureRef]
            if (dsds is not None and str_dict['type'] == 'DataStructure' and
                    str_dict['ID'] in dsds.keys()):
                dsd = dsds[str_dict['ID']]
                item = Dataset(structure=dsd)
            elif dataflows is not None and str_dict['type'] == 'DataFlow':
                if str_dict['ID'] in dataflows.keys():
                    dataflow = dataflows[str_dict['ID']]
                    dsd = dataflow.structure
                    item = Dataset(dataflow=dataflow)
                else:
                    warnings.warn(f'DataFlow {str_dict["ID"]} not found')
                    continue
            else:
                warnings.warn(f'DSD {str_dict["ID"]} not found')
                continue
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

        dataset_attributes = {'reportingBegin': e.reporting_begin_date,
                              'reportingEnd': e.reporting_end_date,
                              'dataExtractionDate': datetime.now().strftime(
                                  '%Y-%m-%dT%H:%M:%S'),
                              'validFrom': e.valid_from_date,
                              'validTo': e.valid_to_date,
                              'publicationYear': e.publication_year,
                              'publicationPeriod': e.publication_period,
                              'action': e.action, 'setId': dsd.id,
                              'dimensionAtObservation': str_dict['dimAtObs']}

        # Default Attributes

        item.dataset_attributes = dataset_attributes.copy()

        attached_attributes = {}

        for k, v in e.any_attributes.items():
            if k in dsd.dataset_attribute_codes:
                attached_attributes[k] = v

        item.attached_attributes = attached_attributes

        if len(e.data) > 0 or e.dataframe is not None:

            temp = None

            if len(e.data) > 0:
                temp = pd.DataFrame(e.data)

            if e.dataframe is not None and temp is not None:
                temp = pd.concat([temp, e.dataframe], ignore_index=True)
            elif temp is None:
                temp = e.dataframe

            item.data = temp
        datasets[dsd.unique_id] = item
    del xmlObj
    return datasets


def _sdmx_gen_to_dataset(xmlObj, dsds, dataflows) -> []:
    datasets = {}

    for e in xmlObj.dataset:
        if e.structureRef in xmlObj.header.structure.keys():
            str_dict = xmlObj.header.structure[e.structureRef]
            if dsds is not None and str_dict['type'] == 'DataStructure' and \
                    str_dict['ID'] in dsds.keys():
                dsd = dsds[str_dict['ID']]
                item = Dataset(structure=dsd)
            elif dataflows is not None and str_dict['type'] == 'DataFlow':
                if str_dict['ID'] in dataflows.keys():
                    dataflow = dataflows[str_dict['ID']]
                    dsd = dataflow.structure
                    item = Dataset(dataflow=dataflow)
                else:
                    warnings.warn(f'DataFlow {str_dict["ID"]} not found')
                    continue
            else:
                warnings.warn(f'DSD {str_dict["ID"]} not found')
                continue
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

        dataset_attributes = {'reportingBegin': e.reporting_begin_date,
                              'reportingEnd': e.reporting_end_date,
                              'dataExtractionDate': datetime.now().strftime(
                                  '%Y-%m-%dT%H:%M:%S'),
                              'validFrom': e.valid_from_date,
                              'validTo': e.valid_to_date,
                              'publicationYear': e.publication_year,
                              'publicationPeriod': e.publication_period,
                              'action': e.action, 'setId': dsd.id,
                              'dimensionAtObservation': str_dict['dimAtObs']}

        item.dataset_attributes = dataset_attributes.copy()

        attached_attributes = {}
        if e.Attributes is not None:
            attached_attributes = e.Attributes.value_

        item.attached_attributes = attached_attributes.copy()
        if len(e.data) > 0 or e.dataframe is not None:

            temp = None

            if len(e.data) > 0:
                temp = pd.DataFrame(e.data)

            if e.dataframe is not None and temp is not None:
                temp = pd.concat([temp, e.dataframe], ignore_index=True)
            elif temp is None:
                temp = e.dataframe

            if str_dict['dimAtObs'] == 'AllDimensions':
                item.data = temp.rename(
                    columns={'OBS_VALUE': dsd.measure_code})
            else:
                item.data = temp.rename(
                    columns={'ObsDimension': str_dict['dimAtObs'],
                             'OBS_VALUE': dsd.measure_code})
        datasets[dsd.unique_id] = item
    del xmlObj
    return datasets


def _sdmx_to_dataset_no_metadata(xml_obj, type_: MessageTypeEnum):
    datasets = {}

    for e in xml_obj.dataset:
        if e.structureRef in xml_obj.header.structure.keys():
            str_dict = xml_obj.header.structure[e.structureRef]
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

        dataset_attributes = {'reportingBegin': e.reporting_begin_date,
                              'reportingEnd': e.reporting_end_date,
                              'dataExtractionDate': datetime.now().strftime(
                                  '%Y-%m-%dT%H:%M:%S'),
                              'validFrom': e.valid_from_date,
                              'validTo': e.valid_to_date,
                              'publicationYear': e.publication_year,
                              'publicationPeriod': e.publication_period,
                              'action': e.action, 'setId': e.structureRef,
                              'dimensionAtObservation': str_dict['dimAtObs']}

        item = Dataset(dataset_attributes=dataset_attributes)

        if type_ == MessageTypeEnum.GenericDataSet:
            attached_attributes = {}
            if e.Attributes is not None:
                attached_attributes = e.Attributes.value_

            if len(e.data) > 0 or e.dataframe is not None:

                temp = None

                if len(e.data) > 0:
                    temp = pd.DataFrame(e.data)

                if e.dataframe is not None and temp is not None:
                    temp = pd.concat([temp, e.dataframe],
                                     ignore_index=True)
                elif temp is None:
                    temp = e.dataframe
                if str_dict['dimAtObs'] == 'AllDimensions':
                    item.data = temp
                else:
                    item.data = temp.rename(
                        columns={'ObsDimension': str_dict['dimAtObs']})
        else:
            attached_attributes = {}
            for k, v in e.any_attributes.items():
                if k not in ['type', 'xsi:dim_type']:
                    attached_attributes[k] = v

            item.attached_attributes = attached_attributes

            if len(e.data) > 0 or e.dataframe is not None:

                temp = None

                if len(e.data) > 0:
                    temp = pd.DataFrame(e.data)

                if e.dataframe is not None and temp is not None:
                    temp = pd.concat([temp, e.dataframe], ignore_index=True)
                elif temp is None:
                    temp = e.dataframe

                item.data = temp

        item.attached_attributes = attached_attributes

        datasets[e.structureRef] = item
    del xml_obj
    return datasets


def _sdmx_to_dataframe(xml_obj, type_: MessageTypeEnum):
    dataframes = {}

    for e in xml_obj.dataset:
        if e.structureRef in xml_obj.header.structure.keys():
            str_dict = xml_obj.header.structure[e.structureRef]
        else:
            warnings.warn(f'Structure {e.structureRef} not found')
            continue

        if type_ == MessageTypeEnum.GenericDataSet:
            if len(e.data) > 0 or e.dataframe is not None:

                temp = None

                if len(e.data) > 0:
                    temp = pd.DataFrame(e.data)

                if e.dataframe is not None and temp is not None:
                    temp = pd.concat([temp, e.dataframe],
                                     ignore_index=True)
                elif temp is None:
                    temp = e.dataframe
                if str_dict['dimAtObs'] == 'AllDimensions':
                    dataframes[str_dict['ID']] = temp
                else:
                    dataframes[str_dict['ID']] = temp.rename(
                        columns={'ObsDimension': str_dict['dimAtObs']})
        else:
            if len(e.data) > 0 or e.dataframe is not None:

                temp = None

                if len(e.data) > 0:
                    temp = pd.DataFrame(e.data)

                if e.dataframe is not None and temp is not None:
                    temp = pd.concat([temp, e.dataframe], ignore_index=True)
                elif temp is None:
                    temp = e.dataframe

                dataframes[str_dict['ID']] = temp

    del xml_obj

    return dataframes
