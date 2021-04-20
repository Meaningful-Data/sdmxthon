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
from .component_list import DataStructureDefinition, DataFlowDefinition


class Dataset:
    """ An organised collection of data.

    :param structure: Associates the DataStructureDefinition to the DataSet
    :type structure: class:`DataStructureDefinition`

    :param dataflow: Associates the DataFlowDefinition to the Dataset
    :type dataflow: class:`DataFlowDefinition`

    :param dataset_attributes: Contains all the attributes from the DataSet
    class of the Information Model :type dataset_attributes: dict

    :param attached_attributes:  Contains all the attributes at a Dataset level
    :type attached_attributes: dict

    :param data: Any object compatible with pandas.DataFrame()
    :type data: `Pandas Dataframe \
    <https://pandas.pydata.org/pandas-docs/stable \
    /reference/api/pandas.DataFrame.html>`_
    """

    def __init__(self, structure: DataStructureDefinition = None,
                 dataflow: DataFlowDefinition = None,
                 dataset_attributes: dict = None,
                 attached_attributes: dict = None, data=None):

        self._dataset_attributes = {}

        self.data = None
        self._dataflow = None
        self._structure = None
        self.attached_attributes = {}

        if attached_attributes is not None:
            self.attached_attributes = attached_attributes.copy()

        if structure is not None and dataflow is not None:
            raise ValueError('A Dataset cannot have a structure '
                             'and a dataflow, use only one')
        elif structure is not None:
            self._dataflow = None
            self.structure = structure
        elif dataflow is not None:
            self.dataflow = dataflow

        if data is not None:
            if isinstance(data, pd.DataFrame):
                self.data = data.copy()
            else:
                self.data = pd.DataFrame(data)

        if dataset_attributes is None:
            self._check_DA_keys({})
        else:
            self._check_DA_keys(dataset_attributes)

    def __str__(self):
        if self.structure is not None:
            return f'<DataSet  - {self.structure.id}>'
        else:
            return '<DataSet - No Structure found>'

    def __unicode__(self):
        if self.structure is not None:
            return f'<DataSet  - {self.structure.id}>'
        else:
            return '<DataSet - No Structure found>'

    def __repr__(self):
        if self.structure is not None:
            return f'<DataSet  - {self.structure.id}>'
        else:
            return '<DataSet - No Structure found>'

    @property
    def dataflow(self) -> DataFlowDefinition:
        """Associates the DataFlowDefinition to the Dataset

        :class: `DataFlowDefinition`

        """
        return self._dataflow

    @dataflow.setter
    def dataflow(self, value: DataFlowDefinition):
        if isinstance(value, DataFlowDefinition) or value is None:
            self._dataflow = value
            if value is not None:
                if len(self.attached_attributes) > 0:
                    attached_attributes = self.attached_attributes.copy()
                    for k in attached_attributes.keys():
                        if k not in value.structure.dataset_attribute_codes:
                            del self._attached_attributes[k]

                    for k in value.structure.dataset_attribute_codes:
                        if k not in attached_attributes.keys():
                            raise ValueError(f'Missing attribute {k} '
                                             f'at a dataset level '
                                             f'(attached_attributes)')

                if ('OBS_VALUE' in self._data.columns and
                        value.structure.measure_code != 'OBS_VALUE'):
                    self._data = self._data.rename(
                        {'OBS_VALUE': value.structure.measure_code})
                self.dataset_attributes['setId'] = value.id
                self._structure = value
                self._structure = value.structure
        else:
            raise TypeError('dataflow must be a DataFlowDefinition')

    @property
    def structure(self) -> DataStructureDefinition:
        """Associates the DataStructureDefinition to the DataSet

        :class: `DataStructureDefinition`

        """
        return self._structure

    @structure.setter
    def structure(self, value: DataStructureDefinition):
        if not isinstance(value,
                          DataStructureDefinition) and value is not None:
            raise TypeError('structure must be a DataStructureDefinition')

        if self._dataflow is not None and value is not None:
            raise ValueError('dataflow property is not None')

        if value is not None:
            if len(self.attached_attributes) > 0:
                attached_attributes = self.attached_attributes.copy()
                for k in attached_attributes.keys():
                    if k not in value.dataset_attribute_codes:
                        del self._attached_attributes[k]

                for k in value.dataset_attribute_codes:
                    if k not in attached_attributes.keys():
                        raise ValueError(f'Missing attribute {k} at a '
                                         f'dataset level '
                                         f'(attached_attributes)')

            if ('OBS_VALUE' in self._data.columns and
                    value.measure_code != 'OBS_VALUE'):
                self._data = self._data.rename(
                    {'OBS_VALUE': value.measure_code})
            self.dataset_attributes['setId'] = value.id
        self._structure = value

    @property
    def dataset_attributes(self) -> dict:
        """Contains all the attributes from the DataSet class of the
        `Information Model <https://sdmx.org/wp-content/uploads/SDMX_2-1
        -1_SECTION_2_InformationModel_201108.pdf#page=85>`_

        :class: dict

        """
        return self._dataset_attributes

    @dataset_attributes.setter
    def dataset_attributes(self, value: dict):
        self._check_DA_keys(value)

    @property
    def attached_attributes(self) -> dict:
        """Contains all the attributes at a Dataset level with
        NoSpecifiedRelationship """
        return self._attached_attributes

    @attached_attributes.setter
    def attached_attributes(self, value: dict):
        if self.structure is not None:
            temp = value.copy()
            for k in temp.keys():
                if k not in self.structure.dataset_attribute_codes:
                    raise ValueError(f'{k} not in the attributes at dataset '
                                     f'level for DSD '
                                     f'{self.structure.unique_id}')

        self._attached_attributes = value

    @property
    def data(self) -> pd.DataFrame:
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
            if self._structure is not None:
                for e in self.structure.dataset_attribute_codes:
                    if e in temp.keys():
                        attached_attributes[e] = temp.loc[0, e]
                        del temp[e]

            self._data = temp
            if len(attached_attributes) > 0:
                for k, v in attached_attributes.items():
                    self.attached_attributes[k] = str(v)

    @property
    def dim_at_obs(self):
        """Extracts the dimensionAtObservation from the dataset_attributes"""
        return self.dataset_attributes.get('dimensionAtObservation')

    def read_csv(self, pathToCSV: str):
        """Loads the data from a CSVCheck the `Pandas read_csv docs
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas
        .read_csv.html>`_

        :param pathToCSV: Path to CSV file
        :type pathToCSV: str

        """
        self._data = pd.read_csv(pathToCSV)

    def read_json(self, pathToJSON: str, orient: str = 'records'):
        """Loads the data from a JSON with orientation as records. Check the
        `Pandas read_json docs
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas
        .read_json.html>`_

        :param pathToJSON: Path to JSON file
        :type pathToJSON: str

        :param orient: Orientation of the file
        :type orient: str
        """
        self._data = pd.read_json(pathToJSON, orient=orient)

    def read_excel(self, pathToExcel: str):
        """Loads the data from a Excel file. Check the `Pandas read_excel
        docs <https://pandas.pydata.org/pandas-docs/stable/reference/api
        /pandas.read_excel.html>`_

        :param pathToExcel: Path to Excel file
        :type pathToExcel: str
        """
        self._data = pd.read_excel(pathToExcel)

    def to_csv(self, pathToCSV: str = None):
        """Parses the data to a CSV file with comma separation and no header
        or index

        :param pathToCSV: Path to save as CSV file
        :type pathToCSV: str

        """
        return self.data.to_csv(pathToCSV, sep=',', encoding='utf-8',
                                index=False, header=True)

    def to_json(self, pathToJSON: str = None):
        """Parses the data using the JSON Specification from the library
        documentation

        :param pathToJSON: Path to save as JSON file
        :type pathToJSON: str

        """

        element = {'structureRef': {"code": self.structure.id,
                                    "version": self.structure.version,
                                    "agencyID": self.structure.agencyID}}
        if len(self.dataset_attributes) > 0:
            element['dataset_attributes'] = self.dataset_attributes

        if len(self.attached_attributes) > 0:
            element['attached_attributes'] = self.attached_attributes

        result = self.data.to_json(orient="records")
        element['data'] = json.loads(result).copy()
        if pathToJSON is None:
            return element
        else:
            with open(pathToJSON, 'w') as f:
                f.write(json.dumps(element, ensure_ascii=False, indent=2))

    def to_feather(self, pathToFeather: str):
        """Parses the data to an Apache Feather format

        :param pathToFeather: Path to Feather file
        :type pathToFeather: str

        """
        self.data.to_feather(pathToFeather)

    def semantic_validation(self):
        """Performs a Semantic Validation on the Data.

        :returns:
            A list of errors as defined in the Validation Page.

        """
        if isinstance(self.data, DataFrame):
            return validate_data(self.data, self.structure)
        else:
            raise ValueError(
                'Data for dataset %s is not well formed' % self.structure.id)

    def set_dimension_at_observation(self, dimAtObs):
        """Sets the dimensionAtObservation
            :param dimAtObs: Dimension At Observation
            :type dimAtObs: str
        """
        if (dimAtObs in self.structure.dimension_codes or
                dimAtObs == 'AllDimensions'):
            self.dataset_attributes['dimensionAtObservation'] = dimAtObs
        else:
            raise ValueError(f'{dimAtObs} is not a dimension '
                             f'of dataset {self.structure.id}')

    def _check_DA_keys(self, attributes: dict):
        """Inputs default values to the dataset_attributes in case they are
        missing

        :param attributes: A dictionary with dataset_attributes
        :type attributes: dict
        """
        keys = ["reportingBegin", "reportingEnd", "dataExtractionDate",
                "validFrom", "validTo", "publicationYear",
                "publicationPeriod", "action", "setId",
                "dimensionAtObservation"]

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
                    if self.structure is not None:
                        attributes[k] = self.structure.id
                    elif self.dataflow is not None:
                        attributes[k] = self.dataflow.structure.id
                elif k == "dimensionAtObservation":
                    attributes[k] = "AllDimensions"
                else:
                    attributes[k] = None

        self._dataset_attributes = attributes.copy()

    def to_xml(self,
               message_type: MessageTypeEnum =
               MessageTypeEnum.StructureDataSet,
               outputPath: str = '',
               id_: str = 'test',
               test: str = 'true',
               prepared: datetime = None,
               sender: str = 'Unknown',
               receiver: str = 'Not_supplied',
               prettyprint=True):
        """Parses the data to SDMX-ML 2.1, specifying the Message_Type
        (StructureSpecific or Generic or Metadata)

        :param message_type: Format of the Message in SDMX-ML
        :type message_type: MessageTypeEnum

        :param outputPath: Path to save the file, defaults to ''
        :type outputPath: str

        :param id_: ID of the Header, defaults to 'test'
        :type id_: str

        :param test: Mark as test file, defaults to 'true'
        :type test: str

        :param prepared: Datetime of the preparation of the Message,
        defaults to current date and time
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
            return writer(path=outputPath, dType=message_type, payload=self,
                          id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver)
        else:
            writer(path=outputPath, dType=message_type, payload=self, id_=id_,
                   test=test,
                   prepared=prepared, sender=sender, receiver=receiver,
                   prettyprint=prettyprint)
