import xmltodict

from sdmxthon.parsers.new_data_read import create_dataset
from sdmxthon.parsers.new_matadata_read import create_metadata
from sdmxthon.utils.parsing_words import SERIES, OBS, STRSPE, GENERIC, \
    STRREF, STRUCTURE, STRID, namespaces, HEADER, DATASET, REF, AGENCY_ID, ID, \
    VERSION, DIM_OBS, ALL_DIM, STRUCTURES
from sdmxthon.utils.xml_base import parse_xml, validate_doc


def parse_sdmx(result):
    datasets = {}

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


def read_xml(xml, validate=True):
    if validate:
        doc = parse_xml(xml, None)
        validate_doc(doc)

    result = xmltodict.parse(xml,
                             process_namespaces=True,
                             namespaces=namespaces,
                             dict_constructor=dict,
                             attr_prefix='')

    datasets = parse_sdmx(result)
    return datasets


def get_elements_from_structure(structure):
    agency_id = structure[STRUCTURE][REF][AGENCY_ID]
    id_ = structure[STRUCTURE][REF][ID]
    version = structure[STRUCTURE][REF][VERSION]
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
