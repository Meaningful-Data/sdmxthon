from xml.parsers.expat import ExpatError

import xmltodict

from sdmxthon.parsers.data_read import create_dataset
from sdmxthon.parsers.metadata_read import create_metadata
from sdmxthon.utils.handlers import split_from_urn
from sdmxthon.utils.parsing_words import SERIES, OBS, STRSPE, GENERIC, \
    STRREF, STRUCTURE, STRID, namespaces, HEADER, DATASET, REF, AGENCY_ID, \
    ID, VERSION, DIM_OBS, ALL_DIM, STRUCTURES, STR_USAGE, URN
from sdmxthon.utils.xml_base import validate_doc, \
    process_string_to_read

options = {'process_namespaces': True,
           'namespaces': namespaces,
           'dict_constructor': dict,
           'attr_prefix': ''}


def parse_sdmx(result):
    datasets = dict()

    if STRSPE in result:
        global_mode = STRSPE
    elif GENERIC in result:
        global_mode = GENERIC
    elif 'Error' in result:
        if 'ErrorMessage' in result['Error']:
            raise Exception(result['Error']['ErrorMessage'])
        raise Exception(result['Error'])
    else:
        global_mode = STRUCTURE

    if global_mode == STRUCTURE:
        # Parsing Structure
        return create_metadata(result[STRUCTURE][STRUCTURES])
    else:
        message = result[global_mode]
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
            datasets[metadata[STRID]] = ds

    return datasets


def read_xml(infile, mode=None, validate=True):
    infile = process_string_to_read(infile)

    if validate:
        validate_doc(infile)
    try:
        result = xmltodict.parse(infile, **options)
    except ExpatError as e:
        if e.offset > 10:  # UTF-8 BOM
            raise e
        result = xmltodict.parse(infile[3:], **options)

    del infile

    if mode is not None:
        if mode == "Data" and STRUCTURE in result:
            raise TypeError("Unable to parse metadata file as data file")
        elif mode == "Metadata" and (STRSPE in result or GENERIC in result):
            raise TypeError("Unable to parse data file as metadata file")
        elif mode not in ["Data", "Metadata"]:
            raise ValueError("Wrong mode")

    datasets = parse_sdmx(result)
    return datasets


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
        return get_ids_from_structure(structure[STRUCTURE])

    elif STR_USAGE in structure:
        return get_ids_from_structure(structure[STR_USAGE])

    return None, None, None


def get_dataset_metadata(structure, dataset_ref, mode):
    if mode == SERIES and structure[DIM_OBS] == ALL_DIM:
        raise Exception
    elif mode == OBS and structure[DIM_OBS] != ALL_DIM:
        raise Exception

    if dataset_ref == structure[STRID]:
        agency_id, id_, version = get_elements_from_structure(structure)
        if agency_id is not None:
            return {DIM_OBS: structure[DIM_OBS],
                    STRID: f"{agency_id}:{id_}({version})"}
        else:
            return {DIM_OBS: structure[DIM_OBS],
                    STRID: f"{id_}({version})"}
    else:
        raise Exception
