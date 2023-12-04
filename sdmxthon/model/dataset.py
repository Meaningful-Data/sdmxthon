"""
    DataSet file contains only the class DataSet, used for external assets
    to perform any validation or conversion to different formats.
"""

import json
from copy import copy
from datetime import date, datetime

import pandas as pd
from pandas import DataFrame

from sdmxthon.model.definitions import DataFlowDefinition, \
    DataStructureDefinition
from sdmxthon.model.header import Header
from sdmxthon.parsers.data_validations import validate_data
from sdmxthon.parsers.write import writer
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import split_unique_id
from sdmxthon.webservices.fmr import validate_sdmx_csv_fmr


class Dataset:
    """ An organised collection of data.

    :param structure: Associates the DataStructureDefinition to the DataSet
    :type structure: class:`DataStructureDefinition`

    :param dataflow: Associates the DataFlowDefinition to the Dataset
    :type dataflow: class:`DataFlowDefinition`

    :param dataset_attributes: Contains all the attributes from the DataSet \
    class of the Information Model
    :type dataset_attributes: dict

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
                 attached_attributes: dict = None,
                 data=None,
                 unique_id: str = None,
                 structure_type: str = None):

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
        if structure is not None:
            self._dataflow = None
            self.structure = structure
            if structure_type is not None:
                raise Exception("Cannot define data structure and "
                                "structure type at the same time")
            if unique_id is not None:
                raise Exception("Cannot define data structure and "
                                "full_id at the same time")
        elif dataflow is not None:
            if structure_type is not None:
                raise Exception("Cannot define dataflow and "
                                "structure type at the same time")
            if unique_id is not None:
                raise Exception("Cannot define dataflow and "
                                "full_id at the same time")
            self.dataflow = dataflow
        elif structure_type is not None:
            self._structure_type = structure_type
            if unique_id is None:
                raise Exception("Cannot define structure type and "
                                "not define full_id")
            self.unique_id = unique_id
            self.gather_metadata()
        else:
            raise ValueError('A Dataset must have a structure or a dataflow')

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

        return '<DataSet - No Structure found>'

    def __unicode__(self):
        if self.structure is not None:
            return f'<DataSet  - {self.structure.id}>'

        return '<DataSet - No Structure found>'

    def __repr__(self):
        if self.structure is not None:
            return f'<DataSet  - {self.structure.id}>'

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
                self._structure_type = "dataflow"
                self._unique_id = value.unique_id
        else:
            raise TypeError('dataflow must be a DataFlowDefinition')

    @property
    def structure(self) -> DataStructureDefinition:
        """Associates the DataStructureDefinition to the DataSet

        :class: `DataStructureDefinition`

        """
        if self._structure is None and self.dataflow is not None:
            return self.dataflow.structure
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
            self._structure_type = "structure"
            self._unique_id = value.unique_id
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
                        if len(temp) > 0:
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

    @property
    def unique_id(self):
        """Extracts the unique_id"""
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value):
        # Check if the value is similar to BIS:BIS_DER(1.0)
        if not isinstance(value, str):
            raise TypeError('unique_id must be a string')
        if not value.count(':') == 1 and value.count('(') == 1 and \
                value.count(')') == 1:
            raise ValueError('unique_id must be in the format '
                             'agency:dataset(version)')
        # Check if the agency is not empty
        if value.split(':')[0] == '':
            raise ValueError('unique_id must contain an agency')
        self._unique_id = value

    @property
    def structure_type(self):
        """Extracts the structure_type"""
        return self._structure_type

    def read_csv(self, path_to_csv: str, **kwargs):
        """Loads the data from a CSV. Check the `Pandas read_csv docs
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas
        .read_csv.html>`_ Kwargs are supported

        :param path_to_csv: Path to CSV file
        :type path_to_csv: str

        """
        self._data = pd.read_csv(path_to_csv, **kwargs)

    def read_json(self, path_to_json: str, **kwargs):
        """Loads the data from a JSON. Check the
        `Pandas read_json docs
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas
        .read_json.html>`_. Kwargs are supported

        :param path_to_json: Path to JSON file
        :type path_to_json: str
        """
        self._data = pd.read_json(path_to_json, **kwargs)

    def read_excel(self, path_to_excel: str, **kwargs):
        """Loads the data from an Excel file. Check the `Pandas read_excel
        docs <https://pandas.pydata.org/pandas-docs/stable/reference/api
        /pandas.read_excel.html>`_. Kwargs are supported

        :param path_to_excel: Path to Excel file
        :type path_to_excel: str
        """
        self._data = pd.read_excel(path_to_excel, **kwargs)

    def to_csv(self, path_to_csv: str = None, **kwargs):
        """Parses the data to a CSV file. Kwargs are supported

        :param path_to_csv: Path to save as CSV file
        :type path_to_csv: str

        """
        return self.data.to_csv(path_to_csv, **kwargs)

    def to_json(self, path_to_json: str = None):
        """Parses the data using the JSON Specification from the library
        documentation

        :param path_to_json: Path to save as JSON file
        :type path_to_json: str

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
        if path_to_json is None:
            return element
        with open(path_to_json, 'w') as f:
            f.write(json.dumps(element, ensure_ascii=False, indent=2))

    def to_feather(self, path_to_feather: str, **kwargs):
        """Parses the data to an Apache Feather format. Kwargs are supported.

        :param path_to_feather: Path to Feather file
        :type path_to_feather: str

        """
        self.data.to_feather(path_to_feather, **kwargs)

    def structural_validation(self):
        """Performs a Structural Validation on the Data.

        :returns:
            A list of errors as defined in the Validation Page.

        """
        if self.data is None:
            raise ValueError('The dataset should contain data to perform '
                             'a structural validation')
        elif self.structure is None:
            raise ValueError('The dataset should contain a structure to '
                             'perform a structural validation')

        if not isinstance(self.data, DataFrame):
            raise ValueError(f'Data for dataset {self.structure.id} '
                             f'is not well formed')
        elif not isinstance(self.structure, DataStructureDefinition):
            raise TypeError('structure must be a DataStructureDefinition')

        return validate_data(self.data, self.structure)

    def to_sdmx_csv(self, version: int, output_path: str = None):

        """
        Converts a dataset to an SDMX CSV format

        :param version: The SDMX-CSV version (1.2)
        :param output_path: The path where the resulting
                            SDMX CSV file will be saved

        :return: The SDMX CSV data as a string if no output path is provided

        .. important::

            The SDMX CSV version must be 1 or 2. Please refer to this link
            for more info:
            https://wiki.sdmxcloud.org/SDMX-CSV

            Uses pandas.Dataframe.to_csv with specific parameters to ensure
            the file is compatible with the SDMX-CSV standard (e.g. no index,
            uses header, comma delimiter, custom column names
            for the first two columns)
        """

        # Link to pandas.to_csv documentation on sphinx:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

        # Create a copy of the dataset
        df: pd.DataFrame = copy(self.data)

        # Add additional attributes to the dataset
        for k, v in self.attached_attributes.items():
            df[k] = v

        if version == 1:
            df.insert(0, 'DATAFLOW', self._unique_id)

        elif version == 2:
            # Insert two columns at the beginning of the data set
            df.insert(0, 'STRUCTURE', self._structure_type)
            df.insert(1, 'STRUCTURE_ID', self._unique_id)
        else:
            raise Exception('Invalid SDMX-CSV version.')

        # Convert the dataset into a csv file
        if output_path is not None:
            # Save the CSV file to the specified output path
            df.to_csv(output_path, index=False, header=True)

        # Return the SDMX CSV data as a string
        return df.to_csv(index=False, header=True)

    def fmr_validation(self, host: str = 'localhost',
                       port: int = 8080,
                       use_https: bool = False,
                       delimiter: str = 'comma',
                       max_retries: int = 10,
                       interval_time: float = 0.5
                       ):

        """
        Uploads data to FMR and performs validation

        :param host: The FMR instance host (default is 'localhost')
        :type host: str

        :param port: The FMR instance port (default is 8080)
        :type port: int

        :param use_https: A boolean indicating whether to use HTTPS
                          (default is False)
        :type use_https: bool

        :param delimiter: The delimiter used in the CSV file
                          (options: 'comma', 'semicolon', 'tab', 'space')
        :type delimiter: str

        :param max_retries: The maximum number of retries for checking
                            validation status (default is 10)
        :type max_retries: int

        :param interval_time: The interval time between retries in seconds
                              (default is 0.5)
        :type interval_time: int

        :return: The validation status if successful
        """
        csv_text = self.to_sdmx_csv()

        return validate_sdmx_csv_fmr(csv_text=csv_text,
                                     host=host,
                                     port=port,
                                     use_https=use_https,
                                     delimiter=delimiter,
                                     max_retries=max_retries,
                                     interval_time=interval_time)

    def set_dimension_at_observation(self, dim_at_obs):
        """Sets the dimensionAtObservation
            :param dim_at_obs: Dimension At Observation
            :type dim_at_obs: str
        """
        if (dim_at_obs in self.structure.dimension_codes or
                dim_at_obs == 'AllDimensions'):
            self.dataset_attributes['dimensionAtObservation'] = dim_at_obs
        else:
            raise ValueError(f'{dim_at_obs} is not a dimension '
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
               output_path: str = '',
               message_type: MessageTypeEnum =
               MessageTypeEnum.StructureSpecificDataSet,
               header: Header = None,
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

        :param output_path: Path to save the file, defaults to ''
        :type output_path: str

        :param prettyprint: Saves the file formatted to be human-readable
        :type prettyprint: bool

        :param header: Header to be written, defaults to None
        :type header: Header

        .. important::

            If the header argument is not None, rest of the below arguments
            will not be used

        :param id_: ID of the Header, defaults to 'test'
        :type id_: str

        :param test: Mark as test file, defaults to 'true'
        :type test: str

        :param prepared: Datetime of the preparation of the Message, \
        defaults to current date and time
        :type prepared: datetime

        :param sender: ID of the Sender, defaults to 'Unknown'
        :type sender: str

        :param receiver: ID of the Receiver, defaults to 'Not_supplied'
        :type receiver: str

        :returns: StringIO object, if outputPath is ''
        """

        if prepared is None:
            prepared = datetime.now()

        if output_path == '':
            return writer(path=output_path, type_=message_type, payload=self,
                          id_=id_, test=test, header=header,
                          prepared=prepared, sender=sender, receiver=receiver)
        writer(path=output_path, type_=message_type, payload=self, id_=id_,
               test=test, header=header,
               prepared=prepared, sender=sender, receiver=receiver,
               prettyprint=prettyprint)

    def gather_metadata(self, unique_id=None, structure_type=None):
        if unique_id is None:
            unique_id = self.unique_id
        else:
            self.unique_id = unique_id
        if structure_type is None:
            structure_type = self.structure_type
        else:
            if structure_type not in ['structure', 'dataflow']:
                raise ValueError('structure_type must be structure or '
                                 'dataflow')
            self._structure_type = structure_type

        agency, id_, version = split_unique_id(unique_id)
        from sdmxthon.webservices.webservices import get_supported_web_services
        ws_mapper = get_supported_web_services()
        if agency not in ws_mapper:
            return
