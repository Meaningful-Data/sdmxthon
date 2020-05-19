from lxml import etree
import pandas as pd
from datetime import datetime
from sdmxthon.model.base import AnnotableArtefact
from sdmxthon.model.structure import DataFlowDefinition, DataStructureDefinition
from sdmxthon import utils
import numpy as np
from typing import Union

class DataSet(AnnotableArtefact):
    
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, 
                  reference:Union[DataFlowDefinition, DataStructureDefinition] = None):
        
        super(DataSet, self).__init__(annotations = annotations)
    
        self.data = data
        self.reference = reference

    @property
    def data(self):
        return self._data
        
    @property
    def reference(self):
        return self._reference

    @property
    def referenceType(self):
        return type(self.reference)

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

    
class GenericDataSet(DataSet):
        
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, dsd = None):
        
        super(GenericDataSet, self).__init__(annotations = annotations, data = data, dsd = dsd)

    def toXml(self, action:str = "Replace",  dimensionAtObservation = "AllDimensions"):
        """
          
        """

        #1. Create root tag
        root = etree.Element(utils.qName("mes", "DataSet"))
        root.attrib["action"] = "Replace"
        root.attrib["structureRef"] = self.reference.id
        root.attrib["validFromDate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        #2. Convert the data to a list of JSON objects
        dataList = self.data.replace({np.nan:None}).to_dict('records')

        #3. For each data point
        for d in dataList:
            #3.1 Create the root elemens
            series = etree.Element(utils.qName("gen", "Series"))
            seriesKey = etree.Element(utils.qName("gen", "SeriesKey"))
            att = etree.Element(utils.qName("gen", "Attributes"))
            obs = etree.Element(utils.qName("gen", "Obs"))
            obsKey = etree.Element(utils.qName("gen", "ObsKey"))
            obsVal = etree.Element(utils.qName("gen", "ObsValue"))
            
            #3.2 For each key-value pair
            for k in d:

                #3.2.1 Create genric:Value tag if the value is not None
                if d[k] is not None:
                    value = etree.Element(utils.qName("gen", "Value"), attrib={"id":k, "value":str(d[k])})
                else:
                    value = None

                #.3.2.2 If the key-value corresponds to a dimension
                if k in self.reference.dimensionCodes:
                    #3.2.2.1 Raise error if the value is None, because dimensions need to have a value
                    if value is None:
                        raise ValueError(f"The dimension {k} has an empty value")
                    
                    #3.2.2.2 Attach the dimension to the right tag depending on the dimensionAtObservation
                    if dimensionAtObservation == "AllDimensions":
                        obsKey.append(value)
                    elif k == dimensionAtObservation:
                        value = etree.Element(utils.qName("gen", "ObsDimension"), attrib={"value":d[k]})
                        obs.append(value)
                    else:
                        seriesKey.append(value)

                #3.2.3 If the key-value corresponds to an attribute
                if k in self.reference.attributeCodes: 
                    if value is not None:
                        att.append(value)
                
                #3.2.4 If the key-value corresponds to the primary measure
                elif k == self.reference.measureCode:
                    #3.2.4.1 Attach it depending on the dimensionAtObservation
                    if dimensionAtObservation == "AllDimensions":
                        obsVal = etree.Element(utils.qName("gen", "ObsValue"), attrib={"value":d[k]})
                    else:    
                        value = etree.Element(utils.qName("gen", "ObsValue"), attrib={"id":k, "value":d[k]})
                        obs.append(value)
            
            #3.3 Depending on dimension at observation ...

                #3.3.1 If dimensionAtObservation is None (All dimensions)
            if dimensionAtObservation == "AllDimensions":
                obs.append(obsKey)
                obs.append(obsVal)
                obs.append(att)

                root.append(obs)
                
                #3.3.2 If the dimensionAtObervation has a value:
            else:
                series.append(seriesKey)
                series.append(obs)
                series.append(att)

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
                  data: pd.DataFrame = None, reference = None):
        
        super(StructureSpecificDataSet, self).__init__(annotations = annotations, data = data, 
                                                        reference = reference)

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

        #2. Convert the data to a list of JSON objects
        dataList = self.data.replace({np.nan:None}).to_dict('records')


        #3. For each data point
        for d in dataList:
        
            # obs = etree.Element(utils.qName("data", "Obs"))
            # series = etree.Element(utils.qName("data", "Series"))
            
            obs = etree.Element("Obs")
            series = etree.Element("Series")

            if dimensionAtObservation == "AllDimensions": 
                for k in d:
                    if k in self.reference.dimensionCodes:
                        if d[k] is None:
                            raise ValueError(f"The dimension {k} has an empty value")
                    
                
                    if d[k] is not None:
                        obs.attrib[k] = d[k]

                    root.append(obs)

            else:
                pass
            #     for k in d:
            #         if k == dimensionAtObservation or k == "OBS_VALUE" or k in self.dsd.attributes:
            #             obs.attrib[k] = d[k]
            #         else:
            #             series

            #         #3.2.2.2 Attach the dimension to the right tag depending on the dimensionAtObservation
            #         if dimensionAtObservation == "AllDimensions":
            #             obsKey.append(value)
            #         elif k == dimensionAtObservation:
            #             value = etree.Element(utils.qName("gen", "ObsDimension"), attrib={"value":d[k]})
            #             obs.append(value)
            #         else:
            #             seriesKey.append(value)

            #     #3.2.3 If the key-value corresponds to an attribute
            #     if k in self.dsd.attributeCodes: 
            #         if value is not None:
            #             att.append(value)
                
            #     #3.2.4 If the key-value corresponds to the primary measure
            #     elif k == self.dsd.measureCode:
            #         #3.2.4.1 Attach it depending on the dimensionAtObservation
            #         if dimensionAtObservation == "AllDimensions":
            #             obsVal = etree.Element(utils.qName("gen", "ObsValue"), attrib={"value":d[k]})
            #         else:    
            #             value = etree.Element(utils.qName("gen", "ObsValue"), attrib={"id":k, "value":d[k]})
            #             obs.append(value)
            
            # #3.3 Depending on dimension at observation ...

            #     #3.3.1 If dimensionAtObservation is None (All dimensions)
            # if dimensionAtObservation == "AllDimensions":
            #     obs.append(obsKey)
            #     obs.append(obsVal)
            #     obs.append(att)

            #     root.append(obs)
                
            #     #3.3.2 If the dimensionAtObervation has a value:
            # else:
            #     series.append(seriesKey)
            #     series.append(obs)
            #     series.append(att)

            #     root.append(series)                

        return root


    def toGenericDataSet(self):
        return GenericDataSet(
            annotations = self.annotations,
            data = self.data,
            reference = self.reference
        )