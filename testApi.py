import logging
import pickle
import sys

from SDMXThon import datasetListToXML, headerCreation, xmlToDatasetList, DatasetType

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

pathDSDS = 'SDMXThon/outputTests/metadata/dsds.pickle'
pathToDataFile = 'SDMXThon/test/BIS/'
pathSaveToGeneric = 'SDMXThon/outputTests/outputGen.xml'
pathSaveToStructure = 'SDMXThon/outputTests/outputSpe.xml'
pathSaveToTimeGen = 'SDMXThon/outputTests/outputTimeGen.xml'
pathSaveToTimeXS = 'SDMXThon/outputTests/outputTimeXS.xml'
pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/RBI_DSD(1.0)_20052020.xml'


def main():
    """
    root = etree.parse(pathToMetadataFile)

    codelists = get_codelist_model(root)
    concepts = get_concept_schemes(root, codelists)
    dsds = get_DSDs(root, concepts, codelists)
    """
    with open(pathDSDS, 'rb') as f:
        dsds = pickle.loads(f.read())

    dataset_list = xmlToDatasetList(pathSaveToStructure, dsds, DatasetType.StructureDataSet)
    header = headerCreation(id_='test', dataset_type=DatasetType.GenericDataSet)
    datasetListToXML(dataset_list, dsds, pathSaveToGeneric, header,
                     dataset_type=DatasetType.GenericDataSet)


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
