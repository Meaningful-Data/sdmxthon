from datetime import datetime
from io import StringIO

import pandas as pd

from sdmxthon.model.component import PrimaryMeasure
from sdmxthon.model.header import Header
from sdmxthon.parsers.data_validations import get_mandatory_attributes
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import add_indent
from sdmxthon.utils.mappings import messageAbbr, commonAbbr, genericAbbr, \
    structureSpecificAbbr, structureAbbr
from sdmxthon.utils.parsing_words import ORGS, DATAFLOWS, CODELISTS, \
    CONCEPTS, DSDS, CONSTRAINTS

chunksize = 100000

"""
     --------------------------------------------
    |                                            |
    |                   Common                   |
    |                                            |
     --------------------------------------------
"""

"""
     --------------------------------------------
    |                                            |
    |                   Common                   |
    |                                            |
     --------------------------------------------
"""


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


def process_dataset(dataset):
    dataset.data = dataset.data.fillna(value='')
    return dataset


def parse_metadata(payload, prettyprint):
    if prettyprint:
        indent = '\t'
        newline = '\n'
    else:
        indent = newline = ''

    outfile = f'{indent}<{messageAbbr}:Structures>'
    if ORGS in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:OrganisationSchemes>'
        for e in payload[ORGS].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:AgencyScheme')
        outfile += f'{indent_child}</{structureAbbr}:OrganisationSchemes>'

    if DATAFLOWS in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:Dataflows>'
        for e in payload[DATAFLOWS].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:Dataflow')
        outfile += f'{indent_child}</{structureAbbr}:Dataflows>'

    if CODELISTS in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:Codelists>'
        for e in payload[CODELISTS].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:Codelist')
        outfile += f'{indent_child}</{structureAbbr}:Codelists>'

    if CONCEPTS in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:Concepts>'
        for e in payload[CONCEPTS].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:ConceptScheme')
        outfile += f'{indent_child}</{structureAbbr}:Concepts>'

    if DSDS in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:DataStructures>'
        for e in payload[DSDS].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:DataStructure')
        outfile += f'{indent_child}</{structureAbbr}:DataStructures>'

    if CONSTRAINTS in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:Constraints>'
        for e in payload[CONSTRAINTS].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:ContentConstraint')
        outfile += f'{indent_child}</{structureAbbr}:Constraints>'

    outfile += f'{newline}{indent}</{messageAbbr}:Structures>{newline}'

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
                record = process_dataset(record)
                outfile += genWriting(record, prettyprint, record.dim_at_obs)
        else:
            payload = process_dataset(payload)
            outfile += genWriting(payload, prettyprint, dim=payload.dim_at_obs)
    elif dType == MessageTypeEnum.StructureDataSet:
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
    elif dType == MessageTypeEnum.Metadata:
        if len(payload) > 0:
            outfile += parse_metadata(payload, prettyprint)
    outfile += f'</{messageAbbr}:{data_type_string}>'

    if path != '':
        with open(path, "w", encoding="UTF-8", errors='replace') as f:
            f.write(outfile)
    else:
        f = StringIO()
        f.write(outfile)
        return f

def format_dict_ser(out, parser, data_dict, obs):
    data_dict['Series'][0]['Obs'] = obs.to_dict(orient="records")
    out.append(parser(data_dict['Series'][0]))
    del data_dict['Series'][0]


def series_process(parser, data, data_dict, series_codes, obs_codes):
    out = []
    data.groupby(by=series_codes)[obs_codes].apply(
        lambda x: format_dict_ser(out, parser, data_dict, x))

    return ''.join(out)


"""
     --------------------------------------------
    |                                            |
    |              Structure Specific            |
    |                                            |
     --------------------------------------------
"""


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
        chunksize = 100000
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


"""
     --------------------------------------------
    |                                            |
    |                   Generic                  |
    |                                            |
     --------------------------------------------
"""


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
        chunksize = 100000
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

        outfile += ser_gen(dataset.data,
                           dim_codes=dim_codes,
                           att_codes=att_codes,
                           measure_code=measure_code,
                           prettyprint=prettyprint,
                           series_codes=series_codes,
                           obs_codes=obs_codes)

    outfile += f'{child1}</{messageAbbr}:DataSet>{nl}'

    return outfile


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
        child5 = '\t\t\t\t\t'
        nl = '\n'
    else:
        child2 = child3 = child4 = child5 = nl = ''

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

        if measure_code != "OBS_VALUE":
            out += f'{child4}<{genericAbbr}:ObsValue id="{measure_code}" ' \
                   f'value="{obs[measure_code]}"/>{nl}'
        else:
            out += f'{child4}<{genericAbbr}:ObsValue ' \
                   f'value="{obs[measure_code]}"/>{nl}'

        # Obs Attributes
        if len(obs_attr) > 0:
            out += f"{child4}<{genericAbbr}:Attributes>{nl}"

            for k in obs_attr:
                if obs[k] != '':
                    out += f'{child5}<{genericAbbr}:Value id="{k}" ' \
                           f'value="{obs[k]}"/>{nl}'

            out += f"{child4}</{genericAbbr}:Attributes>{nl}"

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
