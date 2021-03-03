import os
import re as re_
import sys

from lxml import etree as etree_

from .mappings import ClassToNode

Tag_pattern_ = re_.compile(r'({.*})?(.*)')
CDATA_pattern_ = re_.compile(r'<!\[CDATA\[.*?]]>', re_.DOTALL)
BaseStrType_ = str

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ImportError:
    class GdsCollector(object):
        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print(f"Warning: {msg}")


def parse_xml(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    """Escape markup chars, but do not modify CDATA sections."""
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or str(inStr))
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = f"'{s1}'"
    else:
        s1 = f'"{s1}"'
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return f"'{s1}'"
        else:
            return f"'''{s1}'''"
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return f'"{s1}"'
        else:
            return f'"""{s1}"""'


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
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


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = f'{msg} (element {node.tag}/line {node.sourceline})'
    raise GDSParseError(msg)


def cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    root_class = ClassToNode.get(tag)
    if root_class is None:
        root_class = globals().get(tag)
    return tag, root_class


def get_required_ns_prefix_defs(rootNode):
    """Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    """
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }

    namespacedefs = ' '.join([f'xmlns:{prefix}="{uri}"' for prefix, uri in nsmap.items()])

    return nsmap, namespacedefs


def makeWarnings(print_warnings, gds_collector):
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write(f'----- Warnings -- count: {len(gds_collector.get_messages())} -----\n')
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
