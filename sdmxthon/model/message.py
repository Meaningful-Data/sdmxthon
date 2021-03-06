"""
    Message file contains the Message class for the use of external assets
"""
from datetime import datetime
from io import StringIO
from typing import Dict

from sdmxthon.model.dataset import Dataset
from sdmxthon.model.header import Party, Sender, Header
from sdmxthon.parsers.write import writer
from sdmxthon.utils.enums import MessageTypeEnum


class Message:
    """ Message class holds the type of a SDMX Message, its payload and its
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
                 payload: (Dict[str, dict], Dict[str, Dataset], Dataset),
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
        """Enumeration that withholds the Message type for writing purposes.

        :class: `MessageTypeEnum`

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

    @property
    def content(self):
        """Returns the payload as a dict

        :class: `Dict`

        """
        if isinstance(self.payload, dict):
            return self.payload
        if isinstance(self.payload, Dataset):
            return {'datasets': {self.payload.unique_id, self.payload}}

        return {'datasets': self.payload}

    @property
    def header(self):
        """Header of the message.

        :class: `Header`

        """
        return self._header

    @header.setter
    def header(self, value):

        self._header = value

    def set_dimension_at_observation(self, dimAtObs):
        """Sets the dimensionAtObservation if the payload is formed by Datasets

        :param dimAtObs: Dimension At Observation
        :type dimAtObs: str

        """
        for e in self.payload.values():
            if isinstance(e, Dataset):
                e.set_dimension_at_observation(dimAtObs)

    def header_creation(self, id_: str, test: bool = False,
                        senderId: str = "Unknown",
                        receiverId: str = "not_supplied",
                        datetimeStr=''):
        """
            Creates the header for a Message

            :param id_: ID of the Header
            :type id_: str

            :param test: Mark as test file
            :type test: bool

            :param senderId: ID of the Sender
            :type senderId: str

            :param receiverId: ID of the Receiver
            :type receiverId: str

            :param datetimeStr: Datetime of the preparation of the Message.
            :type datetimeStr: str Format:  '%Y-%m-%dT%H:%M:%S'
        """
        header = Header(ID=id_)
        header.test = test
        if datetimeStr == '':
            header.prepared = datetime.now()
        else:
            header.prepared = header._gds_parse_datetime(datetimeStr)

        sender = Sender()
        sender.id_ = senderId

        receiver = Party()
        receiver.id_ = receiverId

        header.sender = sender
        header.receiver = receiver

        self.header = header

    def validate(self):
        """Performs the semantic validation if the Payload is all Datasets

        :raises:
            TypeError: if the payload is not a DataSet or a dict of DataSets
        """
        validations = {}
        if (isinstance(self.payload, dict) and
                all(isinstance(n, Dataset) for n in self.payload.values())):
            for e in self.payload.values():
                list_errors = e.semantic_validation()
                if len(list_errors) > 0:
                    validations[e.structure.id] = list_errors
            if len(validations) == 0:
                return None

            return validations
        elif isinstance(self.payload, Dataset):
            return self.payload.semantic_validation()
        else:
            raise TypeError('Wrong Payload. Must be of type '
                            'DataSet or a dict of DataSet')

    def to_xml(self, outputPath: str = '',
               header: Header = None,
               id_: str = 'test',
               test: str = 'true',
               prepared: datetime = None,
               sender: str = 'Unknown',
               receiver: str = 'Not_supplied',
               prettyprint=True) -> StringIO:
        """Exports its payload to a XML file in SDMX-ML 2.1 format

        :param outputPath: Path to save the file, defaults to ''
        :type outputPath: str

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

        :returns:
            StringIO object, if outputPath is ''

        """

        if prepared is None:
            prepared = datetime.now()

        if outputPath == '':
            return writer(path=outputPath, type_=self.type,
                          payload=self.payload, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver,
                          header=header, prettyprint=prettyprint)
        writer(path=outputPath, type_=self.type, payload=self.payload,
               id_=id_, test=test, header=header,
               prepared=prepared, sender=sender, receiver=receiver,
               prettyprint=prettyprint)


if __name__ == '__main__':
    print('Don??t do that!!')
