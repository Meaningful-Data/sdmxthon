import os
import re as re_
import sys
from io import BytesIO

import requests
import validators
from lxml import etree as etree_, etree
from lxml.etree import DocumentInvalid

Tag_pattern_ = re_.compile(r'({.*})?(.*)')
CDATA_pattern_ = re_.compile(r'<!\[CDATA\[.*?]]>', re_.DOTALL)
BaseStrType_ = str

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#

pathToSchema = 'schemas/SDMXMessage.xsd'


def parse_xml(infile, parser=None):
    if isinstance(infile, str):
        if validators.url(infile):
            try:
                response = requests.get(infile)
                if response.status_code == 400:
                    raise requests.ConnectionError(
                        f'Invalid URL. Response from server: {response.text}')
                infile = BytesIO(response.content)
            except requests.ConnectionError:
                raise requests.ConnectionError('Invalid URL. '
                                               'No response from server')
        elif infile[0] == '<':
            infile = BytesIO(bytes(infile, 'utf-8'))
        elif '/' in infile or '\\' in infile:
            try:
                infile = os.path.join(infile)
            except AttributeError:
                infile = BytesIO(bytes(infile, 'utf-8'))
        else:
            raise ValueError(f'Unable to parse {infile}')
    else:
        if isinstance(infile, os.PathLike):
            try:
                infile = os.path.join(infile)
            except AttributeError:
                pass

    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    doc = etree_.parse(infile, parser=parser)
    return doc


def validate_doc(doc):
    base_path = os.path.dirname(os.path.dirname(__file__))
    schema = os.path.join(base_path, pathToSchema)
    xmlschema_doc = etree.parse(schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    if not xmlschema.validate(doc):
        try:
            xmlschema.assertValid(doc)
        except DocumentInvalid as e:
            if len(e.args) == 1 and \
                    'xsi:type' in e.args[0] or \
                    'abstract' in e.args[0]:
                pass
            else:
                raise e


def find_attr_value_(attr_name, node):
    if isinstance(node, dict):
        if attr_name in node.keys():
            value = node[attr_name]
            del node[attr_name]
            return value
        else:
            return None

    attrs = node.attrib
    if '}' in attr_name:
        attr_parts = attr_name.split('}')
        attr_parts[0] += '}'
    else:
        attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == '{http://www.w3.org/XML/1998/namespace}':
            value = attrs.get(f'{prefix}{name}')
        else:
            namespace = node.nsmap.get(prefix)
            if namespace is not None:
                value = attrs.get(f'{prefix}:{name}')
    return value


def encode_str_2_3(instr):
    return instr


def raise_parse_error(node, msg):
    if node is not None:
        msg = f'{msg} (element {node.tag}/line {node.sourceline})'
    raise GDSParseError(msg)


def cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)


def make_warnings(print_warnings, gds_collector):
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write(
            f'----- Warnings -- count: {len(gds_collector.get_messages())} '
            f'-----\n')
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)


class GDSParseError(Exception):
    pass
