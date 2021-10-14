from time import time

import pandas as pd

import sdmxthon
from sdmxthon.parsers.new_read import read_xml
from sdmxthon.utils.handlers import first_element_dict

file_str_all = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/str_all.xml").read()
file_str_ser = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/str_ser.xml").read()
file_gen_all = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/gen_all.xml").read()
file_gen_ser = open(
    "sdmxthon/testSuite/readingValidation/data/data_sample/gen_ser.xml").read()
file_data_df = open("sdmxthon/outputTests/BIS_DER_DATAFLOW.xml").read()
file_meta_bis = open("sdmxthon/outputTests/bis.xml").read()
file_meta_ecb = open("sdmxthon/testSuite/metadataFromDiferentSources/data"
                     "/data_sample/ecb.xml").read()
file_meta_estat = open("sdmxthon/testSuite/metadataFromDiferentSources/data"
                       "/data_sample/estat.xml").read()
file_meta_rbi = open("sdmxthon/outputTests/DSD_28APRIL21_updated.xml").read()
file_meta_df = open("sdmxthon/outputTests/metadata.xml").read()


def main():
    start = time()

    df1 = read_xml(file_str_all, validate=False)['BIS:BIS_DER(1.0)']
    df2 = read_xml(file_str_ser, validate=False)['BIS:BIS_DER(1.0)']
    df3 = read_xml(file_gen_all, validate=False)['BIS:BIS_DER(1.0)']
    df4 = read_xml(file_gen_ser, validate=False)['BIS:BIS_DER(1.0)']
    # read_xml(file_data_df, validate=False)['BIS:WEBSTATS_DER_DATAFLOW(1.0)']

    end = time()
    print(f'New data read: {end - start}')

    pd.testing.assert_frame_equal(df1.data.sort_index(axis=1),
                                  df2.data.sort_index(axis=1))
    pd.testing.assert_frame_equal(df2.data.sort_index(axis=1),
                                  df3.data.sort_index(axis=1))
    pd.testing.assert_frame_equal(df3.data.sort_index(axis=1),
                                  df4.data.sort_index(axis=1))

    start = time()
    sdmxthon.read_sdmx(file_str_all, validate=False)
    sdmxthon.read_sdmx(file_str_ser, validate=False)
    sdmxthon.read_sdmx(file_gen_all, validate=False)
    sdmxthon.read_sdmx(file_gen_ser, validate=False)
    sdmxthon.read_sdmx(file_data_df, validate=False)
    end = time()
    print(f'Old data read: {end - start}')

    start = time()
    metadata1 = read_xml(file_meta_bis, validate=False)
    metadata2 = read_xml(file_meta_estat, validate=False)
    metadata5 = read_xml(file_meta_df, validate=False)
    end = time()
    print(f'New metadata read: {end - start}')

    start = time()
    meta_old1 = sdmxthon.read_sdmx(file_meta_bis, validate=False)
    meta_old2 = sdmxthon.read_sdmx(file_meta_estat, validate=False)
    meta_old5 = sdmxthon.read_sdmx(file_meta_df, validate=False)
    end = time()
    print(f'Old metadata read: {end - start}')
    print('------------Metadata 1-----------------')
    print(first_element_dict(meta_old1.content['dsds']) == first_element_dict(
        metadata1['DataStructures']))
    print('------------Metadata 2-----------------')
    print(first_element_dict(meta_old2.content['dsds']) == first_element_dict(
        metadata2['DataStructures']))
    print('------------Metadata 5-----------------')
    print(first_element_dict(meta_old5.content['dsds']) == first_element_dict(
        metadata5['DataStructures']))

    pass


if __name__ == '__main__':
    main()
