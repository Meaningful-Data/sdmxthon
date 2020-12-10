import logging
import sys

from lxml import etree

from SDMXThon import datasetListToXML, headerCreation, xmlToDatasetList, DatasetType
from SDMXThon.utils.parsers import get_codelist_model, get_concept_schemes, get_DSDs

pathToDataFile = 'SDMXThon/test/ecu/IRIS/R017_ALE.csv'
pathToMetadataFile = 'SDMXThon/test/ecu/IRIS/RBI_DSD(1.0)_20052020.xml'
# pathToMetadataFile = 'SDMXThon/metadataTests/sampleFiles/ECB_SHS6_metadata.xml'
# pathToMetadataFile = 'SDMXThon/metadataTests/sampleFiles/IMF_ALT_FISCAL_DSD.xml'
pathToMetadataTimeSeries = 'SDMXThon/test/TimeSeries/metadata_ecb.xml'
pathToSDMXCodelist = 'SDMXThon/metadataTests/sampleFiles/SDMXcodelist.xml'

# pathSaveToGeneric = 'SDMXThon/test/ecu/IRIS/gen_DMID.xml'
pathSaveToGeneric = 'SDMXThon/outputTests/outputGen.xml'
pathSaveToGeneric2 = 'SDMXThon/outputTests/outputGenTestDSD.xml'
pathTimeSeriesGen = 'SDMXThon/test/TimeSeries/test_ecb_gen.xml'
pathTimeSeriesSpe = 'SDMXThon/test/TimeSeries/test_ecb_xs.xml'
pathTimeSeriesGenTest = 'SDMXThon/outputTests/time_gen.xml'

pathSaveToStructure = 'SDMXThon/outputTests/demo_structure.xml'
pathSaveToStructure2 = 'SDMXThon/outputTests/outputSpeTestDSD.xml'

pathSavetoJSON = 'SDMXThon/outputTests/output.json'
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


