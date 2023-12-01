from datetime import datetime

from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.mappings import (messageAbbr, genericAbbr,
                                     structureSpecificAbbr, structureAbbr,
                                     commonAbbr)
from sdmxthon.utils.parsing_words import (ORGS, DATAFLOWS, CODELISTS,
                                          CONCEPTS, DSDS, CONSTRAINTS)

MESSAGE_TYPE_MAPPING = {
    MessageTypeEnum.GenericDataSet: 'GenericData',
    MessageTypeEnum.StructureSpecificDataSet: 'StructureSpecificData',
    MessageTypeEnum.Metadata: 'Structure'
}


def create_namespaces(type_: MessageTypeEnum, payload,
                      prettyprint: bool = False):
    """
    Creates the namespaces for the XML file

    :param type_: Internal message type
    :type type_: MessageTypeEnum

    :param payload: Datasets or None

    :param prettyprint: Prettyprint or not
    :type prettyprint: bool

    :return: String for output file
    """
    if prettyprint:
        nl = '\n'
    else:
        nl = ''
    outfile = f'<?xml version="1.0" encoding="UTF-8"?>{nl}'
    outfile += f'<{messageAbbr}:{MESSAGE_TYPE_MAPPING[type_]} ' \
               f'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
               f'xmlns:{messageAbbr}="http://www.sdmx.org/resources/sdmxml' \
               f'/schemas/v2_1/message" '
    if type_ == MessageTypeEnum.GenericDataSet:
        outfile += f'xmlns:{genericAbbr}="http://www.sdmx.org/resources' \
                   f'/sdmxml/schemas/v2_1/data/generic" '
    elif type_ == MessageTypeEnum.StructureSpecificDataSet:
        outfile += f'xmlns:{structureSpecificAbbr}="http://www.sdmx.org' \
                   f'/resources/sdmxml/schemas/v2_1/data/structurespecific" '
        if payload is None:
            raise Exception('Must provide a dataset to write')
        if isinstance(payload, dict):
            count = 0
            for key, record in payload.items():
                count += 1
                if record.structure is None:
                    raise Exception(f'Dataset {key} has no structure defined')
                outfile += f'xmlns:ns{count}="urn:sdmx:org.sdmx.infomodel' \
                           f'.datastructure.DataStructure=' \
                           f'{record.unique_id}' \
                           f':ObsLevelDim:{record.dim_at_obs}" '
        else:
            if payload.structure is None:
                raise Exception('Dataset has no structure defined')
            outfile += f'xmlns:ns1="urn:sdmx:org.sdmx.infomodel' \
                       f'.datastructure.DataStructure={payload.unique_id}' \
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


def write_from_header(header, prettyprint, type_, payload=None):
    """
    Writes the header to the XML file

    :param header: Header to be written
    :param prettyprint: Prettyprint or not
    :param type_: Message type
    :param payload: Payload to get the structure on StructureSpecificData

    :return: String for output file
    """
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
    if isinstance(payload, dict) and type_ is not MessageTypeEnum.Metadata:
        for record in payload.values():
            outfile += addStructure(record, prettyprint, type_)
    elif type_ is not MessageTypeEnum.Metadata:
        outfile += addStructure(payload, prettyprint, type_)

    if type_ is not MessageTypeEnum.Metadata and header is not None:
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
    return outfile


def _write_metadata_element(payload, dict_word, pkg_word,
                            item_word, newline, indent):
    outfile = ""
    if dict_word in payload:
        indent_child = newline + add_indent(indent)
        outfile += f'{indent_child}<{structureAbbr}:{pkg_word}>'
        for e in payload[dict_word].values():
            outfile += e._parse_XML(indent_child,
                                    f'{structureAbbr}:{item_word}')
        outfile += f'{indent_child}</{structureAbbr}:{pkg_word}>'

    return outfile


def parse_metadata(payload, prettyprint):
    if prettyprint:
        indent = '\t'
        newline = '\n'
    else:
        indent = newline = ''

    outfile = f'{indent}<{messageAbbr}:Structures>'
    outfile += _write_metadata_element(payload, ORGS, 'OrganisationSchemes',
                                       'AgencyScheme', newline, indent)
    outfile += _write_metadata_element(payload, DATAFLOWS, 'Dataflows',
                                       'Dataflow', newline, indent)
    outfile += _write_metadata_element(payload, CODELISTS, 'Codelists',
                                       'Codelist', newline, indent)
    outfile += _write_metadata_element(payload, CONCEPTS, 'Concepts',
                                       'ConceptScheme', newline, indent)
    outfile += _write_metadata_element(payload, DSDS, 'DataStructures',
                                       'DataStructure', newline, indent)
    outfile += _write_metadata_element(payload, CONSTRAINTS, 'Constraints',
                                       'ContentConstraint', newline, indent)

    outfile += f'{newline}{indent}</{messageAbbr}:Structures>{newline}'

    return outfile


def addStructure(dataset, prettyprint, type_):
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
    if type_ != MessageTypeEnum.GenericDataSet:
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


def get_outfile(obj_: dict, key='', indent=''):
    element = obj_.get(key) or []

    outfile = ''

    for i in element:
        outfile += indent + i

    return outfile


def export_intern_data(data: dict, indent: str):
    outfile = get_outfile(data, 'Annotations', indent)
    outfile += get_outfile(data, 'Name', indent)
    outfile += get_outfile(data, 'Description', indent)

    return outfile


def add_indent(indent: str):
    if indent == '':
        return ''
    else:
        indent += '\t'
        return indent


def get_end_message(type_):
    return f'</{messageAbbr}:{MESSAGE_TYPE_MAPPING[type_]}>'
