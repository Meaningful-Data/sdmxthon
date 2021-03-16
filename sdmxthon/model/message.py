"""
    Message file contains the Message class for the use of external assets
"""

from datetime import datetime

# from .component import DataStructureDefinition
from .dataSet import DataSet
from ..model.header import Party, Sender
from ..parsers.message_parsers import Header
# from ..parsers.read import getMetadata
from ..parsers.write import writer
from ..utils.enums import MessageTypeEnum


class Message:
    """ Message class.

           Class that withholds the type of a SDMX Message, its information and its header

            Attributes:
                message_type: Enumeration that withholds the Message type for writing purposes
                payload: Information stored in the message (Datasets or structures)
                header: Header of the message.

    """
    subclass = None
    superclass = None

    def __init__(self, message_type: MessageTypeEnum = MessageTypeEnum.GenericDataSet, payload=None,
                 header: Header = None):
        self._type = message_type
        self._payload = payload
        if header is None:
            header = Header()

            header.id_('test')
            header.test(True)
            header.prepared(datetime.now())

            sender = Sender()
            sender.id_('Unknown')

            receiver = Party()
            receiver.id_('Not_supplied')

            header.sender(sender)
            header.receiver[0] = receiver

        self._header = header

    @property
    def type(self):
        """Enumeration that withholds the Message type for writing purposes"""
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def payload(self):
        """Information stored in the message (Datasets or structures)"""
        if self._payload is None:
            raise ValueError('No Payload found')
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @property
    def header(self):
        """Header of the message."""
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    def setDimensionAtObservation(self, dimAtObs):
        """Sets the dimensionAtObservation in the Datasets"""
        for e in self.payload.values():
            if isinstance(e, DataSet):
                e.setDimensionAtObservation(dimAtObs)

    def headerCreation(self, id_: str, test: bool = False,
                       senderId: str = "Unknown", receiverId: str = "not_supplied",
                       datetimeStr=''):
        """Creates the header for a Message"""
        header = Header()

        header.id_(id_)
        header.test(header.gds_format_boolean(test))
        if datetimeStr == '':
            header.prepared(datetime.now())
        else:
            header.prepared(header.gds_parse_datetime(datetimeStr))

        sender = Sender()
        sender.id_(senderId)

        receiver = Party()
        receiver.id_(receiverId)

        header.sender(sender)
        header.receiver(receiver)

        self._header = header

    def validate(self):
        """Performs the semantic validation if the Payload is all Datasets"""
        validations = {}
        if all(isinstance(n, DataSet) for n in self.payload.values()):
            for e in self.payload.values():
                list_errors = e.semanticValidation()
                if len(list_errors) > 0:
                    validations[e.structure.id] = list_errors
            if len(validations) is 0:
                return None
            else:
                return validations

        else:
            # TODO Validate Metadata
            raise ValueError('Wrong Payload')

    '''
    def readJSON(self, pathToJSON, pathToMetadata):
        """Reads the content of a JSON compliant with the JSON Specification of the library"""
        datasets = {}

        if isinstance(pathToMetadata, dict):
            if all(isinstance(n, DataStructureDefinition) for n in pathToMetadata.values()):
                dsds = pathToMetadata
            else:
                raise ValueError('pathToMetadata must be a DataStructureDefinition dict or a string')
        else:
            dsds, error = getMetadata(pathToMetadata)
        if isinstance(pathToJSON, str):
            with open(pathToJSON, 'r') as f:
                parsed = json.loads(f.read())
        else:
            parsed = json.loads(pathToJSON.read())
        for e in parsed:
            code = e.get('structureRef').get('code')
            version = e.get('structureRef').get('version')
            agency_id = e.get('structureRef').get('agencyID')
            dsdid = f"{agency_id}:{code}({version})"
            if dsdid not in dsds.keys():
                raise ValueError('Could not find any dsd matching to DSDID: %s' % dsdid)
            datasets[code] = DataSet(structure=dsds[dsdid],
                                     dataset_attributes=e.get('dataset_attributes'),
                                     attached_attributes=e.get('attached_attributes'),
                                     data=e.get('data'))
        self.payload = datasets
    '''
    def toXML(self, outputPath='', id_='test',
              test='true',
              prepared=datetime.now(),
              sender='Unknown',
              receiver='Not_supplied'):
        """Exports its payload to a XML file in SDMX-ML 2.1 format"""
        if outputPath == '':
            return writer(path=outputPath, dType=self.type, payload=self.payload, id_=id_, test=test,
                          prepared=prepared, sender=sender, receiver=receiver)
        else:
            writer(path=outputPath, dType=self.type, payload=self.payload, id_=id_, test=test,
                   prepared=prepared, sender=sender, receiver=receiver)
