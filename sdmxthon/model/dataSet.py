from lxml import etree
import pandas as pd
from datetime import datetime
from sdmxthon.model.base import AnnotableArtefact
from sdmxthon.model.structure import DataFlowDefinition, DataStructureDefinition
from sdmxthon import utils
import numpy as np
from typing import Union

class DataSet(AnnotableArtefact):
    #TODO: Implement dimension ad group attributes
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, 
                  reference:Union[DataFlowDefinition, DataStructureDefinition] = None,
                  datasetAttributes:dict = None):
        
        super(DataSet, self).__init__(annotations = annotations)
    
        self.data = data
        self.reference = reference
        self.datasetAttributes = datasetAttributes

    @property
    def data(self):
        return self._data
        
    @property
    def reference(self):
        return self._reference

    @property
    def referenceType(self):
        return type(self.reference)

    @property
    def datasetAttributes(self):
        return self._datasetAttributes

    @data.setter 
    def data(self, value):
        if isinstance(value, pd.DataFrame):
            self._data = value
        else:
            raise TypeError("Data has to be provided as a pandas DataFrame")

    @reference.setter
    def reference(self, value):
        if isinstance(value, DataFlowDefinition) or isinstance(value, DataStructureDefinition):
            self._reference = value
        else:
            raise ValueError(f"DataStructureDefinition or DataFlowDefinition Expected, {type(value)} obtained")
    
    @datasetAttributes.setter
    def datasetAttributes(self, value):
       self._datasetAttributes = utils.genericSetter(value, dict)

