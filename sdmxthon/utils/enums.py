from enum import Enum


class MessageTypeEnum(Enum):
    """
    Enumeration that withholds the Message type for writing purposes.
    """
    GenericDataSet = 'GenAll'
    StructureSpecificDataSet = 'StrSpecificAll'
    Metadata = 'Structures'
    Error = 'Error'
    Submission = 'Submission'


class ActionEnum(Enum):
    """
    Enumeration that withholds the Action type for the dataset
    """
    Append = 'append'
    Replace = 'replace'
    Delete = 'delete'
    Information = 'information'
