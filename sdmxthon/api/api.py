import json
import logging
import sys
from typing import Dict
from zipfile import ZipFile

from SDMXThon.model.dataSet import DataSet
from SDMXThon.model.message import Message
from SDMXThon.parsers.message_parsers import MetadataType
from SDMXThon.parsers.metadata_validations import setReferences
from SDMXThon.parsers.read import _read_xml, _sdmx_gen_to_dataset, _sdmx_str_to_dataset, _sdmx_to_dataframe
from SDMXThon.utils.enums import MessageTypeEnum
from SDMXThon.utils.handlers import first_element_dict

logger = logging.getLogger('logger')


def read_sdmx(path_to_xml, path_to_metadata=None) -> Message:
    """
    Read SDMX performs the operation of reading a SDMX Data and SDMX metadata files. URLs could be used.

    :param path_to_xml: Path or URL to the SDMX data file
    :param path_to_metadata: Path or URL to the SDMX metadata file (Optional)
    :return: A :obj:`Message <model.message.Message>` object or a dict of Dataframes if path_to_metadata is None
    """
    if path_to_metadata is None:
        return get_data(path_to_xml)

    metadata = get_metadata(path_to_metadata)

    obj_ = _read_xml(path_to_xml)
    if isinstance(obj_, MetadataType):
        setReferences(obj_)

    header = obj_.header
    if obj_.original_tag_name_ == 'GenericData':
        type_ = MessageTypeEnum.GenericDataSet
        data = _sdmx_gen_to_dataset(obj_, metadata.payload.dsds, metadata.payload.dataflows)
    elif obj_.original_tag_name_ == 'StructureSpecificData':
        type_ = MessageTypeEnum.StructureDataSet
        data = _sdmx_str_to_dataset(obj_, metadata.payload.dsds, metadata.payload.dataflows)
    elif obj_.original_tag_name_ == 'Structure':
        type_ = MessageTypeEnum.Metadata
        data = obj_.structures
    else:
        raise ValueError('Wrong Message type')
    return Message(type_, data, header)


def get_datasets(path_to_xml, path_to_metadata):
    """
    GetDatasets performs the operation of reading a SDMX Data and SDMX metadata files. URLs could be used.

    :param path_to_xml: Path or URL to the SDMX data file
    :param path_to_metadata: Path or URL to the SDMX metadata file
    :return: A :obj:`Dataset <model.dataSet.DataSet>` object or a dict of :obj:`Datasets <model.dataSet.DataSet>`
    """

    obj_ = _read_xml(path_to_xml)

    metadata = get_metadata(path_to_metadata)

    if obj_.original_tag_name_ == 'GenericData':
        datasets = _sdmx_gen_to_dataset(obj_, metadata.payload.dsds, metadata.payload.dataflows)
    elif obj_.original_tag_name_ == 'StructureSpecificData':
        datasets = _sdmx_str_to_dataset(obj_, metadata.payload.dsds, metadata.payload.dataflows)
    else:
        raise ValueError('Wrong Message type')

    if len(datasets) == 1:
        return first_element_dict(datasets)
    else:
        return datasets


def get_data(path_to_data):
    """
    GetData reads all observations in a SDMX file

    :param path_to_data: Path or URL to the SDMX data file

    :return: A `Pandas Dataframe <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ or a dict of
            `Pandas Dataframe <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_
    """
    obj_ = _read_xml(path_to_data)

    if isinstance(obj_, MetadataType):
        raise TypeError('No data available in a Structure file. You should use get_metadata method')

    return _sdmx_to_dataframe(obj_)


def xml_to_json(pathToXML, path_to_metadata, output_path):
    """
    XML to JSON transforms a SDMX file into a JSON in the shape of the JSON Specification. Saves the file on disk.

    :param pathToXML: Path or URL to the SDMX data file
    :param path_to_metadata: Path or URL to the SDMX metadata file
    :param output_path: Path to save the JSON
    """
    list_elements = []

    dataset = get_datasets(pathToXML, path_to_metadata)

    if isinstance(dataset, dict):
        for e in dataset.values():
            list_elements.append(e.toJSON())
    else:
        list_elements.append(dataset.toJSON())
    with open(output_path, 'w') as f:
        f.write(json.dumps(list_elements, ensure_ascii=False, indent=2))


def xml_to_csv(pathToXML, path_to_metadata, output_path):
    """
    XML to CSV transforms a SDMX file into a CSV. Saves the file on disk or .zip of CSV. If the SDMX data file has
    only a Dataset and output_path is '', it returns a StringIO object.

    :param pathToXML: Path or URL to the SDMX data file
    :param path_to_metadata: Path or URL to the SDMX metadata file
    :param output_path: Path to save the CSV
    :return: A StringIO object if output_path is ''
    """
    datasets: Dict[str, DataSet] = get_datasets(pathToXML, path_to_metadata)

    if '.zip' in output_path:
        with ZipFile(output_path, 'w') as zipObj:
            # Add multiple files to the zip
            for record in datasets.values():
                zipObj.writestr(record.structure.id + '.csv', data=record.toCSV())

    else:
        if len(datasets) > 1:
            raise ValueError('Cannot introduce several Datasets in a CSV. Consider using .zip in output path')
        elif len(datasets) is 1:
            if '.zip' in output_path:
                filename = output_path.split('.')[0]
                output_path = filename + '.csv'
            # Getting first value
            dataset = first_element_dict(datasets)

            return dataset.toCSV(output_path)
        else:
            raise ValueError('No Datasets were parsed')


def read_json(path_to_json, dsds) -> dict:
    """

    Transforms a JSON file in the shape of the JSON Specification into a dict of :obj:`Dataset <model.dataset.DataSet>`.

    :param path_to_json: Path to the JSON file.
    :param dsds: A dict of DataStructureDefinition
    :return: A dict of :obj:`Datasets <model.dataSet.DataSet>`.
    """
    datasets = {}
    if isinstance(path_to_json, str):
        with open(path_to_json, 'r') as f:
            parsed = json.loads(f.read())
    else:
        parsed = json.loads(path_to_json.read())
    for e in parsed:
        code = e.get('structureRef').get('code')
        version = e.get('structureRef').get('version')
        agency_id = e.get('structureRef').get('agencyID')
        dsdid = f"{agency_id}:{code}({version})"
        if dsdid not in dsds.keys():
            raise ValueError('Could not find any dsd matching to DSDID: %s' % dsdid)
        datasets[code] = DataSet(structure=dsds[dsdid],
                                 dataset_attributes=e.get('dataset_attributes'),
                                 attached_attributes=e.get('attached_attributes'),
                                 data=e.get('data'))
    return datasets


def validate_data(datasets: Dict[str, DataSet]):
    """
    Performs a semantic validation on each element of a dict of Dataset

    :param datasets: A dict of :obj:`datasets <model.dataSet.DataSet>`.
    :return: A list of errors. See the Validation page
    """
    validations = {}
    for e in datasets.values():
        list_errors = e.semanticValidation()
        if len(list_errors) > 0:
            validations[e.structure.id] = list_errors
    if len(validations) is 0:
        return None
    else:
        return validations


def _get_size(obj, seen=None):
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
        size += sum([_get_size(v, seen) for v in obj.values()])
        size += sum([_get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += _get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([_get_size(i, seen) for i in obj])
    return size


def get_metadata(path_to_metadata):
    metadata = _read_xml(path_to_metadata)
    if isinstance(metadata, MetadataType):
        setReferences(metadata)
        return Message(payload=metadata.structures, message_type=MessageTypeEnum.Metadata, header=metadata.header)
    else:
        raise TypeError('Need a Structure file to be parsed')
