import io
import os
from io import BytesIO

import requests
import validators
from lxml import etree
from lxml.etree import DocumentInvalid

pathToSchema = 'schemas/SDMXMessage.xsd'


def URLparsing(infile: str):
    try:
        response = requests.get(infile)
        if response.status_code == 400:
            raise requests.ConnectionError(
                f'Invalid URL. Response from server: {response.text}')
        infile = io.TextIOWrapper(BytesIO(response.content),
                                  encoding='utf-8',
                                  errors="replace").read()
    except requests.ConnectionError:
        raise requests.ConnectionError('Invalid URL. '
                                       'No response from server')
    return infile


def process_string_to_read(infile: str):
    if isinstance(infile, (str, os.PathLike)):
        # Is URL
        if validators.url(infile):
            infile = URLparsing(infile)
        # Is file as string
        elif len(infile) > 10 and "<?" in infile[:10] and "xml" in infile[:10]:
            pass
        # Is file as path
        elif ('/' in infile or '\\' in infile or
              (".xml" in infile and "<" not in infile) or
              isinstance(infile, os.PathLike)):
            if not os.path.isfile(infile):
                raise ValueError(f"File not found: {infile}")
            try:
                with open(infile, "r",
                          encoding='utf-8',
                          errors='replace') as f:
                    infile = f.read()
            except AttributeError:
                pass
        else:
            error_msg = f'Cannot parse string as SDMX. ' \
                        f'Found {infile}'
            raise ValueError(error_msg)
    # Is bytes
    elif isinstance(infile, BytesIO):
        infile = io.TextIOWrapper(infile,
                                  encoding='utf-8',
                                  errors="replace").read()

    else:
        error_msg = f'Cannot parse as SDMX, ' \
                    f'please use String or Path to file. ' \
                    f'Found {infile}'
        raise ValueError(error_msg)

    if infile[0] != '<' and infile[3] == '<':  # BOM parsing
        infile = infile[3:]

    return infile


def validate_doc(infile):
    # Use the lxml ElementTree compatible parser so that, e.g.,
    #   we ignore comments.
    try:
        parser = etree.ETCompatXMLParser()
    except AttributeError:
        # fallback to xml.etree
        parser = etree.XMLParser()

    base_path = os.path.dirname(os.path.dirname(__file__))
    schema = os.path.join(base_path, pathToSchema)
    xmlschema_doc = etree.parse(schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    if isinstance(infile, str):
        infile = BytesIO(bytes(infile, "UTF_8"))

    doc = etree.parse(infile, parser=parser)

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


def cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)
