import logging

from lxml import etree

from SDMXThon.utils.parsers import get_codelist_model, get_concept_schemes, get_DSDs

pathToDataFile = 'SDMXThon/test/ecu/IRIS/R017_ALE.csv'
pathToMetadataFile = 'SDMXThon/test/ecu/IRIS/RBI_DSD(1.0)_20052020.xml'
# pathToMetadataFile = 'SDMXThon/outputTests/DSD_demo_pjan_metadata.xml'

pathSaveToGeneric = 'SDMXThon/test/ecu/IRIS/gen_DMID.xml'
pathSaveToGeneric2 = 'SDMXThon/outputTests/outputGen.xml'

pathSaveToStructure = 'SDMXThon/outputTests/demo_structure.xml'
pathSaveToStructure2 = 'SDMXThon/outputTests/outputSpeTest.xml'

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
    dataset_list = xmlToDatasetList(pathSaveToStructure, pathToMetadataFile, DatasetType.StructureDataSet)

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
    """
    root = etree.parse(pathToMetadataFile)
    codelists = get_codelist_model(root)
    concepts = get_concept_schemes(root, codelists)
    dsds = get_DSDs(root, concepts, codelists)

    print(dsds)

if __name__ == '__main__':
    main()
