import logging
import sys

from SDMXThon import DatasetType, getDatasets

# create logger

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
pathToDataFile = 'SDMXThon/outputTests/BIS_DER.xml'
pathSaveToGeneric = 'SDMXThon/outputTests/outputGen.xml'
pathSaveToStructure = 'SDMXThon/outputTests/outputSpe.xml'
pathSaveToTimeGen = 'SDMXThon/outputTests/outputTimeGen.xml'
pathSaveToTimeXS = 'SDMXThon/outputTests/outputTimeXS.xml'
pathToJSON = 'SDMXThon/outputTests/output.json'
pathToCSV = 'SDMXThon/outputTests/csv.zip'
pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/BIS_BIS_DER.xml'


def main():
    # messageToXML(pathSaveToGeneric, message)

    datasets = getDatasets(pathToDataFile, pathToMetadataFile, dataset_type=DatasetType.StructureDataSet)

    # message = Message(DatasetType.GenericDataSet, datasets)

    # xmlToJSON(pathSaveToGeneric, pathToMetadataFile, pathToJSON, dataset_type=DatasetType.GenericDataSet)

    # xmlToCSV(pathSaveToGeneric, pathToMetadataFile, pathToCSV, dataset_type=DatasetType.GenericDataSet)

    # header = headerCreation(id_='test', dataset_type=DatasetType.GenericDataSet)

    """
    gui = show(dataset_list)

    dataframes = gui.get_dataframes()

    for e in dataset_list:
        e.obs = dataframes[e.code]
    """


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


if __name__ == '__main__':
    main()
