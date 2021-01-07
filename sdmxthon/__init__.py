import json
import sys
from typing import Dict
from zipfile import ZipFile

from .common.dataSet import DataSet
from .common.message import Message
from .utils.dataset_parsing import getMetadata
from .utils.enums import DatasetType
from .utils.metadata_parsers import id_creator
from .utils.read import load_AllDimensions, sdmxGenToDataSet, \
    sdmxStrToDataset
from .utils.write import save_file


def readSDMX(path_to_xml, pathToMetadata, dataset_type=None):
    if dataset_type is None:
        raise ValueError('Dataset type cannot be None')
    objStructure = load_AllDimensions(path_to_xml, datasetType=dataset_type)
    dsds = getMetadata(pathToMetadata)

    header = objStructure.Header

    if dataset_type == DatasetType.GenericDataSet or dataset_type == DatasetType.GenericTimeSeriesDataSet:
        datasets = sdmxGenToDataSet(objStructure, dsds)
    elif dataset_type == DatasetType.StructureDataSet or dataset_type == DatasetType.StructureTimeSeriesDataSet:
        datasets = sdmxStrToDataset(objStructure, dsds)
    else:
        raise ValueError('Invalid Dataset Type')
    return Message(dataset_type, datasets, header)


def getDatasets(path_to_xml, pathToMetadata, dataset_type=None):
    if dataset_type is None:
        raise ValueError('Dataset Type cannot be None')

    objStructure = load_AllDimensions(path_to_xml, datasetType=dataset_type)

    dsds, errors = getMetadata(pathToMetadata)
    print(errors)
    if dataset_type == DatasetType.GenericDataSet or dataset_type == DatasetType.GenericTimeSeriesDataSet:
        datasets = sdmxGenToDataSet(objStructure, dsds)
    elif dataset_type == DatasetType.StructureDataSet or dataset_type == DatasetType.StructureTimeSeriesDataSet:
        datasets = sdmxStrToDataset(objStructure, dsds)
    else:
        raise ValueError('Invalid Dataset Type')

    if len(datasets) == 1:
        values_view = datasets.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        return first_value
    else:
        return datasets


def xmlToJSON(pathToXML, pathToMetadata, output_path, dataset_type=DatasetType.GenericDataSet):
    list_elements = []

    dataset = getDatasets(pathToXML, pathToMetadata, dataset_type)

    if isinstance(dataset, dict):
        for e in dataset.values():
            list_elements.append(e.toJSON())
    else:
        list_elements.append(dataset.toJSON())
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
        dsdid = f"{agencyID}:{code}({version})"
        if dsdid not in dsds.keys():
            raise ValueError('Could not find any dsd matching to DSDID: %s' % dsdid)
        datasets[code] = DataSet(structure=dsds[dsdid],
                                 dataset_attributes=e.get('dataset_attributes'),
                                 attached_attributes=e.get('attached_attributes'),
                                 data=e.get('data'))
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


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size
