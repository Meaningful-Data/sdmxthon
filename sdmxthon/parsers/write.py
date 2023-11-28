from datetime import datetime

import pandas as pd

from sdmxthon.model.component import PrimaryMeasure
from sdmxthon.model.header import Header, Sender, Party
from sdmxthon.parsers.data_validations import get_mandatory_attributes
from sdmxthon.parsers.writer_aux import create_namespaces, write_from_header, \
    parse_metadata, get_end_message
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.mappings import messageAbbr, genericAbbr

chunksize = 100000


#
#      --------------------------------------------
#     |                                            |
#     |                   Common                   |
#     |                                            |
#      --------------------------------------------
#


def process_dataset(dataset):
    dataset.data = dataset.data.fillna(value='')
    return dataset


def writer(path, payload, type_, prettyprint=True, id_='test',
           test='true',
           prepared=datetime.now(),
           sender='Unknown',
           receiver='Not_supplied',
           header: Header = None):
    # Header
    outfile = create_namespaces(type_, payload, prettyprint)

    if header is None:
        header = Header(ID=id_,
                        Test=test,
                        Prepared=prepared,
                        sender=Sender(sender),
                        Receiver=[Party(receiver)])

    outfile += write_from_header(header=header, prettyprint=prettyprint,
                                 type_=type_, payload=payload)

    # Dataset
    if type_ == MessageTypeEnum.GenericDataSet:
        if isinstance(payload, dict):
            for record in payload.values():
                record = process_dataset(record)
                outfile += genWriting(record, prettyprint, record.dim_at_obs)
        else:
            payload = process_dataset(payload)
            outfile += genWriting(payload, prettyprint, dim=payload.dim_at_obs)
    elif type_ == MessageTypeEnum.StructureSpecificDataSet:
        if isinstance(payload, dict):
            count = 0
            for record in payload.values():
                count += 1
                record = process_dataset(record)
                outfile += strWriting(record, prettyprint, count,
                                      record.dim_at_obs)
        else:
            payload = process_dataset(payload)
            outfile += strWriting(payload, prettyprint, dim=payload.dim_at_obs)
    elif type_ == MessageTypeEnum.Metadata:
        if len(payload) > 0:
            outfile += parse_metadata(payload, prettyprint)

    outfile += get_end_message(type_)

    if path != '':
        with open(path, "w", encoding="UTF-8", errors='replace') as f:
            f.write(outfile)
    else:
        return outfile


def format_dict_ser(out, parser, data_dict, obs):
    data_dict['Series'][0]['Obs'] = obs.to_dict(orient="records")
    out.append(parser(data_dict['Series'][0]))
    del data_dict['Series'][0]


def series_process(parser, data, data_dict, series_codes, obs_codes):
    out = []
    if all(elem in data.columns for elem in obs_codes):
        data.groupby(by=series_codes)[obs_codes].apply(
            lambda x: format_dict_ser(out, parser, data_dict, x))

    return ''.join(out)


def get_codes(dim, dataset):
    series_codes = []
    obs_codes = [dim, dataset.structure.measure_code]
    for e in dataset.structure.attribute_descriptor.components.values():
        if e.id in dataset.data.keys() and isinstance(e.related_to,
                                                      PrimaryMeasure):
            obs_codes.append(e.id)
    for e in dataset.data.keys():
        if ((e in dataset.structure.dimension_codes and e != dim) or
                (e in dataset.structure.attribute_codes and
                 e not in obs_codes)):
            series_codes.append(e)

    return series_codes, obs_codes


#
#      --------------------------------------------
#     |                                            |
#     |              Structure Specific            |
#     |                                            |
#      --------------------------------------------
#

def memory_optimization_str(dataset, opt_att_codes, prettyprint):
    outfile = ""
    length_ = len(dataset.data)
    if len(dataset.data) > chunksize:
        previous = 0
        next_ = chunksize
        while previous <= length_:
            outfile += obs_str(dataset.data.iloc[previous:next_],
                               opt_att_codes, prettyprint)
            previous = next_
            next_ += chunksize

            if next_ >= length_:
                outfile += obs_str(dataset.data.iloc[previous:],
                                   opt_att_codes, prettyprint)
                previous = next_
    else:
        outfile += obs_str(dataset.data, opt_att_codes, prettyprint)

    return outfile


