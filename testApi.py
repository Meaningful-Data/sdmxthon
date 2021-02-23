import logging

from SDMXThon import readSDMX
from SDMXThon.model.itemScheme import Agency

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
pathToJSON = 'SDMXThon/outputTests/test.json'
pathToCSV = 'SDMXThon/outputTests/csv.zip'
# pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/DSD_FILE_202012240033006_0701.xml'
pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/DSD_FILE_04FEB21.xml'
# pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/BIS_BIS_DER.xml'
urlMetadata = 'http://fusionregistry.meaningfuldata.eu/MetadataRegistry/ws/public/sdmxapi/rest/datastructure' \
              '/BIS/BIS_DER/latest/?format=sdmx-2.1&detail=full&references=all&prettyPrint=true'
pathToDB = 'SDMXThon/outputTests/BIS_DER_OUTS.db'
pathToDataBIS = 'SDMXThon/outputTests/BIS_DER_OUTS.xml'
pathToDataSpe = 'SDMXThon/examples/Structure/outputSpe.xml'
pathToDataGen = 'SDMXThon/examples/Generic/outputGen.xml'
pathToDataGenSer = 'SDMXThon/examples/Generic/genSeries.xml'
pathToCSVData = 'SDMXThon/outputTests/BIS_data.csv'
pathToCSVData2 = 'SDMXThon/outputTests/BIS_data2.csv'


# pathToMetadataFile = 'SDMXThon/outputTests/metadata/sampleFiles/BIS_BIS_DER.xml'

