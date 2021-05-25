import csv
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd

from SDMXThon.utils.enums import MessageTypeEnum
from SDMXThon.utils.mappings import *
from .data_validations import get_mandatory_attributes
from .message_parsers import Structures
from ..model.component import PrimaryMeasure
from ..model.header import Header


def addStructure(dataset, prettyprint, dType):
    outfile = ''

    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = nl = ''

    outfile += f'{nl}{child2}<{messageAbbr}:Structure ' \
               f'structureID="{dataset.structure.id}" '
    if dType != MessageTypeEnum.GenericDataSet:
        outfile += f'namespace="urn:sdmx:org.sdmx.infomodel.' \
                   f'datastructure.DataStructure=' \
                   f'{dataset.structure.agencyID}:{dataset.structure.id}' \
                   f'({dataset.structure.version})" '

    outfile += f'dimensionAtObservation="{dataset.dim_at_obs}">{nl}'
    outfile += f'{child3}<{commonAbbr}:Structure>{nl}{child4}' \
               f'<Ref agencyID="{dataset.structure.agencyID}" ' \
               f'id="{dataset.structure.id}" ' \
               f'version="{dataset.structure.version}" ' \
               f'class="DataStructure"/>' \
               f'{nl}{child3}</{commonAbbr}:Structure>' \
               f'{nl}{child2}</{messageAbbr}:Structure>'

    return outfile


def create_namespaces(dataTypeString, payload, dType, prettyprint):
    if prettyprint:
        nl = '\n'
    else:
        nl = ''
    outfile = f'<?xml version="1.0" encoding="UTF-8"?>{nl}'
    outfile += f'<{messageAbbr}:{dataTypeString} ' \
               f'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
               f'xmlns:{messageAbbr}="http://www.sdmx.org/resources/sdmxml' \
               f'/schemas/v2_1/message" '
    if dType == MessageTypeEnum.GenericDataSet:
        outfile += f'xmlns:{genericAbbr}="http://www.sdmx.org/resources' \
                   f'/sdmxml/schemas/v2_1/data/generic" '
    elif dType == MessageTypeEnum.StructureDataSet:
        outfile += f'xmlns:{structureSpecificAbbr}="http://www.sdmx.org' \
                   f'/resources/sdmxml/schemas/v2_1/data/structurespecific" '
        if isinstance(payload, dict):
            count = 0
            for key, record in payload.items():
                count += 1
                if record.structure is None:
                    raise Exception(f'Dataset {key} has no structure defined')
                outfile += f'xmlns:ns{count}="urn:sdmx:org.sdmx.infomodel' \
                           f'.datastructure.DataStructure=' \
                           f'{record.structure.agencyID}:' \
                           f'{record.structure.id}' \
                           f'({record.structure.version})' \
                           f':ObsLevelDim:{record.dim_at_obs}" '
        else:
            if payload.structure is None:
                raise Exception(f'Dataset has no structure defined')
            outfile += f'xmlns:ns1="urn:sdmx:org.sdmx.infomodel' \
                       f'.datastructure.DataStructure=' \
                       f'{payload.structure.agencyID}:{payload.structure.id}' \
                       f'({payload.structure.version})' \
                       f':ObsLevelDim:{payload.dim_at_obs}" '
    else:
        outfile += f'xmlns:{structureAbbr}="http://www.sdmx.org/resources' \
                   f'/sdmxml/schemas/v2_1/structure" '
    outfile += f'xmlns:{commonAbbr}="http://www.sdmx.org/resources/sdmxml' \
               f'/schemas/v2_1/common" ' \
               f'xsi:schemaLocation="http://www.sdmx.org/resources/sdmxml' \
               f'/schemas/v2_1/message ' \
               f'https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd">{nl}'

    return outfile


