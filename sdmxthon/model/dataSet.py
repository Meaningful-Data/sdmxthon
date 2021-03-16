"""
    DataSet file contains only the class DataSet, used for external assets
    to perform any validation or conversion to different formats.
"""

import json
from datetime import date, datetime

import pandas as pd
from pandas import DataFrame

from ..model.component import DataStructureDefinition, DataFlowDefinition
from ..parsers.data_validations import validate_data
from ..parsers.write import writer
from ..utils.enums import MessageTypeEnum


class DataSet:
    """ DataSet class.

           An organised collection of data.

           Attributes:
               structure: Associates the DataStructureDefinition to the DataSet
               describedBy: Associates the DataFlowDefinition to the Dataset
               dataset_attributes: Contains all the attributes from the DataSet class of the Information Model
               attached_attributes: Contains all the attributes at a Dataset level
               data: Pandas DataFrame that withholds all the data


    """

    subclass = None
    superclass = None

    def __init__(self, structure: DataStructureDefinition, describedBy: DataFlowDefinition = None,
                 dataset_attributes: dict = None, attached_attributes: dict = None, data=None):

        self._structure = structure
        self._dataflow = describedBy

        self._dataset_attributes = {}

        if dataset_attributes is None:
            self.check_DA_keys({}, structure.id)
        else:
            self.check_DA_keys(dataset_attributes, structure.id)

        if attached_attributes is None:
            self._attached_attributes = {}
        else:
            self._attached_attributes = attached_attributes.copy()

        if data is None:
            self._data = pd.DataFrame()
        else:
            if isinstance(data, pd.DataFrame):
                self.data = data.copy()
            else:
                self.data = pd.DataFrame(data)

    def __str__(self):
        return '<DataSet  - %s>' % self.structure.id

    def __unicode__(self):
        return '<DataSet  - %s>' % self.structure.id

    def __repr__(self):
        return '<DataSet  - %s>' % self.structure.id

    @property
    def describedBy(self):
        """Associates the DataFlowDefinition to the Dataset"""
        return self._dataflow

    @describedBy.setter
    def describedBy(self, value):
        if isinstance(value, DataFlowDefinition):
            self._dataflow = value
        else:
            raise TypeError('describedBy must be a DataFlowDefinition')

    @property
    def structure(self):
        """Associates the DataStructureDefinition to the DataSet"""
        return self._structure

    @structure.setter
    def structure(self, value):
        if isinstance(value, DataStructureDefinition):
            self._structure = value
        else:
            raise TypeError('structure must be a DataStructureDefinition')

    @property
    def datasetAttributes(self):
        """Contains all the attributes from the DataSet class of the Information Model"""
        return self._dataset_attributes

    @datasetAttributes.setter
    def datasetAttributes(self, value):
        self._dataset_attributes = value

    @property
    def attachedAttributes(self):
        """Contains all the attributes at a Dataset level"""
        return self._attached_attributes

    @attachedAttributes.setter
    def attachedAttributes(self, value):
        self._attached_attributes = value

    @property
    def data(self):
        """Pandas DataFrame that withholds all the data"""
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            self._data = pd.DataFrame()
        else:
            if isinstance(value, pd.DataFrame):
                temp = value.copy()
            else:
                temp = pd.DataFrame(value)
            attached_attributes = {}
            for e in self.structure.datasetAttributeCodes:
                if e in temp.keys():
                    attached_attributes[e] = temp.loc[0, e]
                    del temp[e]

            self._data = temp
            if len(attached_attributes) > 0:
                for k, v in attached_attributes.items():
                    self.attachedAttributes[k] = str(v)

    @property
    def dimAtObs(self):
        """Extracts the dimensionAtObservation from the dataset_attributes"""
        return self.datasetAttributes.get('dimensionAtObservation')

    def readCSV(self, pathToCSV: str):
        """Loads the data from a CSV"""
        self._data = pd.read_csv(pathToCSV)

    def readJSON(self, pathToJSON: str):
        """Loads the data from a JSON with orientation as records.
        Check the Pandas read_json documentation for more details"""
        self._data = pd.read_json(pathToJSON, orient='records')

    def readExcel(self, pathToExcel: str):
        """Loads the data from a Excel file"""
        self._data = pd.read_excel(pathToExcel)

    def toCSV(self, pathToCSV: str = None):
        """Parses the data to a CSV file with comma separation and no header or index"""
        return self.data.to_csv(pathToCSV, sep=',', encoding='utf-8', index=False, header=True)

    def toJSON(self, pathToJSON: str = None):
        """Parses the data using the JSON Specification from the library documentation"""

        element = {'structureRef': {"code": self.structure.id, "version": self.structure.version,
                                    "agencyID": self.structure.agencyID}}
        if len(self.datasetAttributes) > 0:
            element['dataset_attributes'] = self.datasetAttributes

        if len(self.attachedAttributes) > 0:
            element['attached_attributes'] = self.attachedAttributes

        result = self.data.to_json(orient="records")
        element['data'] = json.loads(result).copy()
        if pathToJSON is None:
            return element
        else:
            with open(pathToJSON, 'w') as f:
                f.write(json.dumps(element, ensure_ascii=False, indent=2))

    def toFeather(self, pathToFeather):
        """Parses the data to an Apache Feather format"""
        self.data.to_feather(pathToFeather)

    def semanticValidation(self):
        """Performs a Semantic Validation on the Data"""
        if isinstance(self.data, DataFrame):
            return validate_data(self.data, self.structure)
        else:
            raise ValueError('Data for dataset %s is not well formed' % self.structure.id)

    def setDimensionAtObservation(self, dimAtObs):
        """Sets the dimensionAtObservation"""
        if dimAtObs in self.structure.dimensionCodes:
            self.datasetAttributes['dimensionAtObservation'] = dimAtObs
        elif dimAtObs == 'AllDimensions':
            self.datasetAttributes['dimensionAtObservation'] = dimAtObs
        else:
            raise ValueError('%s is not a dimension of dataset %s' % (dimAtObs, self.structure.id))

    def check_DA_keys(self, attributes, code):
        """Inputs default values to the dataset_attributes in case they are missing"""
        keys = ["reportingBegin", "reportingEnd", "dataExtractionDate", "validFrom", "validTo", "publicationYear",
                "publicationPeriod", "action", "setId", "dimensionAtObservation"]

        for spared_key in attributes.keys():
            if spared_key not in keys:
                attributes.pop(spared_key)

        for k in keys:
            if k not in attributes.keys():
                if k == "dataExtractionDate":
                    attributes[k] = date.today()
                elif k == "action":
                    attributes[k] = "Replace"
                elif k == "setId":
                    attributes[k] = code
                elif k == "dimensionAtObservation":
                    attributes[k] = "AllDimensions"
                else:
                    attributes[k] = None

        self._dataset_attributes = attributes.copy()

    def toXML(self, message_type: MessageTypeEnum = MessageTypeEnum.GenericDataSet, outputPath='', id_='test',
              test='true',
              prepared=datetime.now(),
              sender='Unknown',
              receiver='Not_supplied',
              prettyprint=True):
        """Parses the data to SDMX-ML 2.1, specifying the Message_Type (StructureSpecific or Generic or Metadata)"""
        if outputPath == '':
            return writer(path=outputPath, dType=message_type, payload=self, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver)
        else:
            writer(path=outputPath, dType=message_type, payload=self, id_=id_, test=test,
                   prepared=prepared, sender=sender, receiver=receiver, prettyprint=prettyprint)
