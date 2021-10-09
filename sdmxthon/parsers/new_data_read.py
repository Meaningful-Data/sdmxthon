import itertools

import numpy as np
import pandas as pd

from sdmxthon.model.dataset import Dataset
from sdmxthon.utils.parsing_words import SERIES, OBS, ID, STRSPE, GENERIC, \
    SERIESKEY, ATTRIBUTES, VALUE, OBS_DIM, OBSVALUE, OBSKEY, DIM_OBS, \
    exc_attributes


def get_element_to_list(data, mode):
    obs = {}
    if VALUE in data[mode]:
        if not isinstance(data[mode][VALUE], list):
            data[mode][VALUE] = [data[mode][VALUE]]
        for k in data[mode][VALUE]:
            obs[k[ID]] = k[VALUE.lower()]
    return obs


def reading_generic_series(dataset):
    # Generic Series
    test_list = []
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

    return test_list


def reading_generic_all(dataset):
    # Generic All Dimensions
    test_list = []
    for data in dataset[OBS]:
        obs = dict()
        obs = {**obs, **get_element_to_list(data, mode=OBSKEY)}
        if ID in data[OBSVALUE]:
            obs[data[OBSVALUE][ID]] = data[OBSVALUE][VALUE.lower()]
        else:
            obs[OBSVALUE.upper()] = data[OBSVALUE][VALUE.lower()]
        obs = {**obs, **get_element_to_list(data, mode=ATTRIBUTES)}
        test_list.append({**obs})

    return test_list


def reading_str_series(dataset):
    # Structure Specific Series
    test_list = []
    for data in dataset[SERIES]:
        keys = dict(itertools.islice(data.items(), len(data) - 1))
        if not isinstance(data[OBS], list):
            data[OBS] = [data[OBS]]
        for j in data[OBS]:
            test_list.append({**keys, **j})

    return test_list


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
            df = pd.DataFrame(reading_str_series(dataset))
        else:
            # Structure Specific All dimensions
            df = pd.DataFrame(dataset[OBS])
            df.replace(np.nan, '', inplace=True)
    elif GENERIC == global_mode:

        # Dataset info
        attached_attributes = get_at_att_gen(dataset)

        # Parsing data
        if SERIES in dataset:
            # Generic Series
            df = pd.DataFrame(reading_generic_series(dataset))
            renames = {'OBSVALUE': 'OBS_VALUE',
                       'ObsDimension': metadata[DIM_OBS]}
            df.rename(columns=renames, inplace=True)
        elif OBS in dataset:
            # Generic All Dimensions
            df = pd.DataFrame(reading_generic_all(dataset))
            df.replace(np.nan, '', inplace=True)
            df.rename(columns={'OBSVALUE': 'OBS_VALUE'}, inplace=True)
        else:
            raise Exception
    else:
        raise Exception

    dataset = Dataset(attached_attributes=attached_attributes, data=df)

    return dataset
