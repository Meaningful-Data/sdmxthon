"""
DataRead holds the functions to read the data from a SDMX file
"""
import itertools

import numpy as np
import pandas as pd

from sdmxthon.model.dataset import Dataset
from sdmxthon.utils.handlers import add_list
from sdmxthon.utils.parsing_words import (ATTRIBUTES, DIM_OBS, exc_attributes,
                                          GENERIC, ID, OBS, OBS_DIM, OBSKEY,
                                          OBSVALUE, SERIES, SERIESKEY, STRID,
                                          STRSPE, STRTYPE, VALUE)

chunksize = 50000


def get_element_to_list(data, mode):
    obs = {}
    if VALUE in data[mode]:
        data[mode][VALUE] = add_list(data[mode][VALUE])
        for k in data[mode][VALUE]:
            obs[k[ID]] = k[VALUE.lower()]
    return obs


def process_df(test_list: list, df: pd.DataFrame):
    if len(test_list) > 0:
        if df is not None:
            df = pd.concat([df, pd.DataFrame(test_list)],
                           ignore_index=True)
        else:
            df = pd.DataFrame(test_list)

    del test_list[:]

    return test_list, df


def reading_generic_series(dataset_info) -> pd.DataFrame:
    """
    Reads each series of a generic dataset
    :param dataset_info: Dict from Generic SDMX file
    :return: A DataFrame with all series
    """
    # Generic Series
    test_list = []
    df = None
    dataset_info[SERIES] = add_list(dataset_info[SERIES])
    for series in dataset_info[SERIES]:
        keys = dict()
        # Series Keys
        if not isinstance(series[SERIESKEY][VALUE], list):
            series[SERIESKEY][VALUE] = [series[SERIESKEY][VALUE]]
        for v in series[SERIESKEY][VALUE]:
            keys[v[ID]] = v[VALUE.lower()]
        if ATTRIBUTES in series:
            if not isinstance(series[ATTRIBUTES][VALUE], list):
                series[ATTRIBUTES][VALUE] = [series[ATTRIBUTES][VALUE]]
            for v in series[ATTRIBUTES][VALUE]:
                keys[v[ID]] = v[VALUE.lower()]
        if not isinstance(series[OBS], list):
            series[OBS] = [series[OBS]]
        for data in series[OBS]:
            obs = dict()
            obs[OBS_DIM] = data[OBS_DIM][VALUE.lower()]
            if OBSVALUE in data:
                obs[OBSVALUE.upper()] = data[OBSVALUE][VALUE.lower()]
            else:
                obs[OBSVALUE.upper()] = None
            if ATTRIBUTES in data:
                obs = {**obs, **get_element_to_list(data, mode=ATTRIBUTES)}
            test_list.append({**keys, **obs})
        if len(test_list) > chunksize:
            test_list, df = process_df(test_list, df)

    test_list, df = process_df(test_list, df)

    return df


def reading_generic_all(dataset_info) -> pd.DataFrame:
    """
    Reads each observation of a generic dataset
    :param dataset_info: Dict from Generic SDMX file
    :return: A DataFrame with all observations
    """
    # Generic All Dimensions
    test_list = []
    df = None
    dataset_info[OBS] = add_list(dataset_info[OBS])
    for data in dataset_info[OBS]:
        obs = dict()
        obs = {**obs, **get_element_to_list(data, mode=OBSKEY)}
        if ID in data[OBSVALUE]:
            obs[data[OBSVALUE][ID]] = data[OBSVALUE][VALUE.lower()]
        else:
            obs[OBSVALUE.upper()] = data[OBSVALUE][VALUE.lower()]
        obs = {**obs, **get_element_to_list(data, mode=ATTRIBUTES)}
        test_list.append({**obs})
        if len(test_list) > chunksize:
            test_list, df = process_df(test_list, df)

    test_list, df = process_df(test_list, df)

    return df


def reading_str_series(dataset_info) -> pd.DataFrame:
    """
    Reads each series of a structure specific dataset
    :param dataset_info: Dict from Structure Specific SDMX file
    :return: A DataFrame with all series
    """
    # Structure Specific Series
    test_list = []
    df = None
    dataset_info[SERIES] = add_list(dataset_info[SERIES])
    for data in dataset_info[SERIES]:
        keys = dict(itertools.islice(data.items(), len(data) - 1))
        if not isinstance(data[OBS], list):
            data[OBS] = [data[OBS]]
        for j in data[OBS]:
            test_list.append({**keys, **j})
        if len(test_list) > chunksize:
            test_list, df = process_df(test_list, df)

    test_list, df = process_df(test_list, df)

    return df


def get_at_att_str(dataset_info):
    """
    Gets Attached attributes from the dataset
    :param dataset_info: Dict from Structure Specific SDMX file
    :return: A dict with attached attributes
    """
    return {k: dataset_info[k] for k in dataset_info if k not in exc_attributes}


def get_at_att_gen(dataset_info):
    """
    Gets Attached attributes from the dataset
    :param dataset_info: Dict from Generic SDMX file
    :return: A dict with attached attributes
    """
    attached_attributes = {}
    if VALUE in dataset_info[ATTRIBUTES]:
        dataset_info[ATTRIBUTES][VALUE] = add_list(
            dataset_info[ATTRIBUTES][VALUE])
        for k in dataset_info[ATTRIBUTES][VALUE]:
            attached_attributes[k[ID]] = k[VALUE.lower()]
    return attached_attributes


def create_dataset(dataset_info, metadata, global_mode):
    """
    Creates a Dataset object from a SDMX data file
    :param dataset_info: Dict with dataset information
    :param metadata: Dict with metadata information
    :param global_mode: Mode of the SDMX data file (Structure Specific
                        or Generic)
    :return: A Dataset object
    """
    if STRSPE == global_mode:
        # Dataset info
        attached_attributes = get_at_att_str(dataset_info)

        # Parsing data
        if SERIES in dataset_info:
            # Structure Specific Series
            df = reading_str_series(dataset_info)
        elif OBS in dataset_info:
            # Structure Specific All dimensions
            df = pd.DataFrame(dataset_info[OBS]).replace(np.nan, '')
        else:
            df = pd.DataFrame()
    elif GENERIC == global_mode:

        # Dataset info
        if ATTRIBUTES in dataset_info:
            attached_attributes = get_at_att_gen(dataset_info)
        else:
            attached_attributes = {}

        # Parsing data
        if SERIES in dataset_info:
            # Generic Series
            df = reading_generic_series(dataset_info)
            renames = {'OBSVALUE': 'OBS_VALUE',
                       'ObsDimension': metadata[DIM_OBS]}
            df.rename(columns=renames, inplace=True)
        elif OBS in dataset_info:
            # Generic All Dimensions
            df = reading_generic_all(dataset_info)
            df.replace(np.nan, '', inplace=True)
            df.rename(columns={'OBSVALUE': 'OBS_VALUE'}, inplace=True)
        else:
            df = pd.DataFrame()
    else:
        raise Exception
    dataset_info = Dataset(attached_attributes=attached_attributes,
                           data=df,
                           unique_id=metadata[STRID],
                           structure_type=metadata[STRTYPE])

    return dataset_info
