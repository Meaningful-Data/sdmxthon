import pandas as pd

from SDMXThon.common.pandasElement import DataSet

path_to_csv = 'ecu/IRIS/R017_ALE.csv'
path_to_metadata = 'ecu/IRIS/RBI_DSD(1.0)_20052020.xml'
save_path_structure = 'ecu/IRIS/output.xml'


def csvIdenticalChecker(path_file_1='ecu/IRIS/generic.csv', path_file_2='ecu/IRIS/structure.csv'):
    with open(path_file_1, 'r') as t1, open(path_file_2, 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

        for line in filetwo:
            if line not in fileone:
                try:
                    print('File: %s, Line number: %d' % (path_file_2, filetwo.index(line)))
                except:
                    try:
                        print('File: %s, Line number: %d' % (path_file_1, fileone.index(line)))
                    except:
                        print('could not determine nº of line missing. Text: %s' % (line))


def sdmxStructureToPandas(rootObj, index='DMID') -> []:
    pandasList = []
    for e in rootObj.DataSet:
        item = DataSet()
        indexArray = {}
        item.attrib = e._anyAttributes_
        length = -1
        for i in e._obs:
            if length == -1:
                length = len(i._anyAttributes_)
            else:
                if len(i._anyAttributes_) != length:
                    control = True
                    break
            for key, value in i._anyAttributes_.items():
                if key in indexArray.keys():
                    indexArray[key].append(value)
                else:
                    indexArray[key] = [value]

        item.df = pd.DataFrame.from_dict(indexArray)
        pandasList.append(item)

    return pandasList


def sdmxGenericToPandas(rootObj, index='DMID') -> []:
    pandasList = []
    for e in rootObj.DataSet:
        item = DataSet()
        indexArray = {}
        for j in e._Attributes.Value:
            item.attrib[j._id] = j._value
        item.attrib['structureRef'] = e._structureRef
        length = -1
        for i in e._obs:
            if length == -1:
                length = len(i._Attributes.Value)
            else:
                if len(i._Attributes.Value) != length:
                    control = True
                    break
            for a in i.ObsKey.Value:
                if a._id in indexArray.keys():
                    indexArray[a._id].append(a._value)
                else:
                    indexArray[a._id] = [a._value]

            for b in i._Attributes.Value:
                if b._id in indexArray.keys():
                    if b._value == '':
                        indexArray[b._id].append('N_A')
                    else:
                        indexArray[b._id].append(b._value)
                else:
                    if b._value == '':
                        indexArray[b._id] = ['N_A']
                    else:
                        indexArray[b._id] = [b._value]

        item.df = pd.DataFrame.from_dict(indexArray)
        pandasList.append(item)

    return pandasList


def main():
    """
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

    save_path_structure = 'ecu/IRIS/structure.xml'

    logger.debug("Empieza carga structure desde csv")
    csv = CsvDataSet()
    csv.load_from_csv(path_to_csv)
    structure_message = csv_to_structure_data_set(csv, path_to_metadata, header=None, dataset_type=DatasetType.StructureDataSet)
    logger.debug("Finaliza carga structure")

    save_path_generic = 'ecu/IRIS/generic.xml'
    logger.debug("Empieza carga generic desde csv")
    generic_message = csv_to_generic_data_set(csv, path_to_metadata, header=None, dataset_type=DatasetType.GenericDataSet)
    logger.debug("Finaliza carga generic desde csv")
    save_csv_structure = 'ecu/IRIS/structure.csv'
    save_csv_generic = 'ecu/IRIS/generic.csv'

    logger.debug("Empieza guardar fichero XML structure")
    f = open(save_path_structure, "w")
    structure_message.export(f, 0, pretty_print=True, has_parent=False)
    f.close()
    logger.debug("Finaliza XML structure")

    logger.debug("Empieza guardar fichero XML generic")
    g = open(save_path_generic, "w")
    generic_message.export(g, 0, pretty_print=True, has_parent=False)
    g.close()
    logger.debug("Finaliza XML generic")


    # CSV Optimization
    logger.debug("Empieza guardar fichero csv structure")
    datasetList = sdmxStructureToPandas(structure_message)
    for e in datasetList:
        filename = e.attrib['xsi:type'].split(':', 1)[0]
        e.df.to_csv('ecu/IRIS/CSVTest/Structure/' + filename + ".csv", index=False, header=True)
    logger.debug("Finaliza csv structure")

    logger.debug("Empieza guardar fichero csv generic")
    datasetList = sdmxGenericToPandas(generic_message)
    for e in datasetList:
        filename = e.attrib['structureRef']
        e.df.to_csv('ecu/IRIS/CSVTest/Generic/' + filename + ".csv", index=False, header=True)
    logger.debug("Finaliza csv generic")

    # End CSV Optimization

    logger.debug("Empieza guardar fichero csv structure")
    data = message_to_dataframe_filter_by_metadata(structure_message, path_to_metadata)
    logger.debug("Pandas structure loaded")
    data.to_csv(save_csv_structure, index=False, header=True)
    logger.debug("Finaliza csv structure")

    logger.debug("Empieza guardar fichero csv generic")
    data = message_to_dataframe_filter_by_metadata(generic_message, path_to_metadata)
    logger.debug("Pandas generic loaded")
    data.to_csv(save_csv_generic, index=False, header=True)
    logger.debug("Finaliza csv generic")

    # csvIdenticalChecker(save_csv_structure, save_csv_generic)
    """


if __name__ == '__main__':
    main()
