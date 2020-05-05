from datetime import datetime
from lxml.etree import QName
import warnings

#
# Convienence setters and getters
#

def setDateFromString(value: str, format_:str = "%Y-%m-%d"):
    try:
        dt = datetime.strptime(value, format_)
    except:
        raise ValueError(f"Wrong date string format. The format {format_} should be followed. {str(value)} passed")

    return dt

def getDateString(date: str,  format_: str = "%Y-%m-%d"):
    if date is None:
        return ""
    else:
        return datetime.strftime(date, format_)

def stringSetter(value: str):
    if isinstance(value, str):
        return value
    elif isinstance(value, int):
        return str(value) 
    elif value is None:
        return None
    else:
        raise ValueError(f"Type should be a string, {type(value)} passed")

def dateSetter(value: datetime):
    if isinstance(value, datetime) or value is None:
        return value
    else:
        raise TypeError("Type should be datetime or date")

def boolSetter(value: bool):
    if isinstance(value, bool) or value is None:
        return bool(value)
    elif value == "false":
        return False
    elif value == "true":
        return True
    else:
        raise ValueError("Type should be bool")

def addToMessage(value, requiredClass, container):
    if isinstance(value, requiredClass):
        if value.urn in container:
            warnings.warn(f"The {requiredClass.__name__} {value.urn} already exists in the message")
        else:
            container[value.urn] = value
    else:
        raise ValueError(f"Object of {requiredClass.__name__} Class required. {type(value)} received")

#
# Qnames manager
#

_base_ns = 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1'
NS = {
    'com': f'{_base_ns}/common',
    'data': f'{_base_ns}/data/structurespecific',
    'str': f'{_base_ns}/structure',
    'mes': f'{_base_ns}/message',
    'gen': f'{_base_ns}/data/generic',
    'footer': f'{_base_ns}/message/footer',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    }


def qName(ns, name):
    """Return a fully-qualified tag *name* in namespace *ns*."""
    return QName(NS[ns], name)

#
#Bool mapper
#

boolMapper = {
    "true": True,
    "false": False,
    None: None
}