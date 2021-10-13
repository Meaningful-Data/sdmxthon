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
file_data_df = open("sdmxthon/outputTests/BIS_DER_DATAFLOW.xml").read()
file_meta_bis = open("sdmxthon/outputTests/bis.xml").read()
file_meta_ecb = open("sdmxthon/testSuite/metadataFromDiferentSources/data"
                     "/data_sample/ecb.xml").read()
file_meta_estat = open("sdmxthon/testSuite/metadataFromDiferentSources/data"
                       "/data_sample/estat.xml").read()
file_meta_rbi = open("sdmxthon/outputTests/DSD_28APRIL21_updated.xml").read()
file_meta_df = open("sdmxthon/outputTests/metadata.xml").read()


def recursive_compare(d1, d2, level='root'):
    if isinstance(d1, dict) and isinstance(d2, dict):
        if d1.keys() != d2.keys():
            s1 = set(d1.keys())
            s2 = set(d2.keys())
            print('{:<20} + {} - {}'.format(level, s1 - s2, s2 - s1))
            common_keys = s1 & s2
        else:
            common_keys = set(d1.keys())

        for k in common_keys:
            recursive_compare(d1[k], d2[k], level='{}.{}'.format(level, k))

    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            print('{:<20} len1={}; len2={}'.format(level, len(d1), len(d2)))
        common_len = min(len(d1), len(d2))

        for i in range(common_len):
            recursive_compare(d1[i], d2[i], level='{}[{}]'.format(level, i))

    else:
        if d1 != d2:
            print('{:<20} {} != {}'.format(level, d1, d2))


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
    # metadata1 = read_xml(file_meta_bis, validate=False)
    # metadata2 = read_xml(file_meta_estat, validate=False)
    # metadata3 = read_xml(file_meta_rbi, validate=False)
    # metadata4 = read_xml(file_meta_ecb, validate=False)
    metadata5 = read_xml(file_meta_df, validate=False)
    end = time()
    print(f'New metadata read: {end - start}')

    start = time()
    # meta_old1 = sdmxthon.read_sdmx(file_meta_bis, validate=False)
    # meta_old2 = sdmxthon.read_sdmx(file_meta_estat, validate=False)
    # meta_old3 = sdmxthon.read_sdmx(file_meta_rbi, validate=False)
    # meta_old4 = sdmxthon.read_sdmx(file_meta_ecb, validate=False)
    meta_old5 = sdmxthon.read_sdmx(file_meta_df, validate=False)
    end = time()
    print(f'Old metadata read: {end - start}')
    recursive_compare(meta_old5.content['dsds']['BIS:BIS_DER(1.0)'],
                      metadata5['DataStructures']['BIS:BIS_DER(1.0)'])

    pass


if __name__ == '__main__':
    main()
