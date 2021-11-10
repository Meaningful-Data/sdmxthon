import os
from io import BytesIO
from xml.parsers.expat import ExpatError

import requests
import validators
import xmltodict

from sdmxthon.parsers.new_data_read import create_dataset
from sdmxthon.parsers.new_metadata_read import create_metadata
from sdmxthon.utils.parsing_words import SERIES, OBS, STRSPE, GENERIC, \
    STRREF, STRUCTURE, STRID, namespaces, HEADER, DATASET, REF, AGENCY_ID, \
    ID, VERSION, DIM_OBS, ALL_DIM, STRUCTURES, STR_USAGE
from sdmxthon.utils.xml_base import parse_xml, validate_doc

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
                                                    mode=SERIES)
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


def read_xml(infile, validate=True):
    if validate:
        doc = parse_xml(infile, None)
        validate_doc(doc)

    if isinstance(infile, str):
        if validators.url(infile):
            try:
                response = requests.get(infile)
                if response.status_code == 400:
                    raise requests.ConnectionError(
                        f'Invalid URL. Response from server: {response.text}')
                infile = BytesIO(response.content)
            except requests.ConnectionError:
                raise requests.ConnectionError('Invalid URL. '
                                               'No response from server')
        elif infile[0] == '<':
            infile = BytesIO(bytes(infile, 'utf-8'))
        elif '/' in infile or '\\' in infile:
            try:
                infile = os.path.join(infile)
                with open(infile, "r", errors='ignore') as f:
                    infile = f.read()
            except AttributeError:
                infile = BytesIO(bytes(infile, 'utf-8'))
        else:
            raise ValueError(f'Unable to parse {infile}')
    else:
        if isinstance(infile, os.PathLike):
            try:
                infile = os.path.join(infile)
                with open(infile, "r", errors='replace') as f:
                    infile = f.read()
            except AttributeError:
                pass

    try:
        result = xmltodict.parse(infile, **options)
    except ExpatError:  # UTF-8 BOM
        result = xmltodict.parse(infile[3:], **options)

    del infile

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
