from datetime import datetime
from io import StringIO

from sdmxthon.model.header import Header
from sdmxthon.parsers.message_parsers import Structures
from sdmxthon.parsers.write import genWriting, strWriting, strSerWriting
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.mappings import messageAbbr, commonAbbr, genericAbbr, \
    structureAbbr, structureSpecificAbbr
from sdmxthon.utils.parsing_words import HEADER

xmlns = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
         messageAbbr: 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message',
         commonAbbr: 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common',
         }
optional = {
    genericAbbr: "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    structureAbbr: "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    structureSpecificAbbr: "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific"
}


def addStructure(dataset, prettyprint, dType):
    outfile = ''

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


def create_namespaces(dataTypeString, payload, dType):
    namespaces = {}
    namespaces['xmlns'] = xmlns
    if dType == MessageTypeEnum.GenericDataSet:
        namespaces['xmlns'] = {**xmlns, **optional[genericAbbr]}
    elif dType == MessageTypeEnum.StructureDataSet:
        namespaces['xmlns'] = {**xmlns, **optional[structureSpecificAbbr]}
        """
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
        
        """
    else:
        namespaces['xmlns'] = {**xmlns, **optional[structureAbbr]}

    namespaces[
        'xsi:schemaLocation'] = 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd'

    return namespaces


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
    if dType == MessageTypeEnum.GenericDataSet:
        data_type_string = 'GenericData'
    elif dType == MessageTypeEnum.StructureDataSet:
        data_type_string = 'StructureSpecificData'
    else:
        data_type_string = 'Structure'

    out = {data_type_string: {}}
    outfile = ''
    # Header
    out[data_type_string] = create_namespaces(data_type_string, payload, dType)

    if header is None:
        out[HEADER] = {'ID': id_,
                       'Test': {test},
                       'Prepared': prepared.strftime("%Y-%m-%dT%H:%M:%S"),
                       'Sender': {'id': sender},
                       'Receiver': {'id': receiver},
                       'Structure': {'structureID': 'BIS_DER',
                                     'namespace': 'urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=BIS:BIS_DER(1.0)',
                                     'dimensionAtObservation': 'AllDimensions',
                                     'Structure': {'Ref': {'agencyID': 'BIS',
                                                           'id': 'BIS_DER',
                                                           'version': '1.0',
                                                           'class': 'DataStructure'}}}}
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
