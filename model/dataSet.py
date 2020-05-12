from lxml import etree
import pandas as pd
from datetime import datetime
from model.base import AnnotableArtefact
import utils
import numpy as np

class DataSet(AnnotableArtefact):
    
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, dsd = None):
        
        super(DataSet, self).__init__(annotations = annotations)
    
        self.data = data
        self.dsd = dsd

    @property
    def data(self):
        return self._data
        
    @data.setter 
    def data(self, value):
        if isinstance(value, pd.DataFrame):
            self._data = value
        else:
            raise TypeError("Data has to be provided as a pandas DataFrame")


    def toXml(self, action:str = "Replace"):
        root = etree.Element(utils.qName("mes", "DataSet"))
        root.attrib["action"] = "Replace"
        root.attrib["structureRef"] = self.dsd.id
        root.attrib["validFromDate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        return root

class GenericDataSet(DataSet):
        
    def __init__(self,  annotations = [],
                  data: pd.DataFrame = None, dsd = None):
        
        super(GenericDataSet, self).__init__(annotations = annotations, data = data, dsd = dsd)

    def toXml(self, action:str = "Replace", compact = False, dimensionObservation = None):
        """
            If compact is True, the value of dimensionAtObservation is disregarded
            If dimensionObservation is None, AllDimensions is used
        """
        #TODO: Compact is not working


        #1. Get root tag from he Dataset class
        root = super().toXml(action)
        


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

            compactObs = etree.Element("Obs")
            
            #3.2 For each key-value pair
            for k in d:
                #3.2.1 For comppact messages
                if compact:

                    compactObs.attrib[k] = str(d[k])
                #3.2.2 For non compact messages
                else:  
                    #3.2.2.1 Create genric:Value tag if the value is not None
                    if d[k] is not None:
                        value = etree.Element(utils.qName("gen", "Value"), attrib={"id":k, "value":str(d[k])})
                    else:
                        value = None

                    #.3.2.2.2 If the key-value corresponds to a dimension
                    if k in self.dsd.dimensionCodes:
                        #3.2.2.2.1 Raise error if the value is None, because dimensions need to have a value
                        if value is None:
                            raise ValueError(f"The dimension {k} has an empty value")
                        
                        #3.2.2.2.2 Attach the dimension to the right tag depending on the dimensionAtObservation
                        if dimensionObservation is None:
                            obsKey.append(value)
                        elif k == dimensionObservation:
                            value = etree.Element(utils.qName("gen", "ObsDimension"), attrib={"id":k, "value":d[k]})
                            obs.append(value)
                        else:
                            seriesKey.append(value)

                    #3.2.2.3 If the key-value corresponds to an attribute
                    if k in self.dsd.attributeCodes: 
                        if value is not None:
                            att.append(value)
                    
                    #3.2.2.4 If the key-value corresponds to the primary measure
                    elif k == self.dsd.measureCode:
                        #3.2.2.4.1 Attach it depending on the dimensionAtObservation
                        if dimensionObservation is None:
                            obsVal = etree.Element(utils.qName("gen", "ObsValue"), attrib={"value":d[k]})
                        else:    
                            value = etree.Element(utils.qName("gen", "ObsValue"), attrib={"id":k, "value":d[k]})
                            obs.append(value)
            
            #3.3 Depending on comcpact and dimension at observation is...
                #3.3.1 If it is compact
            if compact:
                root.append(compactObs)

                #3.3.2 If dimensionObservation is None (All dimensions)
            elif dimensionObservation is None:
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