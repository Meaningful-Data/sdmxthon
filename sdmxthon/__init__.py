import json
import logging
from typing import Dict
from zipfile import ZipFile

from lxml import etree

from .common.dataSet import DataSet
from .common.message import Message
from .utils.creators import DataSetCreator
from .utils.enums import DatasetType
from .utils.parsers import generate_datasets_message, id_creator, get_codelist_model, \
    get_concept_schemes, get_DSDs
from .utils.read_write import load_AllDimensions, save_AllDimensions, sdmxGenToDataSet, \
    sdmxStrToDataset

# create logger
logger = logging.getLogger("logger")
logger.setLevel(logging.WARNING)


def readSDMX(path_to_xml, pathToMetadata, dataset_type=None):
    if dataset_type == None:
        raise ValueError('Dataset type is None')
    objStructure = load_AllDimensions(path_to_xml, datasetType=dataset_type)

    dsds = getMetadata(pathToMetadata)

    header = objStructure.Header

    if dataset_type == DatasetType.GenericDataSet or dataset_type == DatasetType.GenericTimeSeriesDataSet:
        datasets = sdmxGenToDataSet(objStructure, dsds)
    elif dataset_type == DatasetType.StructureDataSet or dataset_type == DatasetType.StructureTimeSeriesDataSet:
        datasets = sdmxStrToDataset(objStructure, dsds)
    else:
        raise ValueError('Invalid Dataset Type')

    return Message(DatasetType.GenericDataSet, datasets, header)


def getDatasets(path_to_xml, pathToMetadata, dataset_type=None) -> dict:
    if dataset_type == None:
        raise ValueError('Dataset Type is None')

    objStructure = load_AllDimensions(path_to_xml, datasetType=dataset_type)

    logger.debug('XML read')

    dsds = getMetadata(pathToMetadata)

    logger.debug('Metadata read')

    if dataset_type == DatasetType.GenericDataSet or dataset_type == DatasetType.GenericTimeSeriesDataSet:
        return sdmxGenToDataSet(objStructure, dsds)
    elif dataset_type == DatasetType.StructureDataSet or dataset_type == DatasetType.StructureTimeSeriesDataSet:
        return sdmxStrToDataset(objStructure, dsds)
    else:
        raise ValueError('Invalid Dataset Type')


def getMetadata(pathToMetadata) -> dict:
    root = etree.parse(pathToMetadata)

    codelists = get_codelist_model(root)
    concepts = get_concept_schemes(root, codelists)
    return get_DSDs(root, concepts, codelists)


def messageToXML(output_path, message):
    if len(message.payload) == 0:
        raise ValueError('Datasets must be provided')

    messageXML = generate_datasets_message(message)
    if message == None:
        raise ValueError('Message could not be parsed')
    if output_path == '':
        return save_AllDimensions(messageXML, output_path)
    else:
        save_AllDimensions(messageXML, output_path)


def xmlToJSON(pathToXML, pathToMetadata, output_path, dataset_type=DatasetType.GenericDataSet):
    list_elements = []

    datasets: Dict[str, DataSet] = getDatasets(pathToXML, pathToMetadata, dataset_type)

    for e in datasets.values():
        list_elements.append(e.toJSON())
    with open(output_path, 'w') as f:
        f.write(json.dumps(list_elements, ensure_ascii=False, indent=2))


def xmlToCSV(pathToXML, pathToMetadata, output_path, dataset_type=DatasetType.GenericDataSet):
    datasets: Dict[str, DataSet] = getDatasets(pathToXML, pathToMetadata, dataset_type)

    if '.zip' in output_path:
        with ZipFile(output_path, 'w') as zipObj:
            # Add multiple files to the zip
            for record in datasets.values():
                zipObj.writestr(record.structure.id + '.csv', data=record.toCSV())

    else:
        if len(datasets) > 1:
            raise ValueError('Cannot introduce several Datasets in a CSV. Consider using .zip as output path')
        elif len(datasets) is 1:
            if '.zip' in output_path:
                filename = output_path.split('.')[0]
                output_path = filename + '.csv'
            # Getting first value
            values_view = datasets.values()
            value_iterator = iter(values_view)
            dset = next(value_iterator)

            dset.toCSV(output_path)
        else:
            raise ValueError('No Datasets were parsed')


def readJSON(pathToJSON, dsds) -> dict:
    datasets = {}
    if isinstance(pathToJSON, str):
        with open(pathToJSON, 'r') as f:
            parsed = json.loads(f.read())
    else:
        parsed = json.loads(pathToJSON.read())
    for e in parsed:
        code = e.get('structureRef').get('code')
        version = e.get('structureRef').get('version')
        agencyID = e.get('structureRef').get('agencyID')
        dsdid = id_creator(agencyID, code, version)
        if dsdid not in dsds.keys():
            raise ValueError('Could not find any dsd matching to DSDID: %s' % dsdid)
        datasets[code] = DataSetCreator(dsd=dsds[dsdid],
                                        dataset_attributes=e.get('dataset_attributes'),
                                        attached_attributes=e.get('attached_attributes'),
                                        obs=e.get('obs'))
    return datasets


def validateData(datasets: Dict[str, DataSet]):
    validations = {}
    for e in datasets.values():
        list_errors = e.semanticValidation()
        if len(list_errors) > 0:
            validations[e.structure.id] = list_errors
    if len(validations) is 0:
        return None
    else:
        return validations
