from enum import Enum


class MessageTypeEnum(Enum):
    GenericDataSet = 'GenericDataSet'
    StructureDataSet = 'StructureDataSet'
    GenericTimeSeriesDataSet = 'GenericTimeSeriesDataSet'
    StructureTimeSeriesDataSet = 'StructureTimeSeriesDataSet'
    Metadata = 'Structures'
