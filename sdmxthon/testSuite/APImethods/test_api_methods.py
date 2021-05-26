"""
API methods Tests
"""
import os
import unittest

from sdmxthon.testSuite import TestHelper


class APImethods(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'gen_all.xml'

        self.read_sdmx_data(data)

    def test_2(self):
        data = 'str_all.xml'

        self.read_sdmx_data(data)

    def test_3(self):
        data = 'gen_ser.xml'

        self.read_sdmx_data(data)

    def test_4(self):
        data = 'str_ser.xml'

        self.read_sdmx_data(data)

    def test_5(self):
        data = 'gen_all.xml'

        self.get_pandas_df_data(data)

    def test_6(self):
        data = 'str_all.xml'

        self.get_pandas_df_data(data)

    def test_7(self):
        data = 'gen_ser.xml'

        self.get_pandas_df_data(data)

    def test_8(self):
        data = 'str_ser.xml'

        self.get_pandas_df_data(data)

    def test_9(self):
        data = 'gen_all.xml'

        self.xml_to_csv_data(data)

    def test_10(self):
        data = 'str_all.xml'

        self.xml_to_csv_data(data)

    def test_11(self):
        data = 'gen_ser.xml'

        self.xml_to_csv_data(data)

    def test_12(self):
        data = 'str_ser.xml'

        self.xml_to_csv_data(data)


if __name__ == '__main__':
    unittest.main(verbosity=1)
