"""
    Message file contains the Message class for the use of external assets
"""
from datetime import datetime
from io import StringIO

from SDMXthon.parsers.message_parsers import Header
from SDMXthon.parsers.write import writer
from SDMXthon.utils.enums import MessageTypeEnum
from .dataSet import DataSet
from .header import Party, Sender


class Message:
    """ Message class holds the type of a SDMX Message, its payload and its header.

    :param message_type: Enumeration that withholds the Message type for writing purposes
    :type message_type: `MessageTypeEnum`

    :param payload: Information stored in the message (Datasets or structures)
    :type payload: :doc:`Dataset<./dataset>`

    :param header: Header of the message.
    :type header: `Header`
    """

    def __init__(self, message_type: MessageTypeEnum, payload, header: Header):
        self._type = message_type
        self._payload = payload
        if header is None:
            self.headerCreation(id_='test')
        else:
            self._header = header

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
        """Information stored in the message (DataSet or Structure). A dictionary of datasets could also be used.

        :class: :doc:`Dataset<./dataset>`
        :class: `Dict [str, Dataset]`
        :class: `Structure`

        """
        if self._payload is None:
            raise ValueError('No Payload found')
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @property
    def header(self):
        """Header of the message.

        :class: `Header`

        """
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    def setDimensionAtObservation(self, dimAtObs):
        """Sets the dimensionAtObservation if the payload is formed by Datasets

        :param dimAtObs: Dimension At Observation
        :type dimAtObs: str

        """
        for e in self.payload.values():
            if isinstance(e, DataSet):
                e.setDimensionAtObservation(dimAtObs)

    def headerCreation(self, id_: str, test: bool = False,
                       senderId: str = "Unknown", receiverId: str = "not_supplied",
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

            :param datetimeStr: Datetime of the preparation of the Message. Format:  '%Y-%m-%dT%H:%M:%S'
            :type datetimeStr: datetime
        """
        header = Header()

        header.id_(id_)
        header.test(header._gds_format_boolean(test))
        if datetimeStr == '':
            header.prepared(datetime.now())
        else:
            header.prepared(header._gds_parse_datetime(datetimeStr))

        sender = Sender()
        sender.id_(senderId)

        receiver = Party()
        receiver.id_(receiverId)

        header.sender(sender)
        header.receiver(receiver)

        self._header = header

    def validate(self):
        """Performs the semantic validation if the Payload is all Datasets

        :raises:
            TypeError: if the payload is not a DataSet or a dict of DataSets
        """
        validations = {}
        if isinstance(self.payload, dict) and all(isinstance(n, DataSet) for n in self.payload.values()):
            for e in self.payload.values():
                list_errors = e.semanticValidation()
                if len(list_errors) > 0:
                    validations[e.structure.id] = list_errors
            if len(validations) is 0:
                return None
            else:
                return validations
        elif isinstance(self.payload, DataSet):
            return self.payload.semanticValidation()
        else:
            # TODO Validate Metadata
            raise TypeError('Wrong Payload. Must be of type DataSet or a dict of DataSet')

    def toXML(self, outputPath: str = '', id_: str = 'test',
              test: str = 'true',
              prepared: datetime = None,
              sender: str = 'Unknown',
              receiver: str = 'Not_supplied') -> StringIO:
        """Exports its payload to a XML file in SDMX-ML 2.1 format

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

        :returns:
            StringIO object, if outputPath is ''

        """

        if prepared is None:
            prepared = datetime.now()

        if outputPath == '':
            return writer(path=outputPath, dType=self.type, payload=self.payload, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver)
        else:
            writer(path=outputPath, dType=self.type, payload=self.payload, id_=id_, test=test,
                   prepared=prepared, sender=sender, receiver=receiver)


if __name__ == '__main__':
    print('Don´t do that!!')
