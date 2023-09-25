from zipfile import ZipFile

from sdmxthon.model.dataset import Dataset
from sdmxthon.model.message import Message
from sdmxthon.parsers.read import read_xml
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict, drop_na_all


def read_sdmx(sdmx_file, validate=True) -> Message:
    """
    Read SDMX performs the operation of reading a SDMX Data and SDMX
    metadata files. URLs could be used.

    :param sdmx_file: Path, URL or SDMX file as string
    :param validate: Validation of the XML file against the XSD (default: True)

    :return: A :obj:`Message <model.message.Message>` object
    """

    data = read_xml(sdmx_file, None, validate=validate)

    if isinstance(first_element_dict(data), Dataset):
        type_ = MessageTypeEnum.StructureDataSet
    else:
        type_ = MessageTypeEnum.Metadata
    return Message(type_, data)


def get_datasets(data, path_to_metadata, validate=True,
                 remove_empty_columns=True):
    """
    GetDatasets performs the operation of reading a SDMX Data and SDMX
    metadata files. URLs could be used.

    :param data: Path, URL or SDMX data file as string

    :param path_to_metadata: Path or URL to the SDMX metadata file

    :param validate: Validation of the XML file against the XSD (default: True)

    :param remove_empty_columns: Removes empty columns on output pd.Dataframe

    :return: A :obj:`Dataset <model.dataSet.DataSet>` object or a dict of \
    :obj:`Datasets <model.dataSet.DataSet>`
    """

    datasets = read_xml(data, mode="Data", validate=validate)

    metadata = read_xml(path_to_metadata,
                        mode="Metadata",
                        validate=validate)

    for v in datasets:
        if v in metadata['DataStructures']:
            datasets[v].structure = metadata['DataStructures'][v]
        elif v in metadata['Dataflows']:
            datasets[v].dataflow = metadata['Dataflows'][v]

        if remove_empty_columns:
            datasets[v].data = drop_na_all(datasets[v].data)

    if len(datasets) == 1:
        return first_element_dict(datasets)

    return datasets


def get_pandas_df(data, validate=True, remove_empty_columns=True):
    """
    GetPandasDF reads all observations in a SDMX file as Pandas Dataframe(s)

    :param data: Path, URL or SDMX data file as string

    :param validate: Validation of the XML file against the XSD (default: True)
    :param remove_empty_columns: Removes empty columns on output pd.Dataframe

    :return: A dict of `Pandas Dataframe \
    <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_
    """
    datasets = read_xml(data, "Data", validate=validate)
    if not remove_empty_columns:
        return {ds: datasets[ds].data for ds in datasets}
    else:
        return {ds: drop_na_all(datasets[ds].data) for ds in datasets}


def xml_to_csv(data, output_path=None, validate=True,
               remove_empty_columns=True, **kwargs):
    """
    XML to CSV transforms a SDMX file into a CSV. Saves the file on disk or
    .zip of CSV. If the SDMX data file has only a Dataset and output_path is
    '', it returns a StringIO object. Kwargs are supported.

    :param data: Path, URL or SDMX file as string (Data file)
    :param output_path: Path to save the CSV (default: None)
    :param validate: Validation of the XML file against the XSD (default: True)
    :param remove_empty_columns: Removes empty columns on output pd.Dataframe
    :param kwargs: Kwargs for `to_csv \
    <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html>`_

    :return: A StringIO object if output_path is ''
    """
    datasets = read_xml(data, mode="Data", validate=validate)

    if remove_empty_columns:
        for ds in datasets:
            datasets[ds].data = drop_na_all(datasets[ds].data)

    if output_path is not None and '.zip' in output_path:
        with ZipFile(output_path, 'w') as zipObj:
            # Add multiple files to the zip
            for record in datasets:
                zipObj.writestr(record + '.csv',
                                data=datasets[record].to_csv(**kwargs))

    else:
        if len(datasets) > 1:
            raise ValueError('Cannot introduce several Datasets in a CSV. '
                             'Consider using .zip in output path')
        if len(datasets) == 1:
            if output_path is not None and '.zip' in output_path:
                filename = output_path.split('.')[0]
                output_path = filename + '.csv'
            # Getting first value
            dataset = first_element_dict(datasets)

            return dataset.to_csv(output_path, **kwargs)

        raise ValueError('No Datasets were parsed')


def get_supported_agencies():
    "Returns the agencies supported by the API"
    from sdmxthon.webservices import webservices
    return {
        'BIS': webservices.BisWs,
        'ECB': webservices.EcbWs,
        'ESTAT': webservices.EuroStatWs,
        'ILO': webservices.IloWs,
        'OECD': webservices.OecdWs,
        'OECDv2': webservices.OecdWs2,
        'UNICEF': webservices.UnicefWs,
    }
