"""
Dataflows writing Tests
"""
import os
import unittest

from SDMXThon.testSuite import TestHelper


class DataflowWriting(TestHelper.TestHelper):
    path = os.path.dirname(__file__)
    pathToDB = os.path.join(os.path.join(path, "data"), "data_sample")
    pathToReference = os.path.join(os.path.join(path, "data"), "reference")

    def test_1(self):
        data = 'bis_dataflow.xml'
        reference = 'bis_webstats_der.txt'
        dataflow_name = 'BIS:WEBSTATS_DER_DATAFLOW(1.0)'

        self.metadata_dataflow_writing(reference, data, dataflow_name)

    def test_2(self):
        data = 'bis_dataflow.xml'
        reference = 'bis_webstats_lbs.txt'
        dataflow_name = 'BIS:WEBSTATS_LBS_D_PUB_DATAFLOW(1.0)'

        self.metadata_dataflow_writing(reference, data, dataflow_name)

    def test_3(self):
        data = 'bis_dataflow.xml'
        reference = 'bis_webstats_xru.txt'
        dataflow_name = 'BIS:WEBSTATS_XRU_CURRENT_D_DATAFLOW(1.0)'

        self.metadata_dataflow_writing(reference, data, dataflow_name)


if __name__ == '__main__':
    unittest.main(verbosity=1)
