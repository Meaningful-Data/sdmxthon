import logging

# create logger
from SDMXThon import DatasetType, readSDMX

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
# formatter = logging.Formatter("%(message)s")
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

pathDSDS = 'SDMXThon/outputTests/metadata/dsds.pickle'
pathTest = 'SDMXThon/outputTests/test_GEN.xml'
pathToDataFile = 'SDMXThon/outputTests/BIS_DER_test.xml'
pathSaveToGeneric = 'SDMXThon/outputTests/outputGen.xml'
pathSaveToStructure = 'SDMXThon/outputTests/outputSpe.xml'
pathSaveToTimeGen = 'SDMXThon/outputTests/outputTimeGen.xml'
pathSaveToTimeXS = 'SDMXThon/outputTests/outputTimeXS.xml'
pathToJSON = 'SDMXThon/outputTests/output.json'
pathToCSV = 'SDMXThon/outputTests/csv.zip'
pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/BIS_BIS_DER.xml'


def main():
    message = readSDMX(pathToDataFile, pathToMetadataFile, dataset_type=DatasetType.StructureDataSet)

    # datasets = getDatasets(pathToDataFile, pathToMetadataFile, dataset_type=DatasetType.StructureDataSet)
    # message = Message(DatasetType.GenericDataSet, datasets)

    # xmlToJSON(pathSaveToGeneric, pathToMetadataFile, pathToJSON, dataset_type=DatasetType.GenericDataSet)

    # xmlToCSV(pathSaveToGeneric, pathToMetadataFile, pathToCSV, dataset_type=DatasetType.GenericDataSet)


"""
gui = show(dataset_list)

dataframes = gui.get_dataframes()

for e in dataset_list:
    e.obs = dataframes[e.code]
"""

if __name__ == '__main__':
    main()
