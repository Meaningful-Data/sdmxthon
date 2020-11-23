from lxml import etree

from SDMXThon.utils.parsers import get_codelist, get_attr_enums, is_enum, is_valid_enum_value


def validate_enum():
    path_to_metadata = 'ecu/IRIS/RBI_DSD(1.0)_20052020.xml'
    root = etree.parse(path_to_metadata)
    codelists = get_codelist(root)
    attr_enums = get_attr_enums(root, 'AALOE')
    enum_name = is_enum('Measure_Type', attr_enums)
    value = is_valid_enum_value(enum_name, 'HOLA_MUNDO', codelists)
    print(value)


def main():
    validate_enum()


if __name__ == '__main__':
    main()
