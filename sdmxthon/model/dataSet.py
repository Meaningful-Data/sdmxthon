"""
    DataSet file contains only the class DataSet, used for external assets
    to perform any validation or conversion to different formats.
"""

import json
from datetime import date, datetime

import pandas as pd
from pandas import DataFrame

from SDMXThon.parsers.data_validations import validate_data
from SDMXThon.parsers.write import writer
from SDMXThon.utils.enums import MessageTypeEnum
from .component import DataStructureDefinition, DataFlowDefinition


class DataSet:
    """ An organised collection of data.

    :param structure: Associates the DataStructureDefinition to the DataSet
    :type structure: class:`DataStructureDefinition`

    :param describedBy: Associates the DataFlowDefinition to the Dataset
    :type describedBy: class:`DataFlowDefinition`

    :param dataset_attributes: Contains all the attributes from the DataSet class of the Information Model
    :type dataset_attributes: dict

    :param attached_attributes:  Contains all the attributes at a Dataset level
    :type attached_attributes: dict

    :param data: Any object compatible with pandas.DataFrame()
    :type data: `Pandas Dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
    """

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
        """Associates the DataFlowDefinition to the Dataset

        :class: `DataFlowDefinition`

        """
        return self._dataflow

    @describedBy.setter
    def describedBy(self, value):
        if isinstance(value, DataFlowDefinition):
            self._dataflow = value
        else:
            raise TypeError('describedBy must be a DataFlowDefinition')

    @property
    def structure(self):
        """Associates the DataStructureDefinition to the DataSet

        :class: `DataStructureDefinition`

        """
        return self._structure

    @structure.setter
    def structure(self, value):
        if isinstance(value, DataStructureDefinition):
            self._structure = value
        else:
            raise TypeError('structure must be a DataStructureDefinition')

    @property
    def datasetAttributes(self):
        """Contains all the attributes from the DataSet class of the `Information Model
        <https://sdmx.org/wp-content/uploads/SDMX_2-1-1_SECTION_2_InformationModel_201108.pdf#page=85>`_

        :class: dict

        """
        return self._dataset_attributes

    @datasetAttributes.setter
    def datasetAttributes(self, value):
        self._dataset_attributes = value

    @property
    def attachedAttributes(self):
        """Contains all the attributes at a Dataset level with NoSpecifiedRelationship"""
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
        """Loads the data from a CSVCheck the
        `Pandas read_csv docs <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html>`_

        :param pathToCSV: Path to CSV file
        :type pathToCSV: str

        """
        self._data = pd.read_csv(pathToCSV)

    def readJSON(self, pathToJSON: str, orient: str = 'records'):
        """Loads the data from a JSON with orientation as records. Check the
        `Pandas read_json docs <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html>`_

        :param pathToJSON: Path to JSON file
        :type pathToJSON: str

        :param orient: Orientation of the file
        :type orient: str
        """
        self._data = pd.read_json(pathToJSON, orient=orient)

    def readExcel(self, pathToExcel: str):
        """Loads the data from a Excel file. Check the
        `Pandas read_excel docs <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html>`_

        :param pathToExcel: Path to Excel file
        :type pathToExcel: str
        """
        self._data = pd.read_excel(pathToExcel)

    def toCSV(self, pathToCSV: str = None):
        """Parses the data to a CSV file with comma separation and no header or index

        :param pathToCSV: Path to save as CSV file
        :type pathToCSV: str

        """
        return self.data.to_csv(pathToCSV, sep=',', encoding='utf-8', index=False, header=True)

    def toJSON(self, pathToJSON: str = None):
        """Parses the data using the JSON Specification from the library documentation

        :param pathToJSON: Path to save as JSON file
        :type pathToJSON: str

        """

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

    def toFeather(self, pathToFeather: str):
        """Parses the data to an Apache Feather format

        :param pathToFeather: Path to Feather file
        :type pathToFeather: str

        """
        self.data.to_feather(pathToFeather)

    def semanticValidation(self):
        """Performs a Semantic Validation on the Data.

        :returns:
            A list of errors as defined in the Validation Page.

        """
        if isinstance(self.data, DataFrame):
            return validate_data(self.data, self.structure)
        else:
            raise ValueError('Data for dataset %s is not well formed' % self.structure.id)

    def setDimensionAtObservation(self, dimAtObs):
        """Sets the dimensionAtObservation
            :param dimAtObs: Dimension At Observation
            :type dimAtObs: str
        """
        if dimAtObs in self.structure.dimensionCodes or dimAtObs == 'AllDimensions':
            self.datasetAttributes['dimensionAtObservation'] = dimAtObs
        else:
            raise ValueError('%s is not a dimension of dataset %s' % (dimAtObs, self.structure.id))

    def check_DA_keys(self, attributes: dict, setID: str):
        """Inputs default values to the dataset_attributes in case they are missing

        :param attributes: A dictionary with dataset_attributes
        :type attributes: dict
        
        :param setID: Provides an identification of the data set.
        :type setID: str
        """
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
                    attributes[k] = setID
                elif k == "dimensionAtObservation":
                    attributes[k] = "AllDimensions"
                else:
                    attributes[k] = None

        self._dataset_attributes = attributes.copy()

    def toXML(self, message_type: MessageTypeEnum = MessageTypeEnum.StructureDataSet, outputPath: str = '',
              id_: str = 'test',
              test: str = 'true',
              prepared: datetime = None,
              sender: str = 'Unknown',
              receiver: str = 'Not_supplied',
              prettyprint=True):
        """Parses the data to SDMX-ML 2.1, specifying the Message_Type (StructureSpecific or Generic or Metadata)

        :param message_type: Format of the Message in SDMX-ML
        :type message_type: MessageTypeEnum

        :param outputPath: Path to save the file, defaults to ''
        :type outputPath: str

        :param id_: ID of the Header, defaults to 'test'
        :type id_: str

        :param test: Mark as test file, defaults to 'true'
        :type test: str

        :param prepared: Datetime of the preparation of the Message, defaults to current date and time
        :type prepared: datetime

        :param sender: ID of the Sender, defaults to 'Unknown'
        :type sender: str

        :param receiver: ID of the Receiver, defaults to 'Not_supplied'
        :type receiver: str

        :param prettyprint: Saves the file formatted to be human readable
        :type prettyprint: bool

        :returns:
            StringIO object, if outputPath is ''
        """

        if prepared is None:
            prepared = datetime.now()

        if outputPath == '':
            return writer(path=outputPath, dType=message_type, payload=self, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver)
        else:
            writer(path=outputPath, dType=message_type, payload=self, id_=id_, test=test,
                   prepared=prepared, sender=sender, receiver=receiver, prettyprint=prettyprint)