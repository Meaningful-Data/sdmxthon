from xml.parsers.expat import ExpatError

import pandas as pd
import xmltodict

from sdmxthon.model.dataset import Dataset
from sdmxthon.model.error import SDMXError
from sdmxthon.model.submission import SubmissionResult
from sdmxthon.parsers.data_read import create_dataset
from sdmxthon.parsers.metadata_read import create_metadata
from sdmxthon.parsers.reader_input_processor import process_string_to_read, \
    validate_doc
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import split_from_urn
from sdmxthon.utils.parsing_words import ACTION, AGENCY_ID, ALL_DIM, DATASET, \
    DATASET_ID, DIM_OBS, ERROR, ERROR_CODE, ERROR_MESSAGE, ERROR_TEXT, FAULT, \
    FAULTCODE, FAULTSTRING, GENERIC, \
    HEADER, ID, MAINTAINABLE_OBJECT, namespaces, OBS, REF, REG_INTERFACE, \
    SERIES, STATUS, STATUS_MSG, STR_USAGE, STRID, STRREF, STRSPE, STRTYPE, \
    STRUCTURE, STRUCTURES, SUBMISSION_RESULT, SUBMIT_STRUCTURE_RESPONSE, \
    SUBMITTED_STRUCTURE, URN, VERSION

options = {'process_namespaces': True,
           'namespaces': namespaces,
           'dict_constructor': dict,
           'attr_prefix': ''}


def parse_sdmx_ml(result, use_dataset_id=False):
    datasets = dict()

    if STRSPE in result:
        global_mode = STRSPE
    elif GENERIC in result:
        global_mode = GENERIC
    elif ERROR in result:
        if ERROR_MESSAGE in result[ERROR]:
            code = result[ERROR][ERROR_MESSAGE][ERROR_CODE]
            text = result[ERROR][ERROR_MESSAGE][ERROR_TEXT]
            return SDMXError(code=code, text=text), MessageTypeEnum.Error
        raise Exception('Cannot parse this sdmx error message')
    elif STRUCTURE in result:
        global_mode = STRUCTURE
    elif REG_INTERFACE in result:
        return handle_registry_interface(result), MessageTypeEnum.Submission
    elif FAULT in result:
        raise Exception(f'SOAP API error: Code ({result[FAULT][FAULTCODE]}). '
                        f'Message: {result[FAULT][FAULTSTRING]}')
    else:
        raise Exception('Cannot parse this sdmx file')

    if global_mode == STRUCTURE:
        # Parsing Structure
        return create_metadata(result[STRUCTURE][STRUCTURES])

    # Getting datasets
    message = result[global_mode]
    type_ = MessageTypeEnum.GenericDataSet if global_mode == GENERIC else \
        MessageTypeEnum.StructureSpecificDataSet
    dataset_key = None
    for key in message:
        if DATASET in key:
            dataset_key = key
    if dataset_key is None:
        raise Exception('Cannot parse datasets on this file')

    if isinstance(message[dataset_key], list):
        structures = {}
        # Relationship between structures and structure id
        for structure in message[HEADER][STRUCTURE]:
            structures[structure[STRID]] = structure
        for single_dataset in message[dataset_key]:
            str_ref = single_dataset[STRREF]
            if SERIES in single_dataset:
                metadata = get_dataset_metadata(structures[str_ref],
                                                str_ref,
                                                mode=SERIES)
            else:
                metadata = get_dataset_metadata(structures[str_ref],
                                                str_ref,
                                                mode=OBS)
            ds = create_dataset(single_dataset, metadata,
                                global_mode)
            datasets[metadata[STRID]] = ds
    else:

        if SERIES in message[dataset_key]:
            metadata = get_dataset_metadata(message[HEADER][STRUCTURE],
                                            message[dataset_key][STRREF],
                                            mode=SERIES)
        elif OBS in message[dataset_key]:
            metadata = get_dataset_metadata(message[HEADER][STRUCTURE],
                                            message[dataset_key][STRREF],
                                            mode=OBS)
        else:
            if message[HEADER][STRUCTURE][DIM_OBS] == "AllDimensions":
                mode = OBS
            else:
                mode = SERIES
            metadata = get_dataset_metadata(message[HEADER][STRUCTURE],
                                            message[dataset_key][STRREF],
                                            mode=mode)
        ds = create_dataset(message[dataset_key], metadata, global_mode)

        if use_dataset_id and DATASET_ID in message[HEADER]:
            dataset_id = message[HEADER][DATASET_ID]
            datasets[dataset_id] = ds
        else:
            datasets[metadata[STRID]] = ds

    return datasets, type_