def writer(path, payload, dType, prettyprint=True, id_='test',
           test='true',
           prepared=datetime.now(),
           sender='Unknown',
           receiver='Not_supplied',
           header: Header = None):
    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        nl = '\n'
    else:
        child1 = child2 = nl = ''

    if dType == MessageTypeEnum.GenericDataSet:
        data_type_string = 'GenericData'
    elif dType == MessageTypeEnum.StructureDataSet:
        data_type_string = 'StructureSpecificData'
    else:
        data_type_string = 'Structure'

    # Header
    outfile = create_namespaces(data_type_string, payload, dType, prettyprint)

    if header is None:
        outfile += f'{child1}<{messageAbbr}:Header>{nl}' \
                   f'{child2}<{messageAbbr}:ID>{id_}</{messageAbbr}:ID>' \
                   f'{nl}{child2}<{messageAbbr}:Test>{test}</{messageAbbr}:Test>' \
                   f'{nl}{child2}<{messageAbbr}:Prepared>' \
                   f'{prepared.strftime("%Y-%m-%dT%H:%M:%S")}' \
                   f'</{messageAbbr}:Prepared>' \
                   f'{nl}{child2}<{messageAbbr}:Sender id="{sender}"/>' \
                   f'{nl}{child2}<{messageAbbr}:Receiver id="{receiver}"/>'
    else:
        outfile += f'{child1}<{messageAbbr}:Header>{nl}' \
                   f'{child2}<{messageAbbr}:ID>{header.id_ if header.id_ is not None else "test"}</{messageAbbr}:ID>' \
                   f'{nl}{child2}<{messageAbbr}:Test>' \
                   f'{str(header.test).lower() if header.test is not None else "true"}</{messageAbbr}:Test>' \
                   f'{nl}{child2}<{messageAbbr}:Prepared>' \
                   f'{header.prepared.strftime("%Y-%m-%dT%H:%M:%S") if header.prepared is not None else datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}' \
                   f'</{messageAbbr}:Prepared>' \
                   f'{nl}{child2}<{messageAbbr}:Sender ' \
                   f'id="{header.sender.id_ if header.sender is not None else "Unknown"}"/>' \
                   f'{nl}{child2}<{messageAbbr}:Receiver ' \
                   f'id="{header.receiver[0].id_ if header.receiver is not None and len(header.receiver) > 0 else "Not_supplied"}"/>'

    if isinstance(payload, dict) and dType is not MessageTypeEnum.Metadata:
        for record in payload.values():
            outfile += addStructure(record, prettyprint, dType)
    elif dType is not MessageTypeEnum.Metadata:
        outfile += addStructure(payload, prettyprint, dType)

    if dType is not MessageTypeEnum.Metadata and header is not None:
        if header.dataset_action is not None:
            outfile += f'{nl}{child2}<{messageAbbr}:DataSetAction>{header.dataset_action}</{messageAbbr}:DataSetAction>'
    if header is not None:
        if header.source is not None:
            list_names = header.source._to_XML(name=f'{messageAbbr}:Source',
                                               prettyprint=True)
            for elem in list_names:
                outfile += f'{nl}{child1}' + elem
        else:
            outfile += f'{nl}{child2}<{messageAbbr}:Source xml:lang="en">' \
                       f'SDMXthon</{messageAbbr}:Source>'

    outfile += f'{nl}{child1}</{messageAbbr}:Header>{nl}'

    # Dataset
    if dType == MessageTypeEnum.GenericDataSet:
        if isinstance(payload, dict):
            for record in payload.values():
                outfile += genWriting(record, prettyprint)
        else:
            outfile += genWriting(payload, prettyprint)
    elif dType == MessageTypeEnum.StructureDataSet:
        if isinstance(payload, dict):
            count = 0
            for record in payload.values():
                count += 1
                if record.dim_at_obs == "AllDimensions":
                    outfile += strWriting(record, prettyprint, count)
                else:
                    outfile += strSerWriting(record, prettyprint, count)
        else:
            if payload.dim_at_obs == "AllDimensions":
                outfile += strWriting(payload, prettyprint)
            else:
                outfile += strSerWriting(payload, prettyprint)
    elif dType == MessageTypeEnum.Metadata and isinstance(payload, Structures):
        outfile += payload.to_XML(prettyprint)
    outfile += f'</{messageAbbr}:{data_type_string}>'

    if path != '':
        with open(path, "w", encoding="UTF-8", errors='replace') as f:
            f.write(outfile)
    else:
        f = StringIO()
        f.write(outfile)
        return f


