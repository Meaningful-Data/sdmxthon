import json
import logging
from datetime import date

import pandas as pd

from .common.dataSet import DataSet
from .message.generic import GenericDataHeaderType, PartyType, SenderType, StructureSpecificDataHeaderType
from .utils.enums import DatasetType
from .utils.parsers import generate_message
from .utils.read_write import load_AllDimensions, save_AllDimensions, sdmxGenToPandas, \
    sdmxStrToPandas

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)


def xmlToDatasetList(path_to_xml, dsd_dict, dataset_type=None) -> list:
    datasetList = list()

    objStructure = load_AllDimensions(path_to_xml, dataset_type)

    if dataset_type == DatasetType.GenericDataSet:
        datasetList = sdmxGenToPandas(objStructure, dsd_dict)
    elif dataset_type == DatasetType.StructureDataSet:
        datasetList = sdmxStrToPandas(objStructure, dsd_dict)

    return datasetList


def datasetListToXML(datasetList, dsd_dict, pathSaveTo, header, dataset_type=DatasetType.StructureDataSet,
                     validate_data=False):
    message = generate_message(datasetList, dsd_dict, header, dataset_type, validate_data)
    if message == None:
        return None
    if pathSaveTo == '':
        return save_AllDimensions(message, pathSaveTo)
    else:
        save_AllDimensions(message, pathSaveTo)


def datasetToXML(dataset, dsd_dict, pathSaveTo, header, dataset_type=DatasetType.StructureDataSet):
    message = generate_message([dataset], dsd_dict, header, dataset_type)

    if pathSaveTo == '':
        return save_AllDimensions(message, pathSaveTo)
    else:
        save_AllDimensions(message, pathSaveTo)


def datasetListToJSON(dataset_list, path_to_file='') -> list:
    listElements = []
    for e in dataset_list:
        element = {}
        result = e.obs.to_json(orient="records")
        parsed = json.loads(result)
        element['structureRef'] = {"code": e.code, "version": e.version, "agencyID": e.agencyID}
        element['dataset_attributes'] = e.dataset_attributes
        element['attached_attributes'] = e.attached_attributes
        element['obs'] = parsed.copy()
        listElements.append(element.copy())

    if path_to_file != '':
        f = open(path_to_file, "w")
        f.write(json.dumps(listElements, ensure_ascii=False, indent=2))
        f.close()

    return listElements


def JSONFileToDatasetList(path_to_json) -> list:
    dataset_list = list()
    f = open(path_to_json, "r")
    parsed = json.loads(f.read())
    for e in parsed:
        dataset_list.append(DataSetCreator(code=e.get('structureRef').get('code'),
                                           version=e.get('structureRef').get('version'),
                                           agencyID=e.get('structureRef').get('agencyID'),
                                           dataset_attributes=e.get('dataset_attributes'),
                                           attached_attributes=e.get('attached_attributes'),
                                           obs=e.get('obs')))
    return dataset_list


def JSONToDatasetList(json_list) -> list:
    dataset_list = list()
    parsed = json.loads(json.dumps(json_list, ensure_ascii=False, indent=2))
    for e in parsed:
        dataset_list.append(DataSetCreator(code=e.get('structureRef').get('code'),
                                           version=e.get('structureRef').get('version'),
                                           agencyID=e.get('structureRef').get('agencyID'),
                                           dataset_attributes=e.get('dataset_attributes'),
                                           attached_attributes=e.get('attached_attributes'),
                                           obs=e.get('obs')))
    return dataset_list


def saveOBSfromDatasetList(format, folder, dataset_list):
    if format == 'csv':
        for e in dataset_list:
            filename = folder + e.code + '.' + format
            e.obs.to_csv(filename, sep=',', encoding='utf-8', index=False, header=True)
    elif format == 'sql':
        for e in dataset_list:
            e.obs.reset_index().to_sql(e.code)
    elif format == 'feather':
        for e in dataset_list:
            filename = folder + e.code + '.' + format
            e.obs.to_feather(filename)


def _filterFillingINF(message):
    for e in message.DataSet:
        if e._structureRef == 'FILINGINF':
            message.DataSet.remove(e)

    for e in message.Header._structure:
        if e._structureID == 'FILINGINF':
            message.Header._structure.remove(e)

    return message


def _messageSort(message):
    message.Header._structure.sort(key=__sortStructureID)
    message.DataSet.sort(key=__sortStructureRef)
    return message


def __sortStructureRef(e):
    return e._structureRef


def __sortStructureID(e):
    return e._structureID


def __sortCode(e):
    return e.code


def _dataSetListSort(dataset_list):
    dataset_list.sort(key=__sortCode)
    return dataset_list


def DataSetCreator(code, version, agencyID, dataset_attributes=None, attached_attributes=None,
                   obs=None):
    if dataset_attributes is None or dataset_attributes == {}:
        dataset_attributes = {"reportingBegin": None,
                              "reportingEnd": None,
                              "dataExtractionDate": date.today(),
                              "validFrom": None,
                              "validTo": None,
                              "publicationYear": None,
                              "publicationPeriod": None}

    if isinstance(obs, pd.DataFrame):
        item = DataSet(code=code, version=version, agencyID=agencyID,
                       dataset_attributes=dataset_attributes, attached_attributes=attached_attributes,
                       obs=obs)
    elif isinstance(obs, list):
        item = DataSet(code=code, version=version, agencyID=agencyID,
                       dataset_attributes=dataset_attributes, attached_attributes=attached_attributes,
                       obs=pd.DataFrame(obs))
    else:
        return None

    return item


def headerCreation(id_: str, test: bool = False,
                   senderId: str = "Unknown", receiverId: str = "not_supplied",
                   datetimeStr='2020-09-10T12:00:00.000',
                   dataset_type=DatasetType.StructureDataSet):
    if dataset_type == DatasetType.GenericDataSet:
        header = GenericDataHeaderType()
    elif dataset_type == DatasetType.StructureDataSet:
        header = StructureSpecificDataHeaderType()
    else:
        return None

    header.set_ID(id_)
    header.set_Test(header.gds_format_boolean(test))
    header.set_Prepared(header.gds_parse_datetime(datetimeStr))

    sender = SenderType()
    sender.set_id(senderId)

    receiver = PartyType()
    receiver.set_id(receiverId)

    header.set_Sender(sender)
    header.add_Receiver(receiver)

    return header