def generate_dataset_from_sdmx_csv(data: pd.DataFrame, sdmx_csv_version):
    # Extract Structure type and structure id
    if sdmx_csv_version == 1:
        # For SDMX-CSV version 1, use 'DATAFLOW' column as the structure id
        structure_id = data['DATAFLOW'].iloc[0]
        # Structure type will be "dataflow" in both versions
        structure_type = 'dataflow'
        # Drop 'DATAFLOW' column from DataFrame
        df_csv = data.drop(['DATAFLOW'], axis=1)
    else:
        # For SDMX-CSV version 2, use 'STRUCTURE_ID'
        # column as the structure id and 'STRUCTURE' as the structure type
        structure_id = data['STRUCTURE_ID'].iloc[0]
        structure_type = data['STRUCTURE'].iloc[0]
        # Drop 'STRUCTURE' and 'STRUCTURE_ID' columns from DataFrame
        df_csv = data.drop(['STRUCTURE', 'STRUCTURE_ID'], axis=1)

    # Return a Dataset object with the extracted information
    return Dataset(unique_id=structure_id, structure_type=structure_type,
                   data=df_csv)


def read_sdmx_csv(infile: str):
    """
    ReadSDMXCSV reads a SDMX-CSV file as a dict of Datasets
    :param infile: Path, URL or SDMX-CSV file as string
    :return: A dict of Datasets
    """
    # Get Dataframe from CSV file
    df_csv = pd.read_csv(infile)
    # Drop empty columns
    df_csv = df_csv.dropna(axis=1, how='all')

    # Determine SDMX-CSV version based on column names
    if 'DATAFLOW' in df_csv.columns:
        version = 1
    elif 'STRUCTURE' in df_csv.columns and 'STRUCTURE_ID' in df_csv.columns:
        version = 2
    else:
        # Raise an exception if the CSV file is not in SDMX-CSV format
        raise Exception('Invalid CSV file, only SDMX-CSV is allowed')

    # Convert all columns to strings
    df_csv = df_csv.astype('str')
    # Check if any column headers contain ':', indicating mode, label or text
    mode_label_text = any([':' in x for x in df_csv.columns])

    # Determine the id column based on the SDMX-CSV version
    if version == 1:
        id_column = 'DATAFLOW'
    else:
        id_column = 'STRUCTURE_ID'

    # If mode, label or text is present, modify the DataFrame
    if mode_label_text:
        # Split the ID column to remove mode, label or text
        df_csv[id_column] = df_csv[id_column].map(lambda x: x.split(': ')[0])
        # Split the other columns to remove mode, label, or text
        for x in df_csv.columns[version:]:
            df_csv[x.split(':')[0]] = df_csv[x].map(
                lambda x: x.split(': ', 2)[0],
                na_action='ignore')
            # Delete the original columns
            del df_csv[x]

    # Separate SDMX-CSV in different datasets per Structure ID
    list_df = [data for _, data in df_csv.groupby(id_column)]

    # Create a payload dictionary to store datasets with the
    # different unique_ids as keys
    payload = {}
    for df in list_df:
        # Generate a dataset from each subset of the DataFrame
        dataset = generate_dataset_from_sdmx_csv(data=df,
                                                 sdmx_csv_version=version)
        # Add the dataset to the payload dictionary
        payload[dataset.unique_id] = dataset

    # Return the payload generated
    return payload


