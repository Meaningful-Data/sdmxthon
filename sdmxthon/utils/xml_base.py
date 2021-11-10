import io
import os
from io import BytesIO

import requests
import validators
from lxml import etree
from lxml.etree import DocumentInvalid

pathToSchema = 'schemas/SDMXMessage.xsd'

def process_string_to_read(infile: str):
    if isinstance(infile, str):
        if validators.url(infile):
            try:
                response = requests.get(infile)
                if response.status_code == 400:
                    raise requests.ConnectionError(
                        f'Invalid URL. Response from server: {response.text}')
                infile = io.TextIOWrapper(BytesIO(response.content),
                                          encoding='UTF-8',
                                          errors="replace").read()
            except requests.ConnectionError:
                raise requests.ConnectionError('Invalid URL. '
                                               'No response from server')
        elif '/' in infile or '\\' in infile:
            try:
                infile = os.path.join(infile)
                with open(infile, "r", errors='replace',
                          encoding="UTF-8") as f:
                    infile = f.read()
            except AttributeError:
                pass
        else:
            raise ValueError(f'Unable to parse {infile}')
    elif isinstance(infile, os.PathLike):
        try:
            infile = os.path.join(infile)
            with open(infile, "r", errors='replace',
                      encoding="UTF-8") as f:
                infile = f.read()
        except AttributeError:
            pass
    elif isinstance(infile, BytesIO):
        infile = io.TextIOWrapper(infile,
                                  encoding='UTF-8',
                                  errors="replace").read()

    if infile[0] != '<' and infile[3] == '<':
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
