# flake8: noqa
from time import time

from sdmxthon.model.dataset import Dataset
from sdmxthon.parsers.new_read import read_xml
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict

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


def main():
    start = time()

    dataset: Dataset = read_xml(file_str_all, validate=False)[
        'BIS:BIS_DER(1.0)']
    dsd = first_element_dict(read_xml(file_meta_bis, validate=False)
                             ['DataStructures'])
    dataset.structure = dsd

    print(dataset.semantic_validation())
    dataset.set_dimension_at_observation("TIME_PERIOD")
    dataset.to_xml(MessageTypeEnum.StructureDataSet)

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
    #
    # start = time()
    # metadata1 = read_xml(file_meta_bis, validate=False)
    # metadata2 = read_xml(file_meta_estat, validate=False)
    # metadata5 = read_xml(file_meta_df, validate=False)
    # end = time()
    # print(f'New metadata read: {end - start}')
    #
    # start = time()
    # meta_old1 = sdmxthon.read_sdmx(file_meta_bis, validate=False)
    # meta_old2 = sdmxthon.read_sdmx(file_meta_estat, validate=False)
    # meta_old5 = sdmxthon.read_sdmx(file_meta_df, validate=False)
    # end = time()
    # print(f'Old metadata read: {end - start}')


if __name__ == '__main__':
    main()