def strWriting(dataset, prettyprint=True, count=1, dim="AllDimensions"):
    outfile = ''

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
        outfile += memory_optimization_str(dataset, opt_att_codes, prettyprint)
    else:
        series_codes, obs_codes = get_codes(dim, dataset)
        outfile += ser_str(dataset.data, opt_att_codes, series_codes,
                           obs_codes, prettyprint)

    outfile += f'{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


def format_obs_str(data: dict, prettyprint: bool) -> str:
    if prettyprint:
        child2 = '\t\t'
        nl = '\n'
    else:
        child2 = nl = ''

    out = f"{child2}<Obs "

    for k, v in data.items():
        out += f'{k}="{v}" '

    out += f"/>{nl}"

    return out


def obs_str(data: pd.DataFrame,
            codes: list,
            prettyprint=True) -> str:
    parser = lambda x: format_obs_str(x, prettyprint)  # noqa: E731

    iterator = map(parser, data.to_dict(orient='records'))
    out = ''.join(iterator)

    for c in codes:
        out = out.replace(f'{c}="" ', '')

    return out


def format_ser_str(data: dict, prettyprint: bool) -> str:
    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = nl = ''

    out = f"{child2}<Series "

    for k, v in data.items():
        if k != 'Obs':
            out += f'{k}="{v}" '

    out += f">{nl}"

    for obs in data['Obs']:
        out += f"{child3}<Obs "

        for k, v in obs.items():
            out += f'{k}="{v}" '

        out += f"/>{nl}"

    out += f"{child2}</Series>{nl}"

    return out


def ser_str(data: pd.DataFrame,
            opt_att_codes: list,
            series_codes: list,
            obs_codes: list,
            prettyprint=True) -> str:
    # Getting each datapoint from data and creating dict
    data = data.sort_values(series_codes, axis=0)
    data_dict = {'Series': data[series_codes].drop_duplicates().reset_index(
        drop=True).to_dict(orient="records")}

    parser = lambda x: format_ser_str(data=x,  # noqa: E731
                                      prettyprint=prettyprint)

    out = series_process(parser=parser, data=data, data_dict=data_dict,
                         series_codes=series_codes, obs_codes=obs_codes)

    for c in opt_att_codes:
        out = out.replace(f'{c}="" ', '')

    return out


#
#      --------------------------------------------
#     |                                            |
#     |                   Generic                  |
#     |                                            |
#      --------------------------------------------
#

def memory_optimization_gen(dataset, dim_codes, att_codes, measure_code,
                            prettyprint):
    outfile = ""
    length_ = len(dataset.data)
    if len(dataset.data) > chunksize:
        previous = 0
        next_ = chunksize
        while previous <= length_:
            outfile += obs_gen(dataset.data.iloc[previous:next_],
                               dim_codes=dim_codes,
                               att_codes=att_codes,
                               measure_code=measure_code,
                               prettyprint=prettyprint)
            previous = next_
            next_ += chunksize

            if next_ >= length_:
                outfile += obs_gen(dataset.data.iloc[previous:length_],
                                   dim_codes=dim_codes,
                                   att_codes=att_codes,
                                   measure_code=measure_code,
                                   prettyprint=prettyprint)
                previous = next_
    else:
        outfile += obs_gen(dataset.data,
                           dim_codes=dim_codes,
                           att_codes=att_codes,
                           measure_code=measure_code,
                           prettyprint=prettyprint)

    return outfile


def genWriting(dataset, prettyprint=True, dim="AllDimensions"):
    outfile = ''

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

    dim_codes = [v for v in dataset.structure.dimension_codes if
                 v in dataset.data.columns]
    att_codes = [v for v in dataset.structure.attribute_codes if
                 v in dataset.data.columns]
    measure_code = dataset.structure.measure_code

    if dim == "AllDimensions":
        outfile += memory_optimization_gen(dataset, dim_codes, att_codes,
                                           measure_code, prettyprint)
    else:
        series_codes, obs_codes = get_codes(dim, dataset)

        outfile += ser_gen(dataset.data,
                           dim_codes=dim_codes,
                           att_codes=att_codes,
                           measure_code=measure_code,
                           prettyprint=prettyprint,
                           series_codes=series_codes,
                           obs_codes=obs_codes)

    outfile += f'{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