class GenericDataSet(DataSet):
        
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, reference = None, datasetAttributes:dict = None):
        
        super(GenericDataSet, self).__init__(annotations = annotations, data = data, 
                                            reference = reference, datasetAttributes = datasetAttributes)

    def toXml(self, action:str = "Replace",  dimensionAtObservation = "AllDimensions"):
        """
          
        """

        #1. Create root tag
        root = etree.Element(utils.qName("mes", "DataSet"))
        root.attrib["action"] = "Replace"
        root.attrib["structureRef"] = self.reference.id
        root.attrib["validFromDate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')



        #2. Get dataset attributes
        if self.datasetAttributes is not None:
            dsAttributes = etree.Element(utils.qName("gen", "Attributes"))
            
            for a in self.datasetAttributes:
                value = etree.Element(utils.qName("gen", "Value"), attrib={"id":a, "value":self.datasetAttributes[a]})
                dsAttributes.append(value)

            if not utils.lxmlElementsEqual(dsAttributes, etree.Element(utils.qName("gen", "Attributes"))): #Checks if there is any value
                root.append(dsAttributes)
        
        #3. Dimension at observation == AllDimensions
        if dimensionAtObservation == "AllDimensions":
            
            #3.0 Convert the data to a list of JSON objects
            dataList = self.data.replace({np.nan:None}).to_dict('records')

                #3.1  For each data point
            for d in dataList:
                #3.2 Create the root elemens
                obs = etree.Element(utils.qName("gen", "Obs"))
                att = etree.Element(utils.qName("gen", "Attributes"))
                obsKey = etree.Element(utils.qName("gen", "ObsKey"))
                obsVal = etree.Element(utils.qName("gen", "ObsValue"))
                
                #3.3 For each key-value pair
                for k in d:
                    #3.3.1 Create genric:Value tag if the value is not None
                    value = etree.Element(utils.qName("gen", "Value"), attrib={"id":k, "value":str(d[k])}) if d[k] is not None else None

                    #.3.2.2 If the key-value corresponds to a dimension
                    if k in self.reference.dimensionCodes:
                        #3.2.2.1 Raise error if the value is None, because dimensions need to have a value
                        if value is None:
                            raise ValueError(f"The dimension {k} has an empty value")
                        
                        #3.2.2.2 Attach the dimension to the right tag depending on the dimensionAtObservation                        
                        obsKey.append(value)

                    #3.2.3 If the key-value corresponds to an attribute
                    elif k in self.reference.attributeCodes: 
                        if value is not None:
                            att.append(value)
                    
                    #3.2.4 If the key-value corresponds to the primary measure
                    elif k == self.reference.measureCode:
                        obsVal.attrib["value"] = d[k]  if d[k] is not None else ""

                obs.append(obsKey)
                obs.append(obsVal)                
                obs.append(att)

                root.append(obs)
                       
        #4.  Dimention at observation != AllDimensions
        else:
            dimNotObs = self.reference.dimensionCodes
            dimNotObs.remove(dimensionAtObservation)
            
            for name, group in self.data.replace({np.nan:None}).groupby(by=dimNotObs):
                dataList = group.to_dict('records')

                series = etree.Element(utils.qName("gen", "Series"))
                
                first = True
                for d in dataList:
                    seriesKey = etree.Element(utils.qName("gen", "SeriesKey"))
                    att = etree.Element(utils.qName("gen", "Attributes"))
                    obs = etree.Element(utils.qName("gen", "Obs")) 

                    for k in d:
                        #Create genric:Value tag if the value is not None
                        value = etree.Element(utils.qName("gen", "Value"), attrib={"id":k, "value":str(d[k])}) if d[k] is not None else None
                    
                        #If the key-value corresponds to a dimension
                        if k in self.reference.dimensionCodes:
                            #Raise error if the value is None, because dimensions need to have a value
                            if value is None:
                                raise ValueError(f"The dimension {k} has an empty value")

                            #Attach the dimension to the right tag depending on the dimensionAtObservation
                            if k == dimensionAtObservation:
                                obsDimension = etree.Element(utils.qName("gen", "ObsDimension"), attrib={"value":d[k]})
                                obs.append(obsDimension)
                            else:
                                seriesKey.append(value)

                        #If the key-value corresponds to an attribute
                        if k in self.reference.attributeCodes: 
                            if value is not None:
                                att.append(value)
                        
                        #If the key-value corresponds to the primary measure
                        elif k == self.reference.measureCode:
                            val = d[k] if d[k] is not None else ""
                            obsValue = etree.Element(utils.qName("gen", "ObsValue"), attrib={"id":k, "value":val})
                            obs.append(obsValue)
                
                    if first:
                        series.append(seriesKey)    
                        first = False

                    obs.append(att)
                    series.append(obs)
                    
                    
                root.append(series)                

        return root


    def toStructureSpecificDataSet(self):
        return StructureSpecificDataSet(
            annotations = self.annotations,
            data = self.data,
            dsd = self.dsd
        )
    
class StructureSpecificDataSet(DataSet):
        
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, reference = None, datasetAttributes:dict = None):
        
        super(StructureSpecificDataSet, self).__init__(annotations = annotations, data = data, 
                                                        reference = reference, datasetAttributes = datasetAttributes)

    def toXml(self, action:str = "Replace",  dimensionAtObservation = "AllDimensions"):
        """
           
        """

        #1. Create root tag
        root = etree.Element(utils.qName("mes", "DataSet"))
        root.attrib[utils.qName("data", "action")] = "Replace"
        root.attrib[utils.qName("data", "structureRef")] = self.reference.id
        root.attrib["validFromDate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        root.attrib[utils.qName("data", "dataScope")] =  "DataFlow" if self.referenceType == "DataFlowDefinition" else "DataStructure"
        root.attrib[utils.qName("xsi", "type")] = f"{self.reference.id}:DataSetType"


        #Where do dataset attributes go?
        # if self.datasetAttributes is not None:
        #     dsAttributes = etree.Element(utils.qName("data", "Attributes"))
            
        #     for a in self.datasetAttributes:
        #         value = etree.Element(utils.qName("data", "Value"), attrib={"id":a, "value":self.datasetAttributes[a]})
        #         dsAttributes.append(value)

        #     root.append(dsAttributes)


        #2. Convert the data to a list of JSON objects
        if dimensionAtObservation == "AllDimensions":        
            dataList = self.data.replace({np.nan:None}).to_dict('records')

            #3. For each data point
            for d in dataList:               
                obs = etree.Element("Obs")

                for k in d:
                    if k in self.reference.dimensionCodes:
                        if d[k] is None:
                            raise ValueError(f"The dimension {k} has an empty value")
                    
                    if d[k] is not None:
                        obs.attrib[k] = str(d[k])

                root.append(obs)

        else:
            dimNotObs = self.reference.dimensionCodes
            dimNotObs.remove(dimensionAtObservation)
            
            for name, group in self.data.replace({np.nan:None}).groupby(by=dimNotObs):
                dataList = group.to_dict('records')

                series = etree.Element("Series")
                  
                for d in dataList:
                    obs = etree.Element("Obs") 

                    for k in d:
                        if k in self.reference.dimensionCodes:
                            if d[k] is None:
                                raise ValueError(f"The dimension {k} has an empty value")
                            if k == dimensionAtObservation:
                                obs.attrib[k] = str(d[k])
                            else:
                                series.attrib[k] = str(d[k])#TODO: Improve. Now it rewrites the dimensions in the series for each observation. Should be done once.
                        
                        elif d[k] is not None:
                            obs.attrib[k] = str(d[k])

                    series.append(obs)
                        
                        
                root.append(series)       

        return root


    def toGenericDataSet(self):
        return GenericDataSet(
            annotations = self.annotations,
            data = self.data,
            reference = self.reference
        )