import csv
import logging
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd

from .validations import get_mandatory_attributes
from .xml_base import makeWarnings
from ..utils.enums import DatasetType

logger = logging.getLogger("logger")


def save_file(message, path='', print_warnings=True):
    if path != '':
        gds_collector = message.gds_collector_
        makeWarnings(print_warnings, gds_collector)
        with open(path, "w") as f:
            message.export(f, 0, pretty_print=True, has_parent=False)
    else:
        f = StringIO()
        message.export(f, 0, pretty_print=True, has_parent=False)
        return f


def addStructure(dataset, prettyprint, dType):
    outfile = ''

    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = nl = ''

    outfile += f'{child2}<message:Structure structureID="{dataset.structure.id}" '
    if dType != DatasetType.GenericDataSet:
        outfile += f'namespace="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=' \
                   f'{dataset.structure.agencyId}:{dataset.structure.id}({dataset.structure.version})" '

    outfile += f'dimensionAtObservation="{dataset.dimAtObs}">{nl}'
    outfile += f'{child3}<common:Structure>{nl}{child4}<Ref agencyID="{dataset.structure.agencyId}" ' \
               f'id="{dataset.structure.id}" ' \
               f'version="{dataset.structure.version}" class="DataStructure"/>{nl}{child3}</common:Structure>' \
               f'{nl}{child2}</message:Structure>{nl}'

    return outfile


def create_namespaces(dataTypeString, dataset, dType, prettyprint):
    if prettyprint:
        nl = '\n'
    else:
        nl = ''
    outfile = f'<?xml version="1.0" encoding="UTF-8"?>{nl}'
    outfile += f'<message:{dataTypeString} xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
               f'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" '
    if dType == DatasetType.GenericDataSet:
        outfile += f'xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic" '
    else:
        outfile += f'xmlns:ss="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" '
        if isinstance(dataset, dict):
            count = 0
            for record in dataset.values():
                count = count + 1
                outfile += f'xmlns:ns{count}="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=' \
                           f'{record.structure.agencyId}:{record.structure.id}({record.structure.version})' \
                           f':ObsLevelDim:{record.dimAtObs}" '
        else:
            outfile += f'xmlns:ns1="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=' \
                       f'{dataset.structure.agencyId}:{dataset.structure.id}({dataset.structure.version})' \
                       f':ObsLevelDim:{dataset.dimAtObs}" '
    outfile += f'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" ' \
               f'xsi:schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message ' \
               f'https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd">{nl}'

    return outfile


def writer(path, dataset, dType, prettyprint=True, id_='test',
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

    if dType == DatasetType.GenericDataSet:
        data_type_string = 'GenericData'
    else:
        data_type_string = 'StructureSpecificData'

    # Header
    outfile = create_namespaces(data_type_string, dataset, dType, prettyprint)

    outfile += f'{child1}<message:Header>{nl}' \
               f'{child2}<message:ID>{id_}</message:ID>' \
               f'{nl}{child2}<message:Test>{test}</message:Test>' \
               f'{nl}{child2}<message:Prepared>{prepared.strftime("%Y-%m-%dT%H:%M:%S")}</message:Prepared>' \
               f'{nl}{child2}<message:Sender id="{sender}"/>' \
               f'{nl}{child2}<message:Receiver id="{receiver}"/>{nl}'

    if isinstance(dataset, dict):
        for record in dataset.values():
            outfile += addStructure(record, prettyprint, dType)
    else:
        outfile += addStructure(dataset, prettyprint, dType)

    outfile += f'{child1}</message:Header>{nl}'

    # Dataset
    if dType == DatasetType.GenericDataSet:
        if isinstance(dataset, dict):
            for record in dataset.values():
                outfile += genWriting(record, prettyprint)
                record.data = None
        else:
            outfile += genWriting(dataset, prettyprint)
    else:
        if isinstance(dataset, dict):
            count = 0
            for record in dataset.values():
                count = count + 1
                outfile += strWriting(record, prettyprint, count)
                record.data = None
        else:
            outfile += strWriting(dataset, prettyprint)
    outfile += f'</message:{data_type_string}>'

    if path != '':
        with open(path, "w") as f:
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
    outfile += f'{child1}<message:DataSet {attached_attributes_str}ss:structureRef="{dataset.structure.id}" ' \
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
    outfile += f'{nl}{child1}</message:DataSet>{nl}'

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

    outfile += f'{child1}<message:DataSet structureRef="{dataset.structure.id}" action="Replace">{nl}'
    if len(dataset.attachedAttributes) > 0:
        outfile += f'{child2}<generic:Attributes>{nl}'
        for k, v in dataset.attachedAttributes.items():
            outfile += f'{child3}<generic:Value id="{k}" value="{v}"/>{nl}'
        outfile += f'{child2}</generic:Attributes>{nl}'

    obs_value_data = dataset.data['OBS_VALUE'].astype('str')
    del dataset.data['OBS_VALUE']
    df_id = f'{child4}<generic:Value id="' + pd.DataFrame(
        np.tile(np.array(dataset.data.columns), len(dataset.data.index)).reshape(len(dataset.data.index), -1),
        index=dataset.data.index,
        columns=dataset.data.columns, dtype='str') + '" value="'
    df_value = dataset.data.astype('str') + '"/>'
    df_id: pd.DataFrame = df_id.add(df_value)
    df_obs_value = f'{child3}<generic:ObsValue value="' + obs_value_data + '"/>'
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
    outfile += f'{nl}{child1}</message:DataSet>{nl}'
    return outfile