def strWriting(dataset, prettyprint=True, count=1):
    outfile = ''

    dataset.data = dataset.data.dropna(axis=1, how="all")

    if prettyprint:
        child1 = '\t'
        nl = '\n'
    else:
        child1 = nl = ''

    attached_attributes_str = ''
    for k, v in dataset.attached_attributes.items():
        attached_attributes_str += f'{k}="{v}" '

    man_att = get_mandatory_attributes(dataset.structure)

    # Datasets
    outfile += f'{child1}<{messageAbbr}:DataSet {attached_attributes_str}' \
               f'ss:structureRef="{dataset.structure.id}" ' \
               f'xsi:type="ns{count}:DataSetType" ' \
               f'ss:dataScope="DataStructure" ' \
               f'action="Replace">{nl}'

    chunksize = 50000
    length_ = len(dataset.data)
    if len(dataset.data) > chunksize:
        previous = 0
        next_ = chunksize
        while previous <= length_:

            if next_ > length_:
                outfile += obs_str(dataset.data.iloc[previous:],
                                   dataset.structure.attribute_codes,
                                   man_att, prettyprint)
            else:
                outfile += obs_str(dataset.data.iloc[previous:next_],
                                   dataset.structure.attribute_codes,
                                   man_att, prettyprint)
                outfile += f'{nl}'
            previous = next_
            next_ += chunksize
    else:
        outfile += obs_str(dataset.data, dataset.structure.attribute_codes,
                           man_att, prettyprint)

    outfile += f'{nl}{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


def obs_str(data: pd.DataFrame, attribute_codes: list, man_att: list,
            prettyprint=True):
    if prettyprint:
        child2 = '\t\t'
        nl = '\n'
    else:
        child2 = nl = ''
    df1 = pd.DataFrame(
        np.tile(np.array(data.columns), len(data.index))
            .reshape(len(data.index), -1),
        index=data.index,
        columns=data.columns, dtype='str') + '='
    df2 = '"' + data.astype('str') + '"'
    df1 = df1.add(df2)
    df1.insert(0, 'head', f'{child2}<Obs')
    df1.insert(len(df1.keys()), 'end', '/>')
    obs_str = ''
    obs_str += df1.to_csv(path_or_buf=None, sep=' ', header=False, index=False,
                          quoting=csv.QUOTE_NONE, escapechar='\\')
    obs_str = obs_str.replace('\\', '')
    obs_str = f'{nl}'.join(obs_str.splitlines())

    obs_str = obs_str.replace('"nan"', '""')

    for e in attribute_codes:
        if e in df1.keys() and e not in man_att:
            obs_str = obs_str.replace(f'{e}="" ', '')

    return obs_str


def genWriting(dataset, prettyprint=True):
    outfile = ''

    dataset.data = dataset.data.dropna(axis=1, how="all")

    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child1 = child2 = child3 = child4 = nl = ''

    outfile += f'{child1}<{messageAbbr}:DataSet ' \
               f'structureRef="{dataset.structure.id}" action="Replace">{nl}'
    if len(dataset.attached_attributes) > 0:
        outfile += f'{child2}<{genericAbbr}:Attributes>{nl}'
        for k, v in dataset.attached_attributes.items():
            outfile += f'{child3}<{genericAbbr}:Value id="{k}" value="{v}"/>{nl}'
        outfile += f'{child2}</{genericAbbr}:Attributes>{nl}'

    man_att = get_mandatory_attributes(dataset.structure)
    outfile += obs_gen(dataset.data, dataset.structure.attribute_codes,
                       dataset.structure.dimension_codes,
                       man_att, prettyprint)

    outfile += f'{nl}{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


