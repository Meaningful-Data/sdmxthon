"""
API module contains the functions to read SDMX files and transform them into
Pandas Dataframes or CSV files. It also contains the function to get the
supported agencies by the API.
"""
import os
from pathlib import Path
from zipfile import ZipFile

from sdmxthon.model.error import SDMXError
from sdmxthon.model.message import Message
from sdmxthon.model.submission import SubmissionResult
from sdmxthon.parsers.read import read_sdmx_csv, read_xml
from sdmxthon.parsers.reader_input_processor import process_string_to_read
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import drop_na_all, first_element_dict
from sdmxthon.webservices.fmr import submit_structures_to_fmr
from sdmxthon.webservices.webservices import BisWs, EcbWs, EuroStatWs, IloWs, \
    OecdWs, \
    OecdWs2, \
    UnicefWs


def read_sdmx(sdmx_file, validate=False, use_dataset_id=False) -> Message:
    """
    Read SDMX performs the operation of reading a SDMX Data and SDMX
    metadata files in XML or CSV format. URLs could be used.

    :param sdmx_file: Path, URL or SDMX file as string
    :param validate: Validation of the XML file against the XSD (default: False)
    :param use_dataset_id: Use the DataSetID as key in output (default: True)

    :return: A :obj:`Message <sdmxthon.model.message.Message>` object
    """
    if isinstance(sdmx_file, Path):
        sdmx_file = str(sdmx_file)

    # Process the SDMX file and check the file type
    infile, filetype = process_string_to_read(sdmx_file)
    if filetype == "xml":
        payload, type_ = read_xml(infile, None, validate=validate,
                                  use_dataset_id=use_dataset_id)
    elif filetype == "json":
        raise Exception('Json is not supported')
    elif filetype == "csv":
        payload = read_sdmx_csv(infile)
        type_ = MessageTypeEnum.StructureSpecificDataSet

    else:
        raise Exception("File type is not recognised")

    if isinstance(payload, dict):
        first_element = first_element_dict(payload)

        if type_ == MessageTypeEnum.StructureSpecificDataSet:

            if len(payload) > 1:
                payload = dict(payload.values())
            else:
                if use_dataset_id:
                    first_element._unique_id = list(payload.keys())[0]
                payload = first_element

        elif isinstance(first_element, SubmissionResult):
            type_ = MessageTypeEnum.Submission

    elif isinstance(payload, SDMXError):
        type_ = MessageTypeEnum.Error
    else:
        raise Exception("Unable to set Message Type")
    return Message(message_type=type_, payload=payload)


def get_datasets(path_to_data, path_to_metadata, validate=True,
                 remove_empty_columns=True):
    """
    GetDatasets performs the operation of reading a SDMX Data and SDMX
    metadata files. URLs could be used.

    :param path_to_data: Path, URL or SDMX data file as string

    :param path_to_metadata: Path or URL to the SDMX metadata file

    :param validate: Validation of the XML file against the XSD (default: True)

    :param remove_empty_columns: Removes empty columns on output pd.Dataframe

    :return: A :obj:`Dataset <sdmxthon.model.dataset.DataSet>` object or a \
    dict of :obj:`Datasets <sdmxthon.model.dataset.DataSet>`
    """

    message_datasets = read_sdmx(path_to_data, validate=validate)

    if message_datasets.type != MessageTypeEnum.StructureSpecificDataSet:
        raise ValueError('The message is not a StructureSpecificDataSet')

    datasets = message_datasets.content['datasets']

    metadata, message_type = read_xml(path_to_metadata,
                                      mode="Metadata",
                                      validate=validate)

    for v in datasets:
        if 'DataStructures' in metadata:
            if v in metadata['DataStructures']:
                datasets[v].structure = metadata['DataStructures'][v]
        if 'Dataflows' in metadata:
            if v in metadata['Dataflows']:
                datasets[v].dataflow = metadata['Dataflows'][v]

        if remove_empty_columns:
            datasets[v].data = drop_na_all(datasets[v].data)

    if len(datasets) == 1:
        return first_element_dict(datasets)

    return datasets


def get_pandas_df(path_to_data, validate=True, remove_empty_columns=True,
                  use_dataset_id=False):
    """
    GetPandasDF reads all observations in a SDMX file as Pandas Dataframe(s)

    :param path_to_data: Path, URL or SDMX data file as string

    :param validate: Validation of the XML file against the XSD (default: True)
    :param remove_empty_columns: Removes empty columns on output pd.Dataframe
    :param use_dataset_id: Use the DataSetID as key in output (default: False)

    :return: A dict of `Pandas Dataframe \
    <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_
    """
    message_datasets = read_sdmx(path_to_data, validate=validate,
                                 use_dataset_id=use_dataset_id)

    if message_datasets.type != MessageTypeEnum.StructureSpecificDataSet:
        raise ValueError('Only SDMX data messages are allowed in get_pandas_df')

    datasets = message_datasets.content['datasets']
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
    datasets, message_type = read_xml(data, mode="Data", validate=validate,
                                      use_dataset_id=True)

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
    """Returns the agencies supported by the API"""
    return {
        'BIS': BisWs,
        'ECB': EcbWs,
        'ESTAT': EuroStatWs,
        'ILO': IloWs,
        'OECD': OecdWs,
        'OECDv2': OecdWs2,
        'UNICEF': UnicefWs,
    }


def upload_metadata_to_fmr(data: (str, os.PathLike),
                           host: str = 'localhost',
                           port: int = 8080,
                           user: str = 'root',
                           password: str = 'password',
                           use_https: bool = False
                           ):
    """
     Uploads metadata to FMR instance

    :param data: Either a string containing SDMX metadata or a path
                 to a file with SDMX metadata
    :type data: str or a path to a file

    :param host: The FMR instance host (default is 'localhost')
    :type host: str

    :param port: The FMR instance port (default is 8080)
    :type port: str

    :param user: The username for authentication (default is 'root')
    :type user: str

    :param password: The password for authentication (default is 'password')
    :type password: str

    :param use_https: A boolean indicating whether to use HTTPS
                      (default is False)
    :type use_https: bool

    :exception: Exception with error details if upload fails
    """

    # Process the input data to obtain SDMX text
    sdmx_text, extension = process_string_to_read(data)

    if extension != 'xml':
        raise ValueError('Only SDMX-ML is supported')

    # Submit the SDMX structures to FMR for processing
    submit_structures_to_fmr(
        sdmx_text=sdmx_text,
        host=host,
        port=port,
        user=user,
        password=password,
        use_https=use_https
    )