def format_measure_att(data, measure_code, att_codes, child3, child4, nl):
    out = ""
    if measure_code != "OBS_VALUE":
        out += f'{child3}<{genericAbbr}:ObsValue id="{measure_code}" ' \
               f'value="{data[measure_code]}"/>{nl}'
    else:
        out += f'{child3}<{genericAbbr}:ObsValue ' \
               f'value="{data[measure_code]}"/>{nl}'

    if len(att_codes) > 0:
        out += f"{child3}<{genericAbbr}:Attributes>{nl}"

        for k in att_codes:
            if data[k] != '':
                out += f'{child4}<{genericAbbr}:Value id="{k}" ' \
                       f'value="{data[k]}"/>{nl}'

        out += f"{child3}</{genericAbbr}:Attributes>{nl}"

    return out


def format_obs(data: dict,
               dim_codes: list,
               att_codes: list,
               measure_code: str,
               prettyprint=True):
    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = nl = ''

    out = f"{child2}<{genericAbbr}:Obs>{nl}"

    out += f"{child3}<{genericAbbr}:ObsKey>{nl}"

    for k in dim_codes:
        out += f'{child4}<{genericAbbr}:Value id="{k}" value="{data[k]}"/>{nl}'

    out += f"{child3}</{genericAbbr}:ObsKey>{nl}"

    out += format_measure_att(data, measure_code, att_codes,
                              child3, child4, nl)

    out += f"{child2}</{genericAbbr}:Obs>{nl}"

    return out


def obs_gen(data: pd.DataFrame,
            dim_codes: list,
            att_codes: list,
            measure_code: str,
            prettyprint=True):
    parser = lambda x: format_obs(x, dim_codes, att_codes,  # noqa: E731
                                  measure_code, prettyprint)

    iterator = map(parser, data.to_dict(orient='records'))
    out = ''.join(iterator)

    return out


def format_ser(data: dict,
               measure_code: str,
               series_key: list,
               series_attr: list,
               obs_attr: list,
               dim: str,
               prettyprint=True):
    if prettyprint:
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = nl = ''

    out = f"{child2}<{genericAbbr}:Series>{nl}"
    # --------------  Series --------------
    # Series Keys

    out += f"{child3}<{genericAbbr}:SeriesKey>{nl}"

    for k in series_key:
        out += f'{child4}<{genericAbbr}:Value id="{k}" value="{data[k]}"/>{nl}'

    out += f"{child3}</{genericAbbr}:SeriesKey>{nl}"

    # Series Attributes

    if len(series_attr) > 0:
        out += f"{child3}<{genericAbbr}:Attributes>{nl}"

        for k in series_attr:
            if data[k] != '':
                out += f'{child4}<{genericAbbr}:Value id="{k}" ' \
                       f'value="{data[k]}"/>{nl}'

        out += f"{child3}</{genericAbbr}:Attributes>{nl}"

    # --------------  Obs  --------------

    for obs in data['Obs']:
        out += f"{child3}<{genericAbbr}:Obs>{nl}"
        # Obs Elements
        if dim in obs:
            out += f'{child4}<{genericAbbr}:ObsDimension ' \
                   f'value="{obs[dim]}"/>{nl}'

        out += format_measure_att(obs, measure_code, obs_attr,
                                  child3, child4, nl)

        out += f"{child3}</{genericAbbr}:Obs>{nl}"

    out += f"{child2}</{genericAbbr}:Series>{nl}"

    del data['Obs']

    return out


def ser_gen(data: pd.DataFrame,
            dim_codes: list,
            att_codes: list,
            measure_code: str,
            obs_codes: list,
            series_codes: list,
            prettyprint=True):
    # Getting each datapoint from data and creating dict

    series_key = [v for v in series_codes if v in dim_codes]
    series_att = [v for v in series_codes if v in att_codes]
    dim = obs_codes[0]
    if len(obs_codes) == 2:
        obs_att = []
    else:
        obs_att = obs_codes[2:]

    data = data.sort_values(series_codes, axis=0)

    data_dict = {'Series': data[series_codes].drop_duplicates().reset_index(
        drop=True).to_dict(orient="records")}

    parser = lambda x: format_ser(data=x,  # noqa: E731
                                  measure_code=measure_code,
                                  series_key=series_key,
                                  series_attr=series_att,
                                  obs_attr=obs_att,
                                  dim=dim,
                                  prettyprint=prettyprint)

    out = series_process(parser=parser, data=data, data_dict=data_dict,
                         series_codes=series_codes, obs_codes=obs_codes)

    del data_dict

    return out
