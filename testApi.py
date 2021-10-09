from time import time

import pandas as pd

import sdmxthon
from sdmxthon.parsers.new_read import read_xml

file_str_all = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/str_all.xml").read()
file_str_ser = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/str_ser.xml").read()
file_gen_all = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/gen_all.xml").read()
file_gen_ser = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/gen_ser.xml").read()
file_meta = open("sdmxthon/outputTests/bis.xml").read()


def main():
    start = time()

    df1 = read_xml(file_str_all, validate=False)['BIS:BIS_DER(1.0)']
    df2 = read_xml(file_str_ser, validate=False)['BIS:BIS_DER(1.0)']
    df3 = read_xml(file_gen_all, validate=False)['BIS:BIS_DER(1.0)']
    df4 = read_xml(file_gen_ser, validate=False)['BIS:BIS_DER(1.0)']

    end = time()
    print(f'New data read: {end - start}')
    print(pd.testing.assert_frame_equal(df1.data.sort_index(axis=1),
                                        df2.data.sort_index(axis=1)))
    print(pd.testing.assert_frame_equal(df3.data.sort_index(axis=1),
                                        df4.data.sort_index(axis=1)))

    start = time()
    sdmxthon.read_sdmx(file_str_all, validate=False)
    sdmxthon.read_sdmx(file_str_ser, validate=False)
    sdmxthon.read_sdmx(file_gen_all, validate=False)
    sdmxthon.read_sdmx(file_gen_ser, validate=False)
    end = time()
    print(f'Old data read: {end - start}')

    start = time()
    metadata = sdmxthon.read_sdmx(file_meta, validate=False)
    end = time()
    print(f'Old metadata read: {end - start}')
    start = time()
    metadata = read_xml(file_meta, validate=False)
    end = time()
    print(f'New metadata read: {end - start}')


if __name__ == '__main__':
    main()