def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def parse_agencies(xml_element, agency_scheme):
    expression = "./str:Agency"
    agencies = xml_element.xpath(expression,
                                 namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    if agencies is not None:
        for e in agencies:
            a = Agency(id_=e.attrib['id_'], uri=e.attrib['urn'], scheme=agency_scheme)

            expression = "./com:Name/text()"
            name = e.xpath(expression,
                           namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(name) > 0:
                a.name = str(name[0])

            expression = "./com:Description/text()"
            desc = e.xpath(expression,
                           namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(desc) > 0:
                a.description = str(desc[0])


def main():
    logger.debug('Start')
    datasets = readSDMX(pathToMetadataFile, pathToMetadataFile)
    logger.debug('Read')

    for e in datasets.payload.keys():
        datasets.payload[e].semanticValidation()
    logger.debug('Validate')

    """
    root = etree.parse(pathToMetadataFile)

    expression = "/mes:Structure/mes:Structures/str:OrganisationSchemes/str:AgencyScheme"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if result is not None:

        schemes = []

        for a in result:
            agency_scheme = AgencyList(id_=a.attrib['id_'], version=a.attrib['version'],
                                       maintainer=Agency(id_=a.attrib['agencyID']))

            expression = "./com:Name/text()"
            name = a.xpath(expression,
                           namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(name) > 0:
                agency_scheme.name = str(name[0])

            parse_agencies(a, agency_scheme)

            schemes.append(agency_scheme)

        print(schemes)

    else:
        return None
    """
    """
    dsds, errors = getMetadata(pathToMetadataFile)

    with open('test_metadata.json', 'w') as f:
        f.write(json.dumps(dsds))
    """
    """
    logger.debug('Start reading')
    conn = sqlite3.connect(pathToDB)
    df = pd.read_sql('SELECT * from BIS_DER LIMIT 1000', conn)
    logger.debug('End reading')

    df['FREQ'] = 'A'

    dsds, errors = getMetadata(urlMetadata)
    dsd: DataStructureDefinition = dsds["BIS:BIS_DER(1.0)"]

    dataset = DataSet(data=df, structure=dsd)
    dataset.setDimensionAtObservation('TIME_PERIOD')
    logger.debug('Start writing')
    dataset.toXML(DatasetType.StructureDataSet, 'test_series.xml')
    logger.debug('End writing')
    """
    """
    logger.debug('Start reading')
    conn = sqlite3.connect(pathToDB)
    df = pd.read_sql('SELECT * from BIS_DER LIMIT 1000', conn).astype('category')
    df['FREQ'] = 'A'
    with open('dsd.pickle', 'rb') as f:
        dsd = pickle.loads(f.read())

    dataset = DataSet(data=df, structure=dsd)
    logger.debug('Start')

    dimObs = "TIME_PERIOD"

    prettyprint = True

    outfile = ''

    df = dataset.data.dropna(axis=1, how="all")

    if prettyprint:
        child1 = '\t'
        child2 = '\t\t'
        child3 = '\t\t\t'
        child4 = '\t\t\t\t'
        child5 = '\t\t\t\t\t'
        nl = '\n'
    else:
        child1 = child2 = child3 = child4 = child5 = nl = ''

    series_key_codes = []
    series_att_codes = []
    obs_att_codes = []
    for e in dataset.structure.attributeDescriptor.components.values():
        if e.id_ in dataset.data.keys() and isinstance(e.relatedTo, PrimaryMeasure):
            obs_att_codes.append(e.id_)
    for e in dataset.data.keys():
        if e in dataset.structure.dimensionCodes and e != dimObs:
            series_key_codes.append(e)
        elif e in dataset.structure.attributeCodes and e not in obs_att_codes:
            series_att_codes.append(e)

    obs_value_data = df[dataset.structure.measureCode].astype('str')
    obs_dim_data = df[dimObs].astype('str')

    del df[dataset.structure.measureCode]
    del df[dimObs]

    df = df.sort_values(series_key_codes + series_att_codes, axis=0).astype('str')
    df_series: pd.DataFrame = df[series_key_codes + series_att_codes].drop_duplicates()
    df_id = f'{child4}<generic:Value id_="' + pd.DataFrame(
        np.tile(np.array(df_series.columns), len(df_series.index)).reshape(len(dataset.data.index), -1),
        index=dataset.data.index,
        columns=dataset.data.columns, dtype='str') + '" value="'
    df_value = dataset.data.astype('str') + '"/>'
    df_id: pd.DataFrame = df_id.add(df_value)



    df_obs_dim = f'{child3}<generic:ObsDimension value="' + obs_dim_data + '"/>'
    df_obs_value = f'{child3}<generic:ObsValue value="' + obs_value_data + '"/>'
    df_id[dimObs] = df_obs_dim
    df_id['OBS_VALUE'] = df_obs_value
    df_id.insert(0, 'head', f'{child2}<generic:Obs>')
    df_id.insert(len(df_id.keys()), 'end', f'{child2}</generic:Obs>')

    dim_codes = []
    att_codes = []
    for e in df_id.keys():
        if e in dataset.structure.dimensionCodes:
            dim_codes.append(e)
        elif e in dataset.structure.attributeCodes:
            att_codes.append(e)

    all_codes = ['head']
    all_codes += series_key_codes
    all_codes += series_att_codes
    all_codes.append(dim_codes)
    all_codes.append('OBS_VALUE')
    all_codes += obs_att_codes
    all_codes.append('end')
    df_id = df_id.reindex(all_codes, axis=1)

    df_dim = df_id[dim_codes]
    last_dim = len(df_dim.columns) - 1
    df_id.loc[:, df_dim.columns[0]] = f'{child3}<generic:ObsKey>{nl}' + df_dim.loc[:, df_dim.columns[0]]
    df_id.loc[:, df_dim.columns[last_dim]] = df_dim.loc[:, df_dim.columns[last_dim]] + f'{nl}{child3}</generic:ObsKey>'

    df_att = df_id[att_codes]
    last_att = len(df_att.columns) - 1
    df_id.loc[:, df_att.columns[0]] = f'{child3}<generic:Attributes>{nl}' + df_att.loc[:, df_att.columns[0]]
    df_id.loc[:, df_att.columns[last_att]] = df_att.loc[:, df_att.columns[last_att]] + f'{nl}' \
                                                                                       f'{child3}</generic:Attributes>'

    obs_str = ''
    obs_str += df_id.to_csv(path_or_buf=None, sep='\n', header=False, index=False, quoting=csv.QUOTE_NONE,
                            escapechar='\\')
    obs_str = obs_str.replace('\\', '')
    obs_str = obs_str.replace('="nan"', '=""')
    man_att = get_mandatory_attributes(dataset.structure)

    for e in dataset.structure.attributeCodes:
        if e in df_id.keys() and e not in man_att:
            obs_str = obs_str.replace(f'{child4}<generic:Value id_="{e}" value=""/>{nl}', '')

    obs_str = f'{nl}'.join(obs_str.splitlines())




    logger.debug('End')

    """
    """ DEMO 3
    dataset.toXML(DatasetType.GenericDataSet, pathTest)

    message = Message(DatasetType.GenericDataSet)
    message.readJSON(pathToJSON, urlMetadata)
    message.toXML(pathTest)
    """


if __name__ == '__main__':
    main()
