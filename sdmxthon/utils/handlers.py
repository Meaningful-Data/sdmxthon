"""
    Handlers file provide functions to make the code more readable
"""
import pandas as pd


def first_element_dict(obj_: dict):
    if len(obj_) != 0:
        values_view = obj_.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        return first_value
    else:
        return None


def split_unique_id(obj_: str):
    data = obj_.split(':', 1)
    agencyID = data[0]
    data = data[1].split('(', 1)
    id = data[0]
    version = data[1].split(')', 1)[0]

    return agencyID, id, version


def split_from_urn(obj_: str, split_id=True):
    full_id = obj_.split("=", 1)[1]
    if split_id:
        return split_unique_id(full_id)
    return full_id


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


def recursive_compare(d1, d2, level='root'):
    control = True
    if isinstance(d1, dict) and isinstance(d2, dict):
        if d1.keys() != d2.keys():
            control = False
            s1 = set(d1.keys())
            s2 = set(d2.keys())
            print('{:<20} + {} - {}'.format(level, s1 - s2, s2 - s1))
            common_keys = s1 & s2
        else:
            common_keys = set(d1.keys())

        for k in common_keys:
            control = recursive_compare(d1[k], d2[k],
                                        level='{}.{}'.format(level, k))

    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            control = False
            print('{:<20} len1={}; len2={}'.format(level, len(d1), len(d2)))
        common_len = min(len(d1), len(d2))
        if common_len != 0 and isinstance(d1[0], str):
            d1 = sorted(d1)
            d2 = sorted(d2)

        for i in range(common_len):
            control = recursive_compare(d1[i], d2[i],
                                        level='{}[{}]'.format(level, i))

    else:
        if d1 != d2:
            control = False
            print('{:<20} {} != {}'.format(level, d1, d2))

    return control


def drop_na_all(df: pd.DataFrame):
    return df.dropna(axis=1, how="all")
