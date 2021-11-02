import csv
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd
import xmltodict

from sdmxthon.model.component import PrimaryMeasure
from sdmxthon.model.header import Header
from sdmxthon.parsers.data_validations import get_mandatory_attributes
from sdmxthon.parsers.message_parsers import Structures
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.mappings import messageAbbr, commonAbbr, genericAbbr, \
    structureSpecificAbbr, structureAbbr


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
                raise Exception('Dataset has no structure defined')
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


def write_from_header(header, prettyprint):
    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        nl = '\n'
    else:
        child1 = child2 = nl = ''

    outfile = f'{child1}<{messageAbbr}:Header>{nl}'
    if header.id_ is not None:
        outfile += f'{child2}<{messageAbbr}:ID>{header.id_}</{messageAbbr}:ID>'
    else:
        outfile += f'{child2}<{messageAbbr}:ID>test</{messageAbbr}:ID>'
    outfile += f'{nl}{child2}<{messageAbbr}:Test>'
    if header.test is not None:
        outfile += f'{str(header.test).lower()}'
    else:
        outfile += 'true'
    outfile += f'</{messageAbbr}:Test>'
    outfile += f'{nl}{child2}<{messageAbbr}:Prepared>'
    if header.prepared is not None:
        outfile += f'{header.prepared.strftime("%Y-%m-%dT%H:%M:%S")}'
    else:
        outfile += f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'
    outfile += f'</{messageAbbr}:Prepared>'

    outfile += f'{nl}{child2}<{messageAbbr}:Sender '
    if header.sender is not None:
        outfile += f'id="{header.sender.id_}"/>'
    else:
        outfile += 'id="Unknown"/>'

    if header.receiver is not None and len(header.receiver) > 0:
        for receiver in header.receiver:
            outfile += f'{nl}{child2}<{messageAbbr}:Receiver '
            outfile += f'id="{receiver.id_}"/>'
    else:
        outfile += f'{nl}{child2}<{messageAbbr}:Receiver '
        outfile += 'id="Not_supplied"/>'

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
                   f'{nl}{child2}<{messageAbbr}:Test>{test}' \
                   f'</{messageAbbr}:Test>' \
                   f'{nl}{child2}<{messageAbbr}:Prepared>' \
                   f'{prepared.strftime("%Y-%m-%dT%H:%M:%S")}' \
                   f'</{messageAbbr}:Prepared>' \
                   f'{nl}{child2}<{messageAbbr}:Sender id="{sender}"/>' \
                   f'{nl}{child2}<{messageAbbr}:Receiver id="{receiver}"/>'
    else:
        outfile += write_from_header(header, prettyprint)

    if isinstance(payload, dict) and dType is not MessageTypeEnum.Metadata:
        for record in payload.values():
            outfile += addStructure(record, prettyprint, dType)
    elif dType is not MessageTypeEnum.Metadata:
        outfile += addStructure(payload, prettyprint, dType)

    if dType is not MessageTypeEnum.Metadata and header is not None:
        if header.dataset_action is not None:
            outfile += f'{nl}{child2}<{messageAbbr}:DataSetAction>' \
                       f'{header.dataset_action}</{messageAbbr}:DataSetAction>'
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
                outfile += strWriting(record, prettyprint, count,
                                      record.dim_at_obs)
        else:
            outfile += strWriting(payload, prettyprint, dim=payload.dim_at_obs)
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


