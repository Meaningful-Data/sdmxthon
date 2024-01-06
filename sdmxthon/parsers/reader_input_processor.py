import csv
import json
import os
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path

import requests
import validators
from lxml import etree

from sdmxthon.utils.xml_allowed_errors import ALLOWED_ERRORS_CONTENT

path_to_schema = 'schemas/SDMXMessage.xsd'


def URLparsing(infile: str):
    try:
        response = requests.get(infile)
        if response.status_code == 400:
            raise requests.ConnectionError(
                f'Invalid URL. Response from server: {response.text}')
        infile = TextIOWrapper(BytesIO(response.content),
                               encoding='utf-8',
                               errors="replace").read()
    except requests.ConnectionError:
        raise requests.ConnectionError('Invalid URL. '
                                       'No response from server')
    return infile


def process_string_to_read(infile: str):
    if isinstance(infile, Path):
        infile = str(infile)
    if isinstance(infile, (str, os.PathLike)):
        # Is URL
        if validators.url(infile):
            infile = URLparsing(infile)
        # Is file as string
        elif len(infile) > 10 and "<?" in infile[:10] and "xml" in infile[:10]:
            pass
        elif len(infile) > 10 and ("{" in infile[:10] or "[" in infile[:10]):
            # Assuming it's JSON if it starts with '{' or '['
            try:
                result = json.loads(infile)
                return result, "json"
            except json.JSONDecodeError:
                pass

        # Is file as path
        elif ((".json" in infile and "{" not in infile[:10]) or
              (".json" in infile and "[" in infile[:10]) or
              (".csv" in infile and "," not in infile[:10]) or
              isinstance(infile, os.PathLike)):
            if not os.path.isfile(infile):
                raise ValueError(f"File not found: {infile}")
            # Check if it's a valid JSON file
            try:
                with open(infile, "r", encoding='utf-8', errors='replace') as f:
                    result = json.load(f)
                return result, "json"
            except (json.JSONDecodeError, AttributeError):
                pass
            # Check if it's a valid CSV file
            try:
                with open(infile, "r", encoding='utf-8', errors='replace') as f:
                    csv.reader(f)
                return infile, "csv"
            except csv.Error:
                pass
        # Is file as path
        elif ((".xml" in infile and "<" not in infile) or
              isinstance(infile, os.PathLike)):
            if not os.path.isfile(infile):
                raise ValueError(f"File not found: {infile}")
            try:
                with open(infile, "r",
                          encoding='utf-8',
                          errors='replace') as f:
                    infile = f.read()
                    return infile, "xml"
            except AttributeError:
                pass
        elif "DATAFLOW," in infile[:11] or ("STRUCTURE," in infile[:11] and
                                            "STRUCTURE_ID" in infile[:25]):
            return StringIO(infile), "csv"
        else:
            error_msg = f'Cannot parse string as SDMX. ' \
                        f'Found {infile}'
            raise ValueError(error_msg)
    # Is bytes
    elif isinstance(infile, BytesIO):
        infile = TextIOWrapper(infile,
                               encoding='utf-8',
                               errors="replace").read()

    else:
        error_msg = f'Cannot parse as SDMX, ' \
                    f'please use String or Path to file. ' \
                    f'Found {infile}'
        raise ValueError(error_msg)

    if infile[0] != '<' and infile[3] == '<':  # BOM parsing
        infile = infile[3:]

    return infile, "xml"


def validate_doc(infile):
    """
    Validates the XML file against the XSD schema

    :param infile: String or Path to file
    :exception: Exception if the XML file is not valid
    """
    try:
        parser = etree.ETCompatXMLParser()
    except AttributeError:
        # fallback to xml.etree
        parser = etree.XMLParser(remove_blank_text=True)

    base_path = os.path.dirname(os.path.dirname(__file__))
    schema = os.path.join(base_path, path_to_schema)
    xmlschema_doc = etree.parse(schema)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    if isinstance(infile, str):
        infile = BytesIO(bytes(infile, "UTF_8"))

    doc = etree.parse(infile, parser=parser)
    if not xmlschema.validate(doc):
        log_errors = list(xmlschema.error_log)
        unhandled_errors = []
        for e in log_errors:
            unhandled_errors.append(e.message)
        severe_errors = unhandled_errors.copy()
        for e in unhandled_errors:
            for allowed_error in ALLOWED_ERRORS_CONTENT:
                if allowed_error in e:
                    severe_errors.remove(e)

        if len(severe_errors) > 0:
            raise Exception(';\n'.join(severe_errors))
