from enum import Enum


class MessageTypeEnum(Enum):
    """
    Enumeration that withholds the Message type for writing purposes.
    """
    GenericDataSet = 'GenAll'
    StructureSpecificDataSet = 'StrSpecificAll'
    GenericTimeSeriesDataSet = 'GenTimeSeries'
    StructureSpecificTimeSeriesDataSet = 'StrSpecificTimeSeries'
    Metadata = 'Structures'
    Error = 'Error'
    Submission = 'Submission'
