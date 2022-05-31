# flake8: noqa
from time import time

import lxml.etree as ET
import pandas as pd


def item_str(element):
    return dict(element.attrib)


def mem_eff_parser(result):
    test_data = []
    data = pd.DataFrame()
    for event, element in result:
        if 'Obs' == element.tag:
            test_data.append(item_str(element))
            if len(test_data) > 500000:
                data = pd.concat([data, pd.DataFrame(test_data)], copy=False, ignore_index=True)
                test_data.clear()
        elif 'DataSet' in element.tag:
            print(element)
        elif 'Structure' in element.tag:
            print(list(list(element)[0])[0].attrib)
        element.clear()

    data = pd.concat([data, pd.DataFrame(test_data)], copy=False, ignore_index=True)
    test_data.clear()
    return data


def main():
    start = time()
    result = ET.iterparse("test_2.xml", events=("start",), tag=('Obs', '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet',
                                                                '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}Structure'))
    data = mem_eff_parser(result)
    # data.to_csv("test.csv", index=False)
    # data = pd.read_csv("test.csv", chunksize=10000)
    # for element in data:
    #     print(element)
    # print(data)
    end = time()
    print(f"New: {end - start}")

    start = time()
    # read_sdmx("./test_2.xml")
    end = time()
    print(f"Old: {end - start}")


if __name__ == '__main__':
    main()
