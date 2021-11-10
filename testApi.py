# flake8: noqa
import sqlite3
from time import time

file_str_all = "sdmxthon/testSuite/readingValidation/data/data_sample" \
               "/str_all.xml "
file_str_ser = "sdmxthon/testSuite/readingValidation/data/data_sample" \
               "/str_ser.xml "
file_gen_all = "sdmxthon/testSuite/readingValidation/data/data_sample" \
               "/gen_all.xml "
file_gen_ser = "sdmxthon/testSuite/readingValidation/data/data_sample" \
               "/gen_ser.xml "
file_data_df = "sdmxthon/outputTests/BIS_DER_DATAFLOW.xml"
file_meta_bis = "sdmxthon/outputTests/bis.xml"
file_meta_ecb = "sdmxthon/testSuite/metadataFromDiferentSources/data" \
                "/data_sample/ecb.xml "
file_meta_estat = "sdmxthon/testSuite/metadataFromDiferentSources/data" \
                  "/data_sample/estat.xml "
file_meta_rbi = "sdmxthon/outputTests/DSD_28APRIL21_updated.xml"
file_meta_df = "sdmxthon/outputTests/metadata.xml"
file_big_bis = "sdmxthon/outputTests/BIS_DER.xml"
file_huge_bis = "sdmxthon/outputTests/out.xml"
file_test_bis = "sdmxthon/outputTests/test_huge.xml"
db_path = "sdmxthon/outputTests/BIS_DER_OUTS.db"

url_bis = "https://stats.bis.org/api/v1/datastructure/BIS/BIS_LBS_DISS" \
          "/1.0?references=all"


def main():
    start = time()
    limit = 110000
    conn = sqlite3.connect(db_path)
    # dsd = read_sdmx(file_meta_rbi, validate=False)
    # print(dsd)
    # dataset = Dataset(structure=dsd, data=df)
    # end = time()
    # print(f"-------- Loaded {len(dataset.data)} in {end - start} ----------")
    # # dsd = first_element_dict(read_xml(url_bis, validate=False)
    # #                          ['DataStructures'])
    # # dataset = read_xml(file_huge_bis, False)['BIS:BIS_LBS_DISS(1.0)']
    # # conn = sqlite3.connect(db_path)
    # # dataset.structure = dsd
    # # dataset.data.to_sql("BIS_LBS_DISS", conn, index=False,
    # # if_exists='replace')
    # # end_2 = time()
    # # print(f"-------- Dump to database in {end_2 - end}")
    #
    # start = time()
    # dataset.to_xml(MessageTypeEnum.GenericDataSet, outputPath="test_1.xml")
    # step_1 = time()
    # dataset.to_xml(MessageTypeEnum.StructureDataSet, outputPath="test_2.xml")
    # step_2 = time()
    # dataset.set_dimension_at_observation("TIME_PERIOD")
    # dataset.to_xml(MessageTypeEnum.GenericDataSet, outputPath="test_3.xml")
    # step_3 = time()
    # dataset.to_xml(MessageTypeEnum.StructureDataSet, outputPath="test_4.xml")
    # end = time()
    # # test4 = read_sdmx("./test_4.xml", False).payload['BIS:BIS_DER(1.0)']
    # pd.testing.assert_frame_equal(dataset.data.astype(str).sort_index(axis=1),
    # #                               test4.data.sort_index(axis=1),
    # #                               check_dtype=False)
    # message = f"""
    # ------- Writing Time: ---------
    # Generic All: {step_1 - start}
    # Structure Specific All: {step_2 - step_1}
    # Generic Series : {step_3 - step_2}
    # Structure Specific Series: {end - step_3}
    # """
    # print(message)
    #
    # del df
    # del dsd
    # del dataset
    #
    # start = time()
    # test1 = first_element_dict(read_sdmx("./test_1.xml", False).payload)
    # step_1 = time()
    # test2 = first_element_dict(read_sdmx("./test_2.xml", False).payload)
    # step_2 = time()
    # test3 = first_element_dict(read_sdmx("./test_3.xml", False).payload)
    # step_3 = time()
    # test4 = first_element_dict(read_sdmx("./test_4.xml", False).payload)
    # end = time()
    #
    # message = f"""
    # ------- Reading Time: ---------
    # Generic All: {step_1 - start}
    # Structure Specific All: {step_2 - step_1}
    # Generic Series : {step_3 - step_2}
    # Structure Specific Series: {end - step_3}
    # """
    # print(message)
    #
    # pd.testing.assert_frame_equal(dataset.data.astype(str).sort_index(axis=1),
    #                               test4.data.sort_index(axis=1),
    #                               check_dtype=False)
    # pd.testing.assert_frame_equal(test1.data.sort_index(axis=1),
    #                               test2.data.sort_index(axis=1))
    # pd.testing.assert_frame_equal(test2.data.sort_index(axis=1),
    #                               test3.data.sort_index(axis=1))
    # pd.testing.assert_frame_equal(test3.data.sort_index(axis=1),
    #                               test4.data.sort_index(axis=1))

    #
    # print(f"Validation: {end - start}")

    # df1 = read_xml(file_str_all, validate=False)['BIS:BIS_DER(1.0)']
    # df2 = read_xml(file_str_ser, validate=False)['BIS:BIS_DER(1.0)']
    # df3 = read_xml(file_gen_all, validate=False)['BIS:BIS_DER(1.0)']
    # df4 = read_xml(file_gen_ser, validate=False)['BIS:BIS_DER(1.0)']
    # read_xml(file_data_df, validate=False)['BIS:WEBSTATS_DER_DATAFLOW(1.0)']
    #
    # end = time()
    # print(f'New data read: {end - start}')
    #
    # pd.testing.assert_frame_equal(df1.data.sort_index(axis=1),
    #                               df2.data.sort_index(axis=1))
    # pd.testing.assert_frame_equal(df2.data.sort_index(axis=1),
    #                               df3.data.sort_index(axis=1))
    # pd.testing.assert_frame_equal(df3.data.sort_index(axis=1),
    #                               df4.data.sort_index(axis=1))
    #
    # start = time()
    # sdmxthon.read_sdmx(file_str_all, validate=False)
    # sdmxthon.read_sdmx(file_str_ser, validate=False)
    # sdmxthon.read_sdmx(file_gen_all, validate=False)
    # sdmxthon.read_sdmx(file_gen_ser, validate=False)
    # sdmxthon.read_sdmx(file_data_df, validate=False)
    # end = time()
    # print(f'Old data read: {end - start}')


if __name__ == '__main__':
    main()
