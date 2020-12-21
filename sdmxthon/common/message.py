import json
from copy import copy
from datetime import datetime

from SDMXThon.model.structure import DataStructureDefinition
from .dataSet import DataSet, generateDataSetXML, get_structure_from_dsd
from ..message.generic import GenericDataType, StructureSpecificDataType, PartyType, SenderType, \
    StructureSpecificTimeSeriesDataHeaderType, GenericTimeSeriesDataHeaderType, StructureSpecificDataHeaderType, \
    GenericDataHeaderType
from ..utils.dataset_parsing import getMetadata
from ..utils.enums import DatasetType
from ..utils.metadata_parsers import id_creator
from ..utils.write import save_file


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
            receiver.set_id('Not_supplied')

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
        datasets = {}

        if isinstance(pathToMetadata, dict):
            if all(isinstance(n, DataStructureDefinition) for n in pathToMetadata.values()):
                dsds = pathToMetadata
            else:
                raise ValueError('pathToMetadata must be a DataStructureDefinition dict or a string')
        else:
            dsds = getMetadata(pathToMetadata)
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
            datasets[code] = DataSet(structure=dsds[dsdid],
                                     dataset_attributes=e.get('dataset_attributes'),
                                     attached_attributes=e.get('attached_attributes'),
                                     data=e.get('data'))
        self.payload = datasets

    def toXML(self, outputPath=''):
        if len(self.payload) == 0:
            raise ValueError('Datasets must be provided')

        structures = []

        header = copy(self.header)

        if self.type == DatasetType.GenericDataSet or self.type == DatasetType.GenericTimeSeriesDataSet:
            messageXML = GenericDataType()
        elif self.type == DatasetType.StructureDataSet or self.type == DatasetType.StructureTimeSeriesDataSet:
            messageXML = StructureSpecificDataType()
        else:
            raise ValueError('Wrong Dataset Type')
        for e in self.payload.values():
            data_set = generateDataSetXML(e, self.type)

            messageXML.add_DataSet(data_set)

            allDimensions = e.datasetAttributes.get('dimensionAtObservation') == 'AllDimensions'

            structure = get_structure_from_dsd(e.structure, e, self.type, allDimensions=allDimensions)

            structures.append(structure)
        header.set_Structure(structures)
        messageXML.set_Header(header)
        if messageXML == None:
            raise ValueError('Message could not be parsed')
        if outputPath == '':
            return save_file(messageXML, outputPath)
        else:
            save_file(messageXML, outputPath)
