from lxml import etree
import pandas as pd
from datetime import datetime

class DataSet():
    def __init__(self, structure=None):
        self.data=None
        self.structure=structure

    @property
    def data(self):
        return self._data
        
    @property
    def obsDimension(self):
        return self.structure["dimensionAtObservation"] if self.structure is not None and "dimensionAtObservation"in self.structure.keys() else None
    @property
    def id(self):
        return self.structure["id"]

    @data.setter 
    def data(self, value):
        if value is None:
            pass
        elif type(value)==list:
            self._data=value
        else:
            raise TypeError("Data has to be provided as a list of datapoints")

    def toXml(self):
        root=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}DataSet")
        root.attrib["action"]="Replace"
        root.attrib["structureRef"]=self.structure["id"]
        root.attrib["validFromDate"]=datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        for d in self.data:
            series=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series")
            key=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}SeriesKey")
            att=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes")
            obs=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs")
            
            for k in d:
                if d[k] is not None:
                    value=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Value", attrib={"id":k, "value":d[k]})

                if k in ["unit", "decimals", "startDate", "unitRef"]:
                    att.append(value)
                elif k=="OBS_VALUE":
                    value=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue", attrib={"id":k, "value":d[k]})
                    obs.append(value)
                elif k==self.obsDimension:
                    value=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension", attrib={"id":k, "value":d[k]})
                    obs.append(value)

                else:
                    key.append(value)
            
            series.append(key)
            series.append(att)
            series.append(obs)

            root.append(series)

        return root


    # def __init__(self, dataSetElement=None, dimensionAtObservation=None):
    #     self._dataDict=[]
    #     self._data=None

    #     if dataSetElement is None:
    #         pass
    #     elif type(dataSetElement)==etree._Element:
    #         self._parse(dataSetElement, dimensionAtObservation)
    #     else:
    #         raise ValueError("The input has to be an lxml etree element")

    # def _parse(self, dataSetElement, dimensionAtObservation):
    #     rslt=[]
    #     series=dataSetElement
        
    #     for s in dataSetElement.findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series"):
    #         preObsRslt={}
    #         for i in s.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}SeriesKey").findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Value"):
    #             preObsRslt[i.get("id")]=i.get("value")
    #         for i in s.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes").findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Value"):
    #             preObsRslt[i.get("id")]=i.get("value")

    #         for i in s.findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs"):
    #             obs=preObsRslt
    #             obs[dimensionAtObservation]=i.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension").get("value")
    #             obs["OBS_VALUE"]=i.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue").get("value") 
    #             for a in s.findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Attributes"):
    #                 att=a.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Value")
    #                 obs[att.get("id")]=att.get("value")
                
    #             rslt.append(obs)
    #     self._dataDict=rslt
    #     self._data=pd.DataFrame.from_dict(self.dataDict)

    # @property
    # def dataDict(self):
    #     return self._dataDict
    # @property
    # def data(self):
    #     return self._data