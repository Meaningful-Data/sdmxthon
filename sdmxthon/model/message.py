"""
    Message file contains the Message class for the use of external assets
"""
from datetime import datetime
from typing import Dict

from sdmxthon.model.dataset import Dataset
from sdmxthon.model.error import SDMXError
from sdmxthon.model.header import Header
from sdmxthon.model.submission import SubmissionResult
from sdmxthon.parsers.write import writer
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict
from sdmxthon.webservices.fmr import submit_structures_to_fmr


class Message:
    """ Message class holds the type of SDMX Message, its payload and its
    header.

    :param message_type: Enumeration that withholds the Message type for \
    writing purposes
    :type message_type: `MessageTypeEnum`

    :param payload: Information stored in the message (Datasets or structures)
    :type payload: :doc:`Dataset<./dataset>`

    :param header: Header of the message.
    :type header: `Header`
    """

    def __init__(self, message_type: MessageTypeEnum,
                 payload: (Dict[str, dict], Dict[str, Dataset], Dataset,
                           SDMXError, Dict[str, SubmissionResult]) = None,
                 header: Header = None):
        self._type = message_type
        self._payload = payload
        self._header = header

    def __eq__(self, other):
        if isinstance(other, Message):
            return (self.type == other.type and
                    self.payload == other.payload and
                    self.header == other.header)

    @property
    def type(self):
        """Holds the Message type for writing purposes (see :meth:`.to_xml`)

        :class:`.MessageTypeEnum`

        """
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def payload(self):
        """Information stored in the message (DataSet or Structure). A
        dictionary of datasets could also be used.

        :class: :doc:`Dataset<./dataset>`
        :class: `Dict [str, Dataset]`
        :class: `Structure`

        """
        if self._payload is None:
            raise ValueError('No Payload found')
        return self._payload

    @payload.setter
    def payload(self, value):
        if not isinstance(value, (dict, Dataset)):
            raise TypeError('Payload must be a DataSet, '
                            'a dict of DataSet or Metadata')
        self._payload = value

    def get_organisationschemes(self):
        """Returns the Organisation Schemes from content"""
        if isinstance(self.content, dict) and 'OrganisationSchemes' in self.content:
            organisationSchemes = self.content['OrganisationSchemes']
            if len(organisationSchemes) > 1:
                return organisationSchemes
            elif len(organisationSchemes) == 1:
                return first_element_dict(organisationSchemes)
        else:
            raise ValueError('No OrganisationScheme found')

    def get_organisationscheme_by_uid(self, unique_id):
        """Returns a specific Organisation Scheme from content"""

        if isinstance(self.content, dict) and 'OrganisationSchemes' in self.content:
            for os in self.content['OrganisationSchemes'].values():
                if os.unique_id == unique_id:
                    return os
            raise ValueError('That OrganisationScheme does not exist')
        else:
            raise ValueError('No OrganisationScheme found')

    def get_codelists(self):
        """Returns the Codelists from content"""
        if isinstance(self.content, dict) and 'Codelists' in self.content:
            codelists = self.content['Codelists']
            if len(codelists) > 1:
                return codelists
            elif len(codelists) == 1:
                return first_element_dict(codelists)
        else:
            raise ValueError('No Codelist found')

    def get_codelist_by_uid(self, unique_id):
        """Returns a specific Codelist from content"""

        if isinstance(self.content, dict) and 'Codelists' in self.content:
            for codelist in self.content['Codelists'].values():
                if codelist.unique_id == unique_id:
                    return codelist
            raise ValueError('That Codelist does not exist')
        else:
            raise ValueError('No Codelist found')

    def get_concepts(self):
        """Returns the Concepts from content"""
        if isinstance(self.content, dict) and 'Concepts' in self.content:
            concepts = self.content['Concepts']
            if len(concepts) > 1:
                return concepts
            elif len(concepts) == 1:
                return first_element_dict(concepts)
        else:
            raise ValueError('No Concept found')

    def get_concept_by_uid(self, unique_id):
        """Returns a specific Concept from content"""

        if isinstance(self.content, dict) and 'Concepts' in self.content:
            for concept in self.content['Concepts'].values():
                if concept.unique_id == unique_id:
                    return concept
            raise ValueError('That Concept does not exist')
        else:
            raise ValueError('No Concept found')

    def get_datastructures(self):
        """Returns the Data Structures from content"""

        if isinstance(self.content, dict) and 'DataStructures' in self.content:
            data_structures = self.content['DataStructures']
            if len(data_structures) > 1:
                return data_structures
            elif len(data_structures) == 1:
                return first_element_dict(data_structures)
        else:
            raise ValueError('No DataStructure found')

    def get_datastructure_by_uid(self, unique_id):
        """Returns a specific Data Structure from content"""

        if isinstance(self.content, dict) and 'DataStructures' in self.content:
            for data_structure in self.content['DataStructures'].values():
                if data_structure.unique_id == unique_id:
                    return data_structure
            raise ValueError('That DataStructure does not exist')
        else:
            raise ValueError('No DataStructure found')

    def get_dataflows(self):
        """Returns the Dataflows from content"""

        if isinstance(self.content, dict) and 'Dataflows' in self.content:
            dataflows = self.content['Dataflows']
            if len(dataflows) > 1:
                return dataflows
            elif len(dataflows) == 1:
                return first_element_dict(dataflows)
        else:
            raise ValueError('No Dataflow found')

    def get_dataflow_by_uid(self, unique_id):
        """Returns a specific Dataflow from content"""

        if isinstance(self.content, dict) and 'Dataflows' in self.content:
            for dataflow in self.content['Dataflows'].values():
                if dataflow.unique_id == unique_id:
                    return dataflow
            raise ValueError('That Dataflow does not exist')
        else:
            raise ValueError('No Dataflow found')

    def get_datasets(self):
        """Returns the Datasets from content"""

        if isinstance(self.content, Dataset):
            return self.content
        elif isinstance(self.content, dict):
            first_element = first_element_dict(self.content)
            if isinstance(first_element, Dataset):
                return self.content
            else:
                raise ValueError('No Dataset found')
        else:
            raise ValueError('Content must be a Dataset or dict')

    def get_dataset_by_uid(self, unique_id):
        """Returns a specific Dataset from content"""

        if isinstance(self.content, Dataset):
            if self.content.unique_id == unique_id:
                return self.content
            else:
                raise ValueError('That Dataset does not exist')
        elif isinstance(self.content, dict):
            for dataset in self.content.values():
                if dataset.unique_id == unique_id:
                    return dataset
            raise ValueError('That Dataset does not exist')
        else:
            raise ValueError('No Dataset found')

    @property
    def content(self):
        """
        Returns the payload as a dict

        :class: `Dict`

        """
        # TODO: Siempre diccionario
        if isinstance(self.payload, (dict, Dataset)):
            return self.payload
        if isinstance(self.payload, SDMXError):
            return {'Errors': self.payload}
        return self.payload



    @property
    def header(self):
        """Header of the message.

        :class: `Header`

        """
        return self._header

    @header.setter
    def header(self, value):

        self._header = value

    def set_dimension_at_observation(self, dim_at_obs):
        """Sets the dimensionAtObservation if the payload is formed by Datasets

        :param dim_at_obs: Dimension At Observation
        :type dim_at_obs: str

        """
        for e in self.payload.values():
            if isinstance(e, Dataset):
                e.set_dimension_at_observation(dim_at_obs)

    def validate(self):
        """Performs the semantic validation if the Payload is all Datasets

        :raises:
            TypeError: if the payload is not a DataSet or a dict of DataSets
        """
        validations = {}
        if (isinstance(self.payload, dict) and
                all(isinstance(n, Dataset) for n in self.payload.values())):
            for e in self.payload.values():
                e: Dataset
                list_errors = e.structural_validation()
                if len(list_errors) > 0:
                    validations[e.structure.id] = list_errors
            if len(validations) == 0:
                return None

            return validations
        elif isinstance(self.payload, Dataset):
            return self.payload.structural_validation()
        else:
            raise TypeError('Wrong Payload. Must be of type '
                            'DataSet or a dict of DataSet')

    def upload_to_fmr(self, host: str = 'localhost',
                      port: int = 8080,
                      user: str = 'root',
                      password: str = 'password',
                      use_https: bool = False):
        """
        Uploads the metadata to the FMR

        :param host: Host to be connected
        :type host: str
        :param port: Port to be used
        :type port: int
        :param user: Username for basic Auth (Admin or Agency privileges)
        :type user: str
        :param password: Password for basic Auth
        :type password: str
        :param use_https: Flag to use or not https
        :type use_https: bool

        """
        # Argument handling
        if self.type != MessageTypeEnum.Metadata:
            raise TypeError('Message type must be Metadata')
        sdmx_text = self.to_xml()
        submit_structures_to_fmr(
            sdmx_text=sdmx_text,
            host=host,
            port=port,
            user=user,
            password=password,
            use_https=use_https
        )

    def to_xml(self,
               output_path: str = '',
               header: Header = None,
               id_: str = 'test',
               test: str = 'true',
               prepared: datetime = None,
               sender: str = 'Unknown',
               receiver: str = 'Not_supplied',
               prettyprint=True) -> str:
        """Exports its payload to a XML file in SDMX-ML 2.1 format

        :param output_path: Path to save the file, defaults to ''
        :type output_path: str

        :param prettyprint: Specifies if the output file is formatted
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

        :returns: A str, if outputPath is ''

        """

        if prepared is None:
            prepared = datetime.now()

        if output_path == '':
            return writer(path=output_path, type_=self.type,
                          payload=self.payload, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver,
                          header=header, prettyprint=prettyprint)
        writer(path=output_path, type_=self.type, payload=self.payload,
               id_=id_, test=test, header=header,
               prepared=prepared, sender=sender, receiver=receiver,
               prettyprint=prettyprint)


if __name__ == '__main__':
    print('Don´t do that!!')
