import json
from datetime import datetime

from lxml import etree

from SDMXThon.model.structure import DataStructureDefinition
from .dataSet import DataSet
from ..message.generic import GenericDataHeaderType, StructureSpecificDataHeaderType, \
    GenericTimeSeriesDataHeaderType, StructureSpecificTimeSeriesDataHeaderType, SenderType, PartyType
from ..utils.creators import id_creator, DataSetCreator
from ..utils.enums import DatasetType


class Message:
    subclass = None
    superclass = None

    def __init__(self, message_type: DatasetType = DatasetType.GenericDataSet, payload: dict = None,
                 header: [GenericDataHeaderType, GenericTimeSeriesDataHeaderType,
                          StructureSpecificDataHeaderType, StructureSpecificTimeSeriesDataHeaderType] = None):
        self._type = message_type
        if payload is None:
            self._payload = {}
        else:
            if all(isinstance(n, DataSet) for n in payload.values()):
                self._payload = payload
        if header is None:
            if self.type == DatasetType.GenericDataSet:
                header = GenericDataHeaderType()
            elif self.type == DatasetType.StructureDataSet:
                header = StructureSpecificDataHeaderType()
            elif self.type == DatasetType.GenericTimeSeriesDataSet:
                header = GenericTimeSeriesDataHeaderType()
            elif self.type == DatasetType.StructureTimeSeriesDataSet:
                header = StructureSpecificTimeSeriesDataHeaderType()
            else:
                raise ValueError('Invalid Dataset type')

            header.set_ID('test')
            header.set_Test(True)
            header.set_Prepared(datetime.now())

            sender = SenderType()
            sender.set_id('Unknown')

            receiver = PartyType()
            receiver.set_id('Not supplied')

            header.set_Sender(sender)
            header.add_Receiver(receiver)

        self._header = header

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def payload(self):
        if self._payload is None:
            raise ValueError('No Payload found')
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    def setDimensionAtObservation(self, dimAtObs):
        for e in self.payload.values():
            e.setDimensionAtObservation(dimAtObs)

    def headerCreation(self, id_: str, test: bool = False,
                       senderId: str = "Unknown", receiverId: str = "not_supplied",
                       datetimeStr=''):
        if self.type == DatasetType.GenericDataSet:
            header = GenericDataHeaderType()
        elif self.type == DatasetType.StructureDataSet:
            header = StructureSpecificDataHeaderType()
        elif self.type == DatasetType.GenericTimeSeriesDataSet:
            header = GenericTimeSeriesDataHeaderType()
        elif self.type == DatasetType.StructureTimeSeriesDataSet:
            header = StructureSpecificTimeSeriesDataHeaderType()
        else:
            raise ValueError('Invalid Dataset type')

        header.set_ID(id_)
        header.set_Test(header.gds_format_boolean(test))
        if datetimeStr == '':
            header.set_Prepared(datetime.now())
        else:
            header.set_Prepared(header.gds_parse_datetime(datetimeStr))

        sender = SenderType()
        sender.set_id(senderId)

        receiver = PartyType()
        receiver.set_id(receiverId)

        header.set_Sender(sender)
        header.add_Receiver(receiver)

        self._header = header

    def validate(self):
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

    def readJSON(self, pathToJSON, pathToMetadata):
        from SDMXThon.utils.parsers import get_codelist_model, get_concept_schemes, get_DSDs
        datasets = {}

        if isinstance(pathToMetadata, str):
            root = etree.parse(pathToMetadata)

            codelists = get_codelist_model(root)
            concepts = get_concept_schemes(root, codelists)
            dsds = get_DSDs(root, concepts, codelists)
        elif isinstance(pathToMetadata, dict):
            if all(isinstance(n, DataStructureDefinition) for n in pathToMetadata.values()):
                dsds = pathToMetadata
            else:
                raise ValueError('pathToMetadata must be a DataStructureDefinition dict or a string')
        else:
            raise ValueError('pathToMetadata must be a DataStructureDefinition dict or a string')
        if isinstance(pathToJSON, str):
            with open(pathToJSON, 'r') as f:
                parsed = json.loads(f.read())
        else:
            parsed = json.loads(pathToJSON.read())
        for e in parsed:
            code = e.get('structureRef').get('code')
            version = e.get('structureRef').get('version')
            agencyID = e.get('structureRef').get('agencyID')
            dsdid = id_creator(agencyID, code, version)
            if dsdid not in dsds.keys():
                raise ValueError('Could not find any dsd matching to DSDID: %s' % dsdid)
            datasets[e.code] = DataSetCreator(dsd=dsds[dsdid],
                                              dataset_attributes=e.get('dataset_attributes'),
                                              attached_attributes=e.get('attached_attributes'),
                                              obs=e.get('obs'))
        self.payload = datasets
