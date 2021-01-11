import logging
import sqlite3

import pandas as pd

from SDMXThon import DatasetType, getMetadata, DataSet
from SDMXThon.model.structure import DataStructureDefinition

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


def addRowStrToOutfile(row):
    string = ''
    for k, v in row.items():
        string += f'{k}="{v}" '
    return f'\t\t<Obs {string}>\n'


def main():
    """
    datasets = getDatasets(pathTestGEN, urlMetadata, DatasetType.GenericDataSet)
    logger.debug('End reading data old')
    """

    logger.debug('Start reading')
    conn = sqlite3.connect(pathToDB)
    df = pd.read_sql('SELECT * from BIS_DER LIMIT 1', conn)
    logger.debug('End reading')

    df['FREQ'] = 'A'

    dsds, errors = getMetadata(urlMetadata)
    dsd: DataStructureDefinition = dsds["BIS:BIS_DER(1.0)"]

    attached_attributes = {}

    for e in df.keys():
        if e in dsd.datasetAttributeCodes:
            attached_attributes[e] = df.loc[0, e]
            del df[e]
    dimObs = 'TIME_PERIOD'

    prettyprint = True

    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        nl = '\n'
    else:
        child1 = child2 = nl = ''

    logger.debug('Start')
    dataset = DataSet(data=df, structure=dsd, attached_attributes=attached_attributes)
    dataset.toXML(dataset_type=DatasetType.StructureDataSet, outputPath='test.xml')
    logger.debug('End')

    """
    del df

    series_codes = []
    obs_codes = [dimObs]
    obs_codes.append(dsd.measureCode)
    for e in dsd.attributeDescriptor.components.values():
        if e.id in dataset.data.keys() and isinstance(e.relatedTo, PrimaryMeasure):
            obs_codes.append(e.id)
    for e in dataset.data.keys():
        if (e in dsd.dimensionCodes and e != dimObs) or (e in dsd.attributeCodes and e not in obs_codes):
            series_codes.append(e)

    series_df = dataset.data[~dataset.data.duplicated(series_codes)][series_codes]

    series_df.reset_index(drop=True, inplace=True)

    df1 = pd.DataFrame(np.tile(np.array(obs_codes), len(dataset.data.index))
                       .reshape(len(dataset.data.index), -1),
                       index=dataset.data.index,
                       columns=obs_codes, dtype='str') + '='
    df2 = '"' + dataset.data[obs_codes].astype('str') + '"'
    df1 = df1 + df2
    df1.insert(0, 'head', f'{child2}<Obs')
    df1.insert(len(df1.keys()), 'end', '/>')
    obs_str = ''
    obs_str += df1.to_csv(path_or_buf=None, sep=' ', header=False, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    obs_str = obs_str.replace('\\', '')
    obs_str = f'{nl}'.join(obs_str.splitlines())
    obs_str.replace(' />', '/>')

    with open('test.xml', 'w') as f:
        f.write(obs_str)
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