def main():
    """
    # SDMX to CSV Generic
    dataset_list = xmlToDatasetList(pathSaveToGeneric, pathToMetadataFile, DatasetType.GenericDataSet)
    for e in dataset_list:
        filename = "SDMXThon/outputTests/CSVGen/" + e.code + '.csv'
        e.obs.to_csv(filename, sep=',', encoding='utf-8', index=False, header=True)

    # SDMX to Pandas Structure Specific
    dataset_list = xmlToDatasetList(pathSaveToStructure, pathToMetadataFile, DatasetType.StructureDataSet)
    for e in dataset_list:
        filename = "SDMXThon/outputTests/CSVSpe/" + e.code + '.csv'
        e.obs.to_csv(filename, sep=',', encoding='utf-8', index=False, header=True)

    # SDMX Generic to DataSet to SDMX Generic
    dataset_list = xmlToDatasetList(pathSaveToGeneric, pathToMetadataFile, DatasetType.GenericDataSet)

    header = headerCreation(id_='test', dataset_type=DatasetType.GenericDataSet)
    datasetListToXML(dataset_list, pathToMetadataFile, pathSaveToGeneric, header,
                     dataset_type=DatasetType.GenericDataSet, validate_data=False)

    # SDMX Structure to DataSet to SDMX Structure
    dataset_list = xmlToDatasetList(pathSaveToStructure, pathToMetadataFile, DatasetType.StructureDataSet)

    header = headerCreation(id_='test', dataset_type=DatasetType.StructureDataSet)
    datasetListToXML(dataset_list, pathToMetadataFile, pathSaveToStructure, header,
                     dataset_type=DatasetType.StructureDataSet, validate_data=False)

    # SDMX Structure to DataSet to SDMX Generic
    dataset_list = xmlToDatasetList(pathSaveToStructure2, pathToMetadataFile, DatasetType.StructureDataSet)

    header = headerCreation(id_='test', dataset_type=DatasetType.StructureDataSet)
    datasetListToXML(dataset_list, pathToMetadataFile, pathSaveToStructure, header,
                     dataset_type=DatasetType.StructureDataSet, validate_data=False)


    """
    """
    # SDMX Generic to DataSet to SDMX Structure
    dataset_list = xmlToDatasetList(pathSaveToStructure, dsds, DatasetType.StructureDataSet)

    header = headerCreation(id_='test', dataset_type=DatasetType.StructureDataSet)
    datasetListToXML(dataset_list, pathToMetadataFile, pathSaveToStructure2, header,
                     dataset_type=DatasetType.StructureDataSet, validate_data=False)
    # datasetListToJSON(dataset_list, pathSavetoJSON)
    """
    """
    # Passing path to file
    dataset_list = xmlToDatasetList(pathSaveToStructure, pathToMetadataFile, DatasetType.StructureDataSet)

    header = headerCreation(id_='test', dataset_type=DatasetType.GenericDataSet)
    message = generate_message(dataset_list, pathToMetadataFile, header, DatasetType.GenericDataSet,
                               validate_data=False)
    print(message)
    # Passing metadata file already opened
    f = open(pathToMetadataFile, 'rb')
    dataset_list = xmlToDatasetList(pathSaveToStructure, f, DatasetType.StructureDataSet)
    header = headerCreation(id_='test', dataset_type=DatasetType.StructureDataSet)
    f.seek(0)
    message = generate_message(dataset_list, f, header, DatasetType.StructureDataSet, validate_data=False)
    print(message)
    logger.debug('Start metadata loading')
    sdmx = etree.parse(pathToSDMXCodelist)
    codelists = get_codelist_model(sdmx)
    logger.debug('File parsed')
    root = etree.parse(pathToMetadataFile)
    codelists = add_elements_to_dict(codelists, get_codelist_model(root), updateElementsFromDict2=True)
    """

    # Testing DSDS
    """
    root = etree.parse(pathToMetadataFile)
    codelists = get_codelist_model(root)
    logger.debug('Codelists loaded')
    concepts = get_concept_schemes(root, codelists)
    dsds = get_DSDs(root, concepts, codelists)
    test_dsds = dsds.copy()
    # True
    print(test_dsds == dsds)

    logger.debug('Dump')
    serial = pickle.dumps(dsds)
    logger.debug('Load')
    new_dsds = pickle.loads(serial)
    logger.debug('End Load')
    # True
    set_dsds_checked_to_false(new_dsds)
    set_dsds_checked_to_false(test_dsds)
    print(new_dsds == test_dsds)
    logger.debug('Fin comprobacion iguales')
    new_dsds['RBI:AALOE(1.0)'].dimensionDescriptor.components[
        'Area_Operation'].localRepresentation.codeList._name = 'BLABLABLA'
    set_dsds_checked_to_false(new_dsds)
    set_dsds_checked_to_false(test_dsds)
    # False
    print(new_dsds == test_dsds)

    
    logger.debug('Data Structure Definitions loaded')
    logger.debug('Inicio')
    print('DSDS: %d' % get_size(dsds))
    logger.debug('Fin')

    print('concepts: %d' % get_size(concepts))
    print('codelists: %d' % get_size(codelists))
    codelists, concepts = delete_unused_codelists(codelists, concepts, dsds)
    print('concepts: %d' % get_size(concepts))
    print('codelists: %d' % get_size(codelists))
    """

    logger.debug('Inicio')
    root = etree.parse(pathToMetadataTimeSeries)
    codelists = get_codelist_model(root)
    concepts = get_concept_schemes(root, codelists)
    dsds = get_DSDs(root, concepts, codelists)
    logger.debug('DSD loaded')
    """
    logger.debug('Finish serializing')
    logger.debug('Starting serializing list')
    serial = pickle.dumps(dsds)
    logger.debug('Finish serializing list')

    with open('SDMXThon/metadataTests/dsds.pickle', "wb") as f:
        f.write(serial)
    """
    # Testing creating message with dsds
    dataset_list = xmlToDatasetList(pathTimeSeriesGen, dsds, DatasetType.GenericTimeSeriesDataSet)
    logger.debug('End reading')
    header = headerCreation(id_='test', dataset_type=DatasetType.GenericTimeSeriesDataSet)
    datasetListToXML(dataset_list, dsds, pathTimeSeriesGenTest, header,
                     dataset_type=DatasetType.GenericTimeSeriesDataSet, validate_data=True)


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
