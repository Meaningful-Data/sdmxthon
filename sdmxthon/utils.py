from datetime import datetime
from lxml import etree
import warnings
import re
from typing import List, Dict

#
# Convienence setters and getters
#

def setDateFromString(value: str, format_:str = "%Y-%m-%dT%H:%M:%S"):
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

def stringSetter(value: str, pattern: str = None, enumeration:List[str] = None):
    """Generic function validating strings for setters

    Checks that the input is a string or integer.
    If it is a string, and a pattern is passed, checks that the pattern
    is respected.

    Args:
        value: The value to be validated.
        pattern: A regex pattern to be validated
        enumeration: A list with valid strings

    Returns:
        The validated string

    Raises:
        ValueError: If the value violates any of the conditions.
    """
    
    if isinstance(value, str):
        if pattern is not None:
            regex = re.compile(pattern, re.I)
            if regex.match(value):
                return value
            else:
                raise ValueError(f"Error setting the string. Pattern '{pattern}' not respected")
        elif enumeration is not None:
            if value in enumeration:
                return value
            else:
                raise ValueError(f"Error setting the string. Enumeration {str(enumeration)} not respected")
        else:
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
    elif isinstance(value, str):
        return setDateFromString(value)
    else:
        raise TypeError("Type should be datetime or date")

def boolSetter(value: bool):
    if isinstance(value, bool) or value is None:
        return value
    elif value == "false":
        return False
    elif value == "true":
        return True
    else:
        raise ValueError("Type should be bool")

def genericSetter(value, clss):
    if isinstance(value, clss) or value is None:
        return value
    else:
        raise TypeError(f"The value has to be an instance of the {clss.__name__} class. {type(value)} passed")
    
def addToMessage(value, requiredClass, container):
    if isinstance(value, requiredClass):
        if value.urn in container:
            warnings.warn(f"The {requiredClass.__name__} {value.urn} already exists in the message")
        else:
            container[value.urn] = value
    else:
        raise ValueError(f"Object of {requiredClass.__name__} Class required. {type(value)} received")

def intSetter(value: int):
    if isinstance(value, int) or value is None:
        return value
    else:
        try:
            return int(value)
        except:
            raise ValueError("Type shoudl be int")


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
    return etree.QName(NS[ns], name)

#
#Bool mapper
#

boolMapper = {
    "true": True,
    "false": False,
    None: None
}

#
#Get international strings
#

def getNameAndDescription(elem: etree.Element):
    from sdmxthon.model.base import InternationalString
    
    #1. Get Names
    nameElems = elem.findall(qName("com", "Name"))
    name = InternationalString.fromXml(nameElems)

    #2. Get descriptions
    descriptionElems = elem.findall(qName("com", "Description"))
    description = InternationalString.fromXml(descriptionElems)

    return name, description

#
#Get references
#

def getReferences(elem):
    if elem is None:
        return None
    else: 
        ref = elem.find("Ref")
        if ref is None:
            raise TypeError("The file contains a reference without Ref tag")

        
        
        return {
            "id_" : ref.get("id"), 
            "version" : ref.get("version"), 
            "agencyId" : ref.get("agencyID"),
            "maintainableParentId" : ref.get("maintainableParentID"),
            "package" : ref.get("package"),
            "maintainableParentVersion" : ref.get("maintainableParentVersion")
            }

def lxmlElementsEqual(e1, e2):
    """
        Checks if two lxml Elements are equal, in the sense that they have the same tag, attributes...
    """
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all(lxmlElementsEqual(c1, c2) for c1, c2 in zip(e1, e2))