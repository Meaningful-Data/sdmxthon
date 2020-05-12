from ECU import ecuDataset
from model import message
from model.dataSet import GenericDataSet
from lxml import etree
from datetime import datetime

URN_DSDS = "urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=RBI:{}(1.0)"

def convertFile(pathToDataFile:str, pathToMetadataFile:str, pathSaveTo:str, id_:str, test:bool = False, 
                 senderId:str = "Unknown", receiverId:str = "not_supplied",
                 reportingBegin:datetime = None, reportingEnd:datetime = None,
                 typeDataset:str = "GenericDataSet", nrDatasets = None):
    
    #1. Read input files
    allDs = ecuDataset.EcuDataset.fromCsv(str(pathToDataFile))
    mesMetadata = message.StructureMessage.fromXml(str(pathToMetadataFile))

    #2. get dsds from ECU file
    dsds = allDs.dsds
    if nrDatasets is not None:
        dsds = dsds[:nrDatasets]

    #3. Create the header
    header = message.Header(
        id_ = id_,
        test = test,
        prepared = datetime.now(),
        senderId = senderId,
        receiverId = receiverId,
        reportingBegin = reportingBegin,
        reportingEnd = reportingEnd
    )

    
    #3. Create correct datasets
    dataSets = []
    for ds in dsds:
        #3.1 If there is no dsd metadata, raise error
        try:
            dsd = mesMetadata.dsds[URN_DSDS.format(ds)]
        except:
            raise ValueError(f"the DSD {ds} has not been loaded as metadata")
        
        #3.2 Attach the dsd to the header
        header.addStructure(dsd)

        #3.3 create a set with all dimensions, attributes and the measure code
        allCodes = dsd.dimensionCodes + dsd.attributeCodes + [dsd.measureCode]
        
        #3.4 Get the dataset only when the DSDID corresponds to the dsd
        df = allDs.data
        dSet = df.loc[df['DSDID'] == ds]
        
        #3.5 If a dimension does not exist, add it with default values
        for d in dsd.dimensionCodes:
            if d not in dSet.columns:
                dSet[d] = "N_A"

        for a in dsd.attributeCodes:
            if a not in dSet.columns:
                dSet[a] = None

        #3.6 get only the required columns
        dSet = dSet[allCodes]

        #3.7 Substitute NaNs for dimensions TODO: See if input files are corrected
        for d in dsd.dimensionCodes:
            dSet[d].fillna("N_A", inplace=True)

        #3.8 instantiate the dataset
        cls_ = globals()[typeDataset]
        dSet = cls_(data = dSet, dsd = dsd)

        dataSets.append(dSet)

    #4. Instantiate new message
    mesData = message.GenericDataMessage(header = header, dataSets=dataSets)

    #5. Save the XML
    mesData.toXml(str(pathSaveTo))