def obs_gen(data: pd.DataFrame, attribute_codes: list, dimension_codes: list,
            man_att: list,
            prettyprint=True):
    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = nl = ''
    df_data = data.astype('str')
    obs_value_data = df_data['OBS_VALUE'].astype('str')
    del df_data['OBS_VALUE']
    df_id = f'{child4}<{genericAbbr}:Value id="' + pd.DataFrame(
        np.tile(np.array(df_data.columns), len(df_data.index)).reshape(
            len(df_data.index), -1),
        index=df_data.index,
        columns=df_data.columns, dtype='str') + '" value="'
    df_value = df_data + '"/>'
    df_id: pd.DataFrame = df_id.add(df_value)
    df_obs_value = f'{child3}<{genericAbbr}:ObsValue value="' + \
                   obs_value_data + '"/>'
    df_obs_value = df_obs_value.replace(
        f'{child3}<{genericAbbr}:ObsValue value="nan"/>',
        f'{child3}<{genericAbbr}:ObsValue value=""/>')
    df_id['OBS_VALUE'] = df_obs_value

    df_id.insert(0, 'head', f'{child2}<{genericAbbr}:Obs>')
    df_id.insert(len(df_id.keys()), 'end', f'{child2}</{genericAbbr}:Obs>')

    dim_codes = []
    att_codes = []
    for e in df_id.keys():
        if e in dimension_codes:
            dim_codes.append(e)
        elif e in attribute_codes:
            att_codes.append(e)

    all_codes = ['head']
    all_codes += dim_codes.copy()
    all_codes.append('OBS_VALUE')
    all_codes += att_codes
    all_codes.append('end')
    df_id = df_id.reindex(all_codes, axis=1)

    df_dim = df_id[dim_codes]
    last_dim = len(df_dim.columns) - 1
    df_id.loc[:, df_dim.columns[0]] = f'{child3}<{genericAbbr}:ObsKey>{nl}' + \
                                      df_dim.loc[:, df_dim.columns[0]]
    df_id.loc[:, df_dim.columns[last_dim]] = \
        df_dim.loc[:, df_dim.columns[last_dim]] + \
        f'{nl}{child3}</{genericAbbr}:ObsKey>'

    df_att = df_id[att_codes]
    last_att = len(df_att.columns) - 1
    df_id.loc[:, df_att.columns[0]] = f'{child3}<{genericAbbr}:' \
                                      f'Attributes>{nl}' + \
                                      df_att.loc[:, df_att.columns[0]]
    df_id.loc[:, df_att.columns[last_att]] = \
        df_att.loc[:, df_att.columns[last_att]] + \
        f'{nl}{child3}</{genericAbbr}:Attributes>'

    obs_string = ''
    obs_string += df_id.to_csv(path_or_buf=None, sep='\n', header=False,
                               index=False, quoting=csv.QUOTE_NONE,
                               escapechar='\\')
    obs_string = obs_string.replace('\\', '')
    obs_string = obs_string.replace('="nan"', '=""')

    for e in attribute_codes:
        if e in df_id.keys() and e not in man_att:
            obs_string = obs_string.replace(
                f'{child4}<{genericAbbr}:Value id="{e}" value=""/>{nl}', '')

    df_data.add(obs_value_data)
    obs_string = f'{nl}'.join(obs_string.splitlines())

    return obs_string


