import logging

from SDMXThon import readJSON, getMetadata

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
pathTestGEN = 'SDMXThon/outputTests/test_GEN.xml'
pathTestGENSer = 'SDMXThon/outputTests/test_GEN_ser.xml'
pathTestXS = 'SDMXThon/outputTests/test_XS.xml'
pathTestXSSer = 'SDMXThon/outputTests/test_XS_ser.xml'
pathToDataFile = 'SDMXThon/outputTests/BIS_DER_test.xml'
pathSaveToGeneric = 'SDMXThon/outputTests/outputGen.xml'
pathSaveToStructure = 'SDMXThon/outputTests/outputSpe.xml'
pathSaveToTimeGen = 'SDMXThon/outputTests/outputTimeGen.xml'
pathSaveToTimeXS = 'SDMXThon/outputTests/outputTimeXS.xml'
pathToJSON = 'SDMXThon/outputTests/test.json'
pathToCSV = 'SDMXThon/outputTests/csv.zip'
# pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/RBI_DSD(1.0)_20052020.xml'
pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/DSD_FILE_202012240033006.xml'
urlMetadata = 'http://fusionregistry.meaningfuldata.eu/MetadataRegistry/ws/public/sdmxapi/rest/datastructure/BIS/BIS_DER/latest/?format=sdmx-2.1&detail=full&references=all&prettyPrint=true'
pathToDB = 'SDMXThon/outputTests/BIS_DER_OUTS.db'
pathToDataBIS = 'SDMXThon/outputTests/BIS_DER_OUTS.xml'
pathToData = 'SDMXThon/outputTests/BIS_DER_test.xml'
pathTest = 'SDMXThon/outputTests/RBI_test.xml'
patternTest = 'SDMXThon/outputTests/pattern_test.xml'
pathToCSVData = 'SDMXThon/outputTests/BIS_data.csv'
pathToCSVData2 = 'SDMXThon/outputTests/BIS_data2.csv'


# pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/BIS_BIS_DER.xml'


def main():
    dsds, errors = getMetadata(pathToMetadataFile)
    logger.debug('Start reading')
    datasets = readJSON(pathToJSON, dsds)
    logger.debug('End reading')

    """
    logger.debug('Start reading')
    dataset = getDatasets(pathTest, pathToMetadataFile, DatasetType.GenericDataSet)
    logger.debug('End reading')

    logger.debug('Start validations')
    e = dataset['ASSETS_EX_LNA_SLR']
    #print(f'-----------{e.structure.id}------------')
    print(e.data.memory_usage(deep=True))
    
    all_codes = e.structure.dimensionCodes + e.structure.attributeCodes
    data_codes = []
    for i in all_codes:
        if i in e.data.keys() and i != 'DMID':
            data_codes.append(i)
    
    
    e.data[data_codes] = e.data[data_codes].astype("category")
    e.data[e.structure.measureCode] = e.data[e.structure.measureCode].astype("float32")


    #print(e.data['Asset_Ex_LNA'])
    print(e.data.memory_usage(deep=True))
    print(e.data['DMID'])
    logger.debug('End validations')
    """
    """
    datasets = getDatasets(pathTestGEN, urlMetadata, DatasetType.GenericDataSet)
    logger.debug('End reading data old')
    """

    """
    logger.debug('Start reading')
    conn = sqlite3.connect(pathToDB)
    df = pd.read_sql('SELECT * from BIS_DER_little', conn)
    logger.debug('End reading')

    df['FREQ'] = 'S'

    dsds = getMetadata(urlMetadata)
    dsd: DataStructureDefinition = dsds["BIS:BIS_DER(1.0)"]

    grouping_keys = dsd.dimensionCodes
    grouping_keys.remove('TIME_PERIOD')

    for e in dsd.attributeDescriptor.components.values():
        e: Attribute
        if e.id in df.keys() and e.relatedTo is not None and not isinstance(e.relatedTo, PrimaryMeasure):
            grouping_keys.append(e.id)

    logger.debug('Start grouping')

    yourdf = df[~df.duplicated(subset=grouping_keys)][grouping_keys].reset_index()
    logger.debug('End grouping')
    """
    """ DEMO 3
    dataset.toXML(DatasetType.GenericDataSet, pathTest)

    message = Message(DatasetType.GenericDataSet)
    message.readJSON(pathToJSON, urlMetadata)
    message.toXML(pathTest)
    """

    """
    dataset.setDimensionAtObservation('AllDimensions')
    dataset.toXML(DatasetType.GenericDataSet, pathTestGEN)
    logger.debug('Fin All Generic')

    dataset.setDimensionAtObservation('TIME_PERIOD')
    dataset.toXML(DatasetType.StructureDataSet, pathTestXSSer)
    logger.debug('Fin Series Structure')

    dataset.setDimensionAtObservation('AllDimensions')
    dataset.toXML(DatasetType.StructureDataSet, pathTestXS)
    logger.debug('Fin All Structure')
    """

    """
    logger.debug('Start')
    message = Message(DatasetType.GenericDataSet)
    message.readJSON(pathToJSON, urlMetadata)
    logger.debug('Reading JSON')

    message.toXML(pathTestGENSer)
    logger.debug('Writing to Generic (AllDimensions)')

    message.setDimensionAtObservation('AllDimensions')
    message.toXML(pathTestGEN)
    logger.debug('Writing to Generic (TimeSeries)')

    message.type = DatasetType.StructureDataSet
    message.toXML(pathTestXS)
    logger.debug('Writing to Structure (AllDimensions)')


    message.setDimensionAtObservation('TIME_PERIOD')
    message.toXML(pathTestXSSer)
    logger.debug('Writing to Structure (TimeSeries)')
    """


if __name__ == '__main__':
    main()
