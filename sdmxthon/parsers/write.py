import csv
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd

from SDMXthon.model.component import PrimaryMeasure
from SDMXthon.utils.enums import MessageTypeEnum
from SDMXthon.utils.mappings import *
from .data_validations import get_mandatory_attributes
from .message_parsers import Structures


def addStructure(dataset, prettyprint, dType):
    outfile = ''

    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = nl = ''

    outfile += f'{child2}<{messageAbbr}:Structure structureID="{dataset.structure.id}" '
    if dType != MessageTypeEnum.GenericDataSet:
        outfile += f'namespace="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=' \
                   f'{dataset.structure.agencyID}:{dataset.structure.id}({dataset.structure.version})" '

    outfile += f'dimensionAtObservation="{dataset.dimAtObs}">{nl}'
    outfile += f'{child3}<{commonAbbr}:Structure>{nl}{child4}<Ref agencyID="{dataset.structure.agencyID}" ' \
               f'id="{dataset.structure.id}" ' \
               f'version="{dataset.structure.version}" class="DataStructure"/>{nl}{child3}</{commonAbbr}:Structure>' \
               f'{nl}{child2}</{messageAbbr}:Structure>{nl}'

    return outfile


def create_namespaces(dataTypeString, payload, dType, prettyprint):
    if prettyprint:
        nl = '\n'
    else:
        nl = ''
    outfile = f'<?xml version="1.0" encoding="UTF-8"?>{nl}'
    outfile += f'<{messageAbbr}:{dataTypeString} xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
               f'xmlns:{messageAbbr}="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" '
    if dType == MessageTypeEnum.GenericDataSet:
        outfile += f'xmlns:{genericAbbr}="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic" '
    elif dType == MessageTypeEnum.StructureDataSet:
        outfile += f'xmlns:{structureSpecificAbbr}="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" '
        if isinstance(payload, dict):
            count = 0
            for record in payload.values():
                count += 1
                outfile += f'xmlns:ns{count}="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=' \
                           f'{record.structure.agencyID}:{record.structure.id}({record.structure.version})' \
                           f':ObsLevelDim:{record.dimAtObs}" '
        else:
            outfile += f'xmlns:ns1="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=' \
                       f'{payload.structure.agencyID}:{payload.structure.id}({payload.structure.version})' \
                       f':ObsLevelDim:{payload.dimAtObs}" '
    else:
        outfile += f'xmlns:{structureAbbr}="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure" '
    outfile += f'xmlns:{commonAbbr}="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" ' \
               f'xsi:schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message ' \
               f'https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd">{nl}'

    return outfile