def read_xml(infile: str, mode: str = None,
             validate: bool = True,
             use_dataset_id: bool = False):
    """
    ReadXML reads a SDMX file as a dict of Datasets or Metadata dict
    :param infile: Path, URL or SDMX file as string
    :param mode: "Data", "Metadata" or "Submission"
    :param validate: Validation of the XML file against the XSD (default: True)
    :param use_dataset_id: Use the dataset id as key in the dict (default: False)
    :return:
    """
    infile, filetype = process_string_to_read(infile)
    if validate:
        validate_doc(infile)
    try:
        dict_info = xmltodict.parse(infile, **options)
    except ExpatError as e:
        if e.offset > 10:  # UTF-8 BOM
            raise e
        dict_info = xmltodict.parse(infile[3:], **options)

    del infile

    if mode is not None:
        if mode == "Data" and (STRSPE not in dict_info and
                               GENERIC not in dict_info):
            raise TypeError("Unable to parse sdmx file as data file")
        elif mode == "Metadata" and (STRUCTURE not in dict_info):
            raise TypeError("Unable to parse sdmx file as metadata file")
        elif mode == "Submission" and (ERROR not in dict_info and
                                       REG_INTERFACE not in dict_info):
            raise TypeError("Unable to parse sdmx file as error file")
        elif mode not in ["Data", "Metadata", "Error"]:
            raise ValueError("Wrong mode")

    return parse_sdmx_ml(dict_info, use_dataset_id)



def get_ids_from_structure(element: dict):
    if REF in element:
        agency_id = element[REF][AGENCY_ID]
        id_ = element[REF][ID]
        version = element[REF][VERSION]
        return agency_id, id_, version
    elif URN in element:
        return split_from_urn(element[URN])
    return None, None, None


def get_elements_from_structure(structure):
    if STRUCTURE in structure:
        structure_type = "datastructure"
        tuple_ids = get_ids_from_structure(structure[STRUCTURE])

    elif STR_USAGE in structure:
        structure_type = "dataflow"
        tuple_ids = get_ids_from_structure(structure[STR_USAGE])
    else:
        return None, None, None, None
    return tuple_ids + (structure_type,)


def get_dataset_metadata(structure, dataset_ref, mode):
    if mode == SERIES and structure[DIM_OBS] == ALL_DIM:
        raise Exception
    elif mode == OBS and structure[DIM_OBS] != ALL_DIM:
        raise Exception

    if dataset_ref == structure[STRID]:
        (agency_id, id_,
         version, structure_type) = get_elements_from_structure(structure)
        if agency_id is not None:
            str_id = f"{agency_id}:{id_}({version})"
        else:
            str_id = f"{id_}({version})"
        return {DIM_OBS: structure[DIM_OBS],
                STRID: str_id,
                STRTYPE: structure_type}
    else:
        raise Exception("Could not find structure reference")


def handle_registry_interface(dict_info) -> dict:
    if SUBMIT_STRUCTURE_RESPONSE in dict_info[REG_INTERFACE]:
        response = dict_info[REG_INTERFACE][SUBMIT_STRUCTURE_RESPONSE]
        if SUBMISSION_RESULT in response:
            if isinstance(response[SUBMISSION_RESULT], list):
                result = {}
                for submission_result in response[SUBMISSION_RESULT]:
                    if SUBMITTED_STRUCTURE not in submission_result:
                        raise Exception(f"Cannot parse this SubmissionResult, "
                                        f"missing {SUBMITTED_STRUCTURE}")
                    if STATUS_MSG not in submission_result:
                        raise Exception(f"Cannot parse this SubmissionResult, "
                                        f"missing {STATUS_MSG}")
                    structure = submission_result[SUBMITTED_STRUCTURE]
                    action = structure[ACTION]
                    urn = structure[MAINTAINABLE_OBJECT][URN]
                    full_id = split_from_urn(urn, split_id=False)
                    status = submission_result[STATUS_MSG][STATUS]
                    result[full_id] = SubmissionResult(action, full_id, status)
                return result
    raise Exception("Cannot parse this registry interface message")