def strSerWriting(dataset, prettyprint=True, count=1):
    outfile = ''

    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        child3 = '\t\t\t'
        child5 = '\t\t\t\t\t'
        nl = '\n'
    else:
        child1 = child2 = child3 = child5 = nl = ''

    mark_series = '//SeriesMark//'

    dim_obs = dataset.dim_at_obs

    attached_attributes_str = ''
    for k, v in dataset.attached_attributes.items():
        attached_attributes_str += f'{k}="{v}" '

    dataset.data = dataset.data.dropna(axis=1, how="all")

    # Datasets
    outfile += f'{child1}<{messageAbbr}:DataSet {attached_attributes_str}' \
               f'ss:structureRef="{dataset.structure.id}" ' \
               f'xsi:type="ns{count}:DataSetType" ' \
               f'ss:dataScope="DataStructure" ' \
               f'action="Replace">{nl}'

    series_codes = []
    obs_codes = [dim_obs, dataset.structure.measure_code]
    for e in dataset.structure.attribute_descriptor.components.values():
        if e.id in dataset.data.keys() and isinstance(e.related_to,
                                                      PrimaryMeasure):
            obs_codes.append(e.id)
    for e in dataset.data.keys():
        if (e in dataset.structure.dimension_codes and e != dim_obs) or (
                e in dataset.structure.attribute_codes and e not in obs_codes):
            series_codes.append(e)
    df = dataset.data.sort_values(series_codes, axis=0).astype('str')
    df = df.reset_index(drop=True)
    df_series: pd.DataFrame = df[series_codes].drop_duplicates()

    df1_series = pd.DataFrame(
        np.tile(np.array(series_codes), len(df_series.index)).reshape(
            len(df_series.index), -1),
        index=df_series.index,
        columns=series_codes, dtype='str') + '='
    df2_series = '"' + df_series.astype('str') + '"'
    df1_series = df1_series + df2_series
    df1_series.insert(0, 'head', f'{child2}<Series')
    df1_series.insert(len(df1_series.keys()), 'end', f'>{nl}')

    df1_obs = pd.DataFrame(
        np.tile(np.array(obs_codes), len(df[obs_codes].index)).reshape(
            len(df[obs_codes].index), -1),
        index=df[obs_codes].index,
        columns=obs_codes, dtype='str') + '='
    df2_obs = '"' + df[obs_codes].astype('str') + '"'
    df1_obs = df1_obs + df2_obs
    df1_obs.insert(0, 'head', f'{child3}<Obs')
    df1_obs.insert(len(df1_obs.keys()), 'end', '/>')

    del df
    df1_obs.iloc[df_series.index, 0] = f'{mark_series}' + df1_obs.iloc[
        df_series.index, 0]

    series_str = ''
    temp_str = ''
    series_str += df1_series.to_csv(path_or_buf=None, sep=' ', header=False,
                                    index=False, quoting=csv.QUOTE_NONE,
                                    escapechar='\\')
    series_str = series_str.replace('\\', '')
    series_str = series_str.replace('\r\n', '')
    series_str.replace('> ', '>')
    list_series = series_str.split('<')
    list_series = list_series[1:]
    temp_str += df1_obs.to_csv(path_or_buf=None, sep=' ', header=False,
                               index=False, quoting=csv.QUOTE_NONE,
                               escapechar='\\')
    temp_str = temp_str.replace('\\', '')
    temp_str = temp_str.replace('="nan"', '=""')
    temp_str = f'{nl}'.join(temp_str.splitlines())

    obs_codes.remove(dataset.structure.measure_code)

    for e in obs_codes:
        temp_str = temp_str.replace(f'{e}="" ', '')

    list_obs = temp_str.split(mark_series)
    list_obs = list_obs[1:]

    end_series = f'{nl}{child2}</Series>{nl}'
    outfile += ''.join([f"{child2}<" + str(a) + b + end_series for a, b in
                        zip(list_series, list_obs)])
    outfile = outfile.replace(f'{child5}', f'{child3}')
    outfile = outfile.replace(f'{nl}{nl}', f'{nl}')
    outfile += f'{child1}</{messageAbbr}:DataSet>{nl}'
    return outfile
