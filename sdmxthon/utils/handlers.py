"""
    Handlers file provide functions to make the code more readable
"""


def first_element_dict(obj_: dict):
    values_view = obj_.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)
    return first_value


def split_unique_id(obj_: str):
    data = obj_.split(':', 1)
    agencyID = data[0]
    data = data[1].split('(', 1)
    id = data[0]
    version = data[1].split(')', 1)[0]

    return agencyID, id, version


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


def add_list(element: any):
    if not isinstance(element, list):
        element = [element]
    return element


def unique_id(agencyID, id_, version):
    return f"{agencyID}:{id_}({version})"
