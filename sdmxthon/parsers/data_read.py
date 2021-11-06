import itertools

import numpy as np
import pandas as pd

from sdmxthon.model.dataset import Dataset
from sdmxthon.utils.handlers import add_list
from sdmxthon.utils.parsing_words import SERIES, OBS, ID, STRSPE, GENERIC, \
    SERIESKEY, ATTRIBUTES, VALUE, OBS_DIM, OBSVALUE, OBSKEY, DIM_OBS, \
    exc_attributes

chunksize = 50000


def get_element_to_list(data, mode):
    obs = {}
    if VALUE in data[mode]:
        if not isinstance(data[mode][VALUE], list):
            data[mode][VALUE] = [data[mode][VALUE]]
        for k in data[mode][VALUE]:
            obs[k[ID]] = k[VALUE.lower()]
    return obs


def process_df(test_list: list, df: pd.DataFrame):
    if len(test_list) > 0:
        if df is not None:
            df = pd.concat([df, pd.DataFrame(test_list)], ignore_index=True)
        else:
            df = pd.DataFrame(test_list)

    del test_list[:]

    return test_list, df


def reading_generic_series(dataset) -> pd.DataFrame:
    # Generic Series
    test_list = []
    df = None
    dataset[SERIES] = add_list(dataset[SERIES])
    for series in dataset[SERIES]:
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
            obs[OBSVALUE.upper()] = data[OBSVALUE][VALUE.lower()]
            if ATTRIBUTES in data:
                obs = {**obs, **get_element_to_list(data, mode=ATTRIBUTES)}
            test_list.append({**keys, **obs})
        if len(test_list) > chunksize:
            test_list, df = process_df(test_list, df)

    test_list, df = process_df(test_list, df)

    return df


def reading_generic_all(dataset) -> pd.DataFrame:
    # Generic All Dimensions
    test_list = []
    df = None
    dataset[OBS] = add_list(dataset[OBS])
    for data in dataset[OBS]:
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


def reading_str_series(dataset) -> pd.DataFrame:
    # Structure Specific Series
    test_list = []
    df = None
    dataset[SERIES] = add_list(dataset[SERIES])
    for data in dataset[SERIES]:
        keys = dict(itertools.islice(data.items(), len(data) - 1))
        if not isinstance(data[OBS], list):
            data[OBS] = [data[OBS]]
        for j in data[OBS]:
            test_list.append({**keys, **j})
        if len(test_list) > chunksize:
            test_list, df = process_df(test_list, df)

    test_list, df = process_df(test_list, df)

    return df


def get_at_att_str(dataset):
    return {k: dataset[k] for k in dataset if k not in exc_attributes}


def get_at_att_gen(dataset):
    attached_attributes = {}
    if VALUE in dataset[ATTRIBUTES]:
        for k in dataset[ATTRIBUTES][VALUE]:
            attached_attributes[k[ID]] = k[VALUE.lower()]
    return attached_attributes


def create_dataset(dataset, metadata, global_mode):
    if STRSPE == global_mode:
        # Dataset info
        attached_attributes = get_at_att_str(dataset)

        # Parsing data
        if SERIES in dataset:
            # Structure Specific Series
            df = reading_str_series(dataset)
        else:
            # Structure Specific All dimensions
            df = pd.DataFrame(dataset[OBS]).replace(np.nan, '')
    elif GENERIC == global_mode:

        # Dataset info
        if ATTRIBUTES in dataset:
            attached_attributes = get_at_att_gen(dataset)
        else:
            attached_attributes = {}

        # Parsing data
        if SERIES in dataset:
            # Generic Series
            df = reading_generic_series(dataset)
            renames = {'OBSVALUE': 'OBS_VALUE',
                       'ObsDimension': metadata[DIM_OBS]}
            df.rename(columns=renames, inplace=True)
        elif OBS in dataset:
            # Generic All Dimensions
            df = reading_generic_all(dataset)
            df.replace(np.nan, '', inplace=True)
            df.rename(columns={'OBSVALUE': 'OBS_VALUE'}, inplace=True)
        else:
            raise Exception
    else:
        raise Exception

    dataset = Dataset(attached_attributes=attached_attributes, data=df)

    return dataset