def strWriting(dataset, prettyprint=True, count=1, dim="AllDimensions"):
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

    # Datasets
    outfile += f'{child1}<{messageAbbr}:DataSet {attached_attributes_str}' \
               f'ss:structureRef="{dataset.structure.id}" ' \
               f'xsi:type="ns{count}:DataSetType" ' \
               f'ss:dataScope="DataStructure" ' \
               f'action="Replace">{nl}'
    man_att = get_mandatory_attributes(dataset.structure)
    opt_att_codes = [att for att in dataset.structure.attribute_codes
                     if att not in man_att]

    if dim == "AllDimensions":

        chunksize = 50000
        length_ = len(dataset.data)
        if len(dataset.data) > chunksize:
            previous = 0
            next_ = chunksize
            while previous <= length_:

                if next_ > length_:
                    outfile += obs_str(dataset.data.iloc[previous:],
                                       opt_att_codes, prettyprint)
                else:
                    outfile += obs_str(dataset.data.iloc[previous:next_],
                                       opt_att_codes, prettyprint)
                    outfile += f'{nl}'
                previous = next_
                next_ += chunksize
        else:
            outfile += obs_str(dataset.data, opt_att_codes, prettyprint)

    else:
        series_codes = []
        obs_codes = [dim, dataset.structure.measure_code]
        for e in dataset.structure.attribute_descriptor.components.values():
            if e.id in dataset.data.keys() and isinstance(e.related_to,
                                                          PrimaryMeasure):
                obs_codes.append(e.id)
        for e in dataset.data.keys():
            if ((e in dataset.structure.dimension_codes and e != dim)
                    or (e in dataset.structure.attribute_codes and
                        e not in obs_codes)):
                series_codes.append(e)
        outfile += ser_str(dataset.data, opt_att_codes, series_codes,
                           obs_codes, prettyprint)

    outfile += f'{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


def obs_str(data: pd.DataFrame,
            codes: list,
            prettyprint=True):
    data_dict = {
        'Obs': data.add_prefix('@').astype('str').replace('nan', '').to_dict(
            orient='records')}
    out = xmltodict.unparse(input_dict=data_dict, short_empty_elements=True,
                            pretty=prettyprint, depth=2, full_document=False)

    del data_dict

    for c in codes:
        out = out.replace(f'{c}="" ', '')

    return out


def ser_str(data: pd.DataFrame,
            opt_att_codes: list,
            series_codes: list,
            obs_codes: list,
            prettyprint=True):
    obs_codes = [f'@{v}' for v in obs_codes]

    # Getting each datapoint from data and creating dict

    data_dict = {'Series': data.sort_values(series_codes, axis=0)[
        series_codes].add_prefix('@').astype('str').replace('nan', '')
        .drop_duplicates().reset_index(drop=True).to_dict(orient="records")}

    for e in data_dict['Series']:
        # Filter each datapoint and get the obs as dict
        e['Obs'] = data.add_prefix('@').loc[
            (data.add_prefix('@')[list(e)] == pd.Series(e)).all(axis=1)][
            obs_codes].astype('str').replace('nan', '').to_dict(
            orient="records")

    out = xmltodict.unparse(input_dict=data_dict, short_empty_elements=True,
                            pretty=prettyprint, depth=2, full_document=False)

    del data_dict

    for c in opt_att_codes:
        out = out.replace(f'{c}="" ', '')

    return out


def genWriting(dataset, prettyprint=True):
    outfile = ''

    dataset.data = dataset.data.dropna(axis=1, how="all")

    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        child3 = '\t\t\t'
        nl = '\n'
    else:
        child1 = child2 = child3 = nl = ''

    outfile += f'{child1}<{messageAbbr}:DataSet ' \
               f'structureRef="{dataset.structure.id}" action="Replace">{nl}'
    if len(dataset.attached_attributes) > 0:
        outfile += f'{child2}<{genericAbbr}:Attributes>{nl}'
        for k, v in dataset.attached_attributes.items():
            outfile += f'{child3}<{genericAbbr}:Value id="{k}" ' \
                       f'value="{v}"/>{nl}'
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
    if len(dim_codes) == 1:
        df_id.loc[:, df_dim.columns[last_dim]] = \
            df_id.loc[:, df_dim.columns[last_dim]] + \
            f'{nl}{child3}</{genericAbbr}:ObsKey>'
    else:
        df_id.loc[:, df_dim.columns[last_dim]] = \
            df_dim.loc[:, df_dim.columns[last_dim]] + \
            f'{nl}{child3}</{genericAbbr}:ObsKey>'

    if len(att_codes) > 0:
        df_att = df_id[att_codes]
        df_id.loc[:, df_att.columns[0]] = f'{child3}<{genericAbbr}:' \
                                          f'Attributes>{nl}' + \
                                          df_att.loc[:, df_att.columns[0]]
        if len(att_codes) == 1:
            df_id.loc[:, df_att.columns[0]] = \
                df_id.loc[:, df_att.columns[0]] + \
                f'{nl}{child3}</{genericAbbr}:Attributes>'
        else:
            last_att = len(df_att.columns) - 1
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