def writer(path, payload, dType, prettyprint=True, id_='test',
           test='true',
           prepared=datetime.now(),
           sender='Unknown',
           receiver='Not_supplied'):
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

    outfile += f'{child1}<{messageAbbr}:Header>{nl}' \
               f'{child2}<{messageAbbr}:ID>{id_}</{messageAbbr}:ID>' \
               f'{nl}{child2}<{messageAbbr}:Test>{test}</{messageAbbr}:Test>' \
               f'{nl}{child2}<{messageAbbr}:Prepared>{prepared.strftime("%Y-%m-%dT%H:%M:%S")}</{messageAbbr}:Prepared>' \
               f'{nl}{child2}<{messageAbbr}:Sender id="{sender}"/>' \
               f'{nl}{child2}<{messageAbbr}:Receiver id="{receiver}"/>{nl}'

    if isinstance(payload, dict) and dType is not MessageTypeEnum.Metadata:
        for record in payload.values():
            outfile += addStructure(record, prettyprint, dType)
    elif dType is not MessageTypeEnum.Metadata:
        outfile += addStructure(payload, prettyprint, dType)

    outfile += f'{child1}</{messageAbbr}:Header>{nl}'

    # Dataset
    if dType == MessageTypeEnum.GenericDataSet:
        if isinstance(payload, dict):
            for record in payload.values():
                outfile += genWriting(record, prettyprint)
                record.data = None
        else:
            outfile += genWriting(payload, prettyprint)
    elif dType == MessageTypeEnum.StructureDataSet:
        if isinstance(payload, dict):
            count = 0
            for record in payload.values():
                count += 1
                if record.dimAtObs == "AllDimensions":
                    outfile += strWriting(record, prettyprint, count)
                else:
                    outfile += strSerWriting(record, prettyprint, count)
                record.data = None
        else:
            if payload.dimAtObs == "AllDimensions":
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
        child2 = '\t\t'
        nl = '\n'
    else:
        child1 = child2 = nl = ''

    attached_attributes_str = ''
    for k, v in dataset.attachedAttributes.items():
        attached_attributes_str += f'{k}="{v}" '

    # Datasets
    outfile += f'{child1}<{messageAbbr}:DataSet {attached_attributes_str}ss:structureRef="{dataset.structure.id}" ' \
               f'xsi:type="ns{count}:DataSetType" ss:dataScope="DataStructure" ' \
               f'action="Replace">{nl}'
    df1 = pd.DataFrame(np.tile(np.array(dataset.data.columns), len(dataset.data.index))
                       .reshape(len(dataset.data.index), -1),
                       index=dataset.data.index,
                       columns=dataset.data.columns, dtype='str') + '='
    df2 = '"' + dataset.data.astype('str') + '"'
    df1 = df1.add(df2)
    df1.insert(0, 'head', f'{child2}<Obs')
    df1.insert(len(df1.keys()), 'end', '/>')
    obs_str = ''
    obs_str += df1.to_csv(path_or_buf=None, sep=' ', header=False, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
    obs_str = obs_str.replace('\\', '')
    obs_str = f'{nl}'.join(obs_str.splitlines())

    man_att = get_mandatory_attributes(dataset.structure)

    obs_str = obs_str.replace('"nan"', '""')

    for e in dataset.structure.attributeCodes:
        if e in df1.keys() and e not in man_att:
            obs_str = obs_str.replace(f'{e}="" ', '')

    outfile += obs_str
    outfile += f'{nl}{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


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

    outfile += f'{child1}<{messageAbbr}:DataSet structureRef="{dataset.structure.id}" action="Replace">{nl}'
    if len(dataset.attachedAttributes) > 0:
        outfile += f'{child2}<generic:Attributes>{nl}'
        for k, v in dataset.attachedAttributes.items():
            outfile += f'{child3}<generic:Value id="{k}" value="{v}"/>{nl}'
        outfile += f'{child2}</generic:Attributes>{nl}'

    df_data = dataset.data.astype('str')
    obs_value_data = df_data['OBS_VALUE'].astype('str')
    del df_data['OBS_VALUE']
    df_id = f'{child4}<generic:Value id="' + pd.DataFrame(
        np.tile(np.array(df_data.columns), len(df_data.index)).reshape(len(df_data.index), -1),
        index=df_data.index,
        columns=df_data.columns, dtype='str') + '" value="'
    df_value = df_data + '"/>'
    df_id: pd.DataFrame = df_id.add(df_value)
    df_obs_value = f'{child3}<generic:ObsValue value="' + obs_value_data + '"/>'
    df_obs_value = df_obs_value.replace(f'{child3}<generic:ObsValue value="nan"/>', f'{child3}<generic:ObsValue />')
    df_id['OBS_VALUE'] = df_obs_value

    df_id.insert(0, 'head', f'{child2}<generic:Obs>')
    df_id.insert(len(df_id.keys()), 'end', f'{child2}</generic:Obs>')

    dim_codes = []
    att_codes = []
    for e in df_id.keys():
        if e in dataset.structure.dimensionCodes:
            dim_codes.append(e)
        elif e in dataset.structure.attributeCodes:
            att_codes.append(e)

    all_codes = ['head']
    all_codes += dim_codes.copy()
    all_codes.append('OBS_VALUE')
    all_codes += att_codes
    all_codes.append('end')
    df_id = df_id.reindex(all_codes, axis=1)

    df_dim = df_id[dim_codes]
    last_dim = len(df_dim.columns) - 1
    df_id.loc[:, df_dim.columns[0]] = f'{child3}<generic:ObsKey>{nl}' + df_dim.loc[:, df_dim.columns[0]]
    df_id.loc[:, df_dim.columns[last_dim]] = df_dim.loc[:, df_dim.columns[last_dim]] + f'{nl}{child3}</generic:ObsKey>'

    df_att = df_id[att_codes]
    last_att = len(df_att.columns) - 1
    df_id.loc[:, df_att.columns[0]] = f'{child3}<generic:Attributes>{nl}' + df_att.loc[:, df_att.columns[0]]
    df_id.loc[:, df_att.columns[last_att]] = df_att.loc[:, df_att.columns[last_att]] + f'{nl}' \
                                                                                       f'{child3}</generic:Attributes>'

    obs_str = ''
    obs_str += df_id.to_csv(path_or_buf=None, sep='\n', header=False, index=False, quoting=csv.QUOTE_NONE,
                            escapechar='\\')
    obs_str = obs_str.replace('\\', '')
    obs_str = obs_str.replace('="nan"', '=""')
    man_att = get_mandatory_attributes(dataset.structure)

    for e in dataset.structure.attributeCodes:
        if e in df_id.keys() and e not in man_att:
            obs_str = obs_str.replace(f'{child4}<generic:Value id="{e}" value=""/>{nl}', '')

    obs_str = f'{nl}'.join(obs_str.splitlines())

    outfile += obs_str
    outfile += f'{nl}{child1}</{messageAbbr}:DataSet>{nl}'

    df_data.add(obs_value_data)

    return outfile


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

    dim_obs = dataset.dimAtObs

    attached_attributes_str = ''
    for k, v in dataset.attachedAttributes.items():
        attached_attributes_str += f'{k}="{v}" '

    dataset.data = dataset.data.dropna(axis=1, how="all")

    # Datasets
    outfile += f'{child1}<{messageAbbr}:DataSet {attached_attributes_str}ss:structureRef="{dataset.structure.id}" ' \
               f'xsi:type="ns{count}:DataSetType" ss:dataScope="DataStructure" ' \
               f'action="Replace">{nl}'

    series_codes = []
    obs_codes = [dim_obs, dataset.structure.measureCode]
    for e in dataset.structure.attributeDescriptor.components.values():
        if e.id in dataset.data.keys() and isinstance(e.relatedTo, PrimaryMeasure):
            obs_codes.append(e.id)
    for e in dataset.data.keys():
        if (e in dataset.structure.dimensionCodes and e != dim_obs) or (
                e in dataset.structure.attributeCodes and e not in obs_codes):
            series_codes.append(e)
    df = dataset.data.sort_values(series_codes, axis=0).astype('str')
    df = df.reset_index(drop=True)
    df_series: pd.DataFrame = df[series_codes].drop_duplicates()

    df1_series = pd.DataFrame(np.tile(np.array(series_codes), len(df_series.index))
                              .reshape(len(df_series.index), -1),
                              index=df_series.index,
                              columns=series_codes, dtype='str') + '='
    df2_series = '"' + df_series.astype('str') + '"'
    df1_series = df1_series + df2_series
    df1_series.insert(0, 'head', f'{child2}<Series')
    df1_series.insert(len(df1_series.keys()), 'end', f'>{nl}')

    df1_obs = pd.DataFrame(np.tile(np.array(obs_codes), len(df[obs_codes].index))
                           .reshape(len(df[obs_codes].index), -1),
                           index=df[obs_codes].index,
                           columns=obs_codes, dtype='str') + '='
    df2_obs = '"' + df[obs_codes].astype('str') + '"'
    df1_obs = df1_obs + df2_obs
    df1_obs.insert(0, 'head', f'{child3}<Obs')
    df1_obs.insert(len(df1_obs.keys()), 'end', '/>')

    del df
    df1_obs.iloc[df_series.index, 0] = f'{mark_series}' + df1_obs.iloc[df_series.index, 0]

    series_str = ''
    temp_str = ''
    series_str += df1_series.to_csv(path_or_buf=None, sep=' ', header=False, index=False, quoting=csv.QUOTE_NONE,
                                    escapechar='\\')
    series_str = series_str.replace('\\', '')
    series_str = series_str.replace('\r\n', '')
    series_str.replace('> ', '>')
    list_series = series_str.split('<')
    list_series = list_series[1:]
    temp_str += df1_obs.to_csv(path_or_buf=None, sep=' ', header=False, index=False, quoting=csv.QUOTE_NONE,
                               escapechar='\\')
    temp_str = temp_str.replace('\\', '')
    temp_str = temp_str.replace('="nan"', '=""')
    temp_str = f'{nl}'.join(temp_str.splitlines())

    obs_codes.remove(dataset.structure.measureCode)

    for e in obs_codes:
        temp_str = temp_str.replace(f'{e}="" ', '')

    list_obs = temp_str.split(mark_series)
    list_obs = list_obs[1:]

    end_series = f'{nl}{child2}</Series>{nl}'
    outfile += ''.join([f"{child2}<" + str(a) + b + end_series for a, b in zip(list_series, list_obs)])
    outfile = outfile.replace(f'{child5}', f'{child3}')
    outfile = outfile.replace(f'{nl}{nl}', f'{nl}')
    outfile += f'{child1}</{messageAbbr}:DataSet>{nl}'
    return outfile
