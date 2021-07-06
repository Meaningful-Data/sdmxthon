from zipfile import ZipFile

from sdmxthon.model.message import Message
from sdmxthon.parsers.message_parsers import MetadataType
from sdmxthon.parsers.metadata_validations import _set_references
from sdmxthon.parsers.read import _read_xml, _sdmx_gen_to_dataset, \
    _sdmx_str_to_dataset, _sdmx_to_dataframe, \
    _sdmx_to_dataset_no_metadata
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict


def read_sdmx(sdmx_file, validate=True) -> Message:
    """
    Read SDMX performs the operation of reading a SDMX Data and SDMX
    metadata files. URLs could be used.

    :param sdmx_file: Path, URL or SDMX file as string
    :param validate: Validation of the XML file against the XSD (default: True)

    :return: A :obj:`Message <model.message.Message>` object
    """

    obj_ = _read_xml(sdmx_file, validate=validate)
    if isinstance(obj_, MetadataType):
        _set_references(obj_)

    header = obj_.header
    if obj_.original_tag_name_ == 'GenericData':
        type_ = MessageTypeEnum.GenericDataSet
        data = _sdmx_to_dataset_no_metadata(obj_, type_)
    elif obj_.original_tag_name_ == 'StructureSpecificData':
        type_ = MessageTypeEnum.StructureDataSet
        data = _sdmx_to_dataset_no_metadata(obj_, type_)
    elif obj_.original_tag_name_ == 'Structure':
        type_ = MessageTypeEnum.Metadata
        data = obj_.structures
    else:
        raise ValueError('Wrong Message type')
    return Message(type_, data, header)


def get_datasets(data, path_to_metadata, validate=True):
    """
    GetDatasets performs the operation of reading a SDMX Data and SDMX
    metadata files. URLs could be used.

    :param data: Path, URL or SDMX data file as string

    :param path_to_metadata: Path or URL to the SDMX metadata file

    :param validate: Validation of the XML file against the XSD (default: True)


    :return: A :obj:`Dataset <model.dataSet.DataSet>` object or a dict of \
    :obj:`Datasets <model.dataSet.DataSet>`
    """

    obj_ = _read_xml(data, validate=validate)

    metadata = read_sdmx(path_to_metadata, validate=validate)

    if obj_.original_tag_name_ == 'GenericData':
        datasets = _sdmx_gen_to_dataset(obj_, metadata.payload.dsds,
                                        metadata.payload.dataflows)
    elif obj_.original_tag_name_ == 'StructureSpecificData':
        datasets = _sdmx_str_to_dataset(obj_, metadata.payload.dsds,
                                        metadata.payload.dataflows)
    else:
        raise ValueError('Wrong Message type')

    if len(datasets) == 1:
        return first_element_dict(datasets)

    return datasets


def get_pandas_df(data, validate=True):
    """
    GetPandasDF reads all observations in a SDMX file as Pandas Dataframe(s)

    :param data: Path, URL or SDMX data file as string

    :param validate: Validation of the XML file against the XSD (default: True)

    :return: A dict of `Pandas Dataframe \
    <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_
    """
    obj_ = _read_xml(data, validate=validate)

    if isinstance(obj_, MetadataType):
        raise TypeError('No data available in a Structure file. '
                        'You should use read_sdmx method')

    if obj_.original_tag_name_ == 'GenericData':
        type_ = MessageTypeEnum.GenericDataSet
    elif obj_.original_tag_name_ == 'StructureSpecificData':
        type_ = MessageTypeEnum.StructureDataSet
    else:
        raise ValueError('No data available in a Structure file. '
                         'You should use read_sdmx method')

    return _sdmx_to_dataframe(obj_, type_)

  
def xml_to_csv(data, output_path=None, validate=True, **kwargs):
    """
    XML to CSV transforms a SDMX file into a CSV. Saves the file on disk or
    .zip of CSV. If the SDMX data file has only a Dataset and output_path is
    '', it returns a StringIO object. Kwargs are supported.

    :param data: Path, URL or SDMX file as string
    :param output_path: Path to save the CSV (default: None)
    :param validate: Validation of the XML file against the XSD (default: True)
    :return: A StringIO object if output_path is ''
    """
    message = read_sdmx(data, validate=validate)
    if message.type == MessageTypeEnum.Metadata:
        raise TypeError('Metadata files are not allowed here')

    if output_path is not None and '.zip' in output_path:
        with ZipFile(output_path, 'w') as zipObj:
            # Add multiple files to the zip
            for record in message.payload.values():
                zipObj.writestr(record.structure.id + '.csv',
                                data=record.to_csv(**kwargs))

    else:
        if len(message.payload) > 1:
            raise ValueError('Cannot introduce several Datasets in a CSV. '
                             'Consider using .zip in output path')
        elif len(message.payload) == 1:
            if output_path is not None and '.zip' in output_path:
                filename = output_path.split('.')[0]
                output_path = filename + '.csv'
            # Getting first value
            dataset = first_element_dict(message.payload)

            return dataset.to_csv(output_path, **kwargs)

        raise ValueError('No Datasets were parsed')
