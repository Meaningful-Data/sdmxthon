from xml.parsers.expat import ExpatError

import xmltodict

from sdmxthon.parsers.data_read import create_dataset
from sdmxthon.parsers.metadata_read import create_metadata
from sdmxthon.utils.parsing_words import SERIES, OBS, STRSPE, GENERIC, \
    STRREF, STRUCTURE, STRID, namespaces, HEADER, DATASET, REF, AGENCY_ID, \
    ID, VERSION, DIM_OBS, ALL_DIM, STRUCTURES, STR_USAGE
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
    else:
        global_mode = STRUCTURE

    if global_mode == STRUCTURE:
        # Parsing Structure
        return create_metadata(result[STRUCTURE][STRUCTURES])
    else:
        message = result[global_mode]
        if isinstance(message[DATASET], list):
            structures = {}
            # Relationship between structures and structure id
            for structure in message[HEADER][STRUCTURE]:
                structures[structure[STRID]] = structure
            for single_dataset in message[DATASET]:
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
            if SERIES in message[DATASET]:
                metadata = get_dataset_metadata(message[HEADER][STRUCTURE],
                                                message[DATASET][STRREF],
                                                mode=SERIES)
            else:
                metadata = get_dataset_metadata(message[HEADER][STRUCTURE],
                                                message[DATASET][STRREF],
                                                mode=OBS)

            ds = create_dataset(message[DATASET], metadata, global_mode)
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


def get_elements_from_structure(structure):
    if STRUCTURE in structure:
        agency_id = structure[STRUCTURE][REF][AGENCY_ID]
        id_ = structure[STRUCTURE][REF][ID]
        version = structure[STRUCTURE][REF][VERSION]
    else:
        agency_id = structure[STR_USAGE][REF][AGENCY_ID]
        id_ = structure[STR_USAGE][REF][ID]
        version = structure[STR_USAGE][REF][VERSION]
    return agency_id, id_, version


def get_dataset_metadata(structure, dataset_ref, mode):
    if mode == SERIES and structure[DIM_OBS] == ALL_DIM:
        raise Exception
    elif mode == OBS and structure[DIM_OBS] != ALL_DIM:
        raise Exception

    if dataset_ref == structure[STRID]:
        agency_id, id_, version = get_elements_from_structure(structure)
        return {DIM_OBS: structure[DIM_OBS],
                STRID: f"{agency_id}:{id_}({version})"}
    else:
        raise Exception
