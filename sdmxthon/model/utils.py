"""
    Utils has some handling functions for the model module
"""

import re
from base64 import b64encode
from datetime import datetime
from typing import List

from sdmxthon.utils.enums import ActionEnum


#
# Convenience setters and getters
#

def set_date_from_string(value: str, format_: str = "%Y-%m-%dT%H:%M:%S"):
    """Generic function to format a string to datetime

    Args: value: The value to be validated.
    format_: A regex pattern to validate if the string has a specific format

    Returns:
        A datetime object

    Raises:
        ValueError: If the value violates the format constraint.
    """

    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if value[-1] == "Z":
        value = value[:-1]
    for fmt in (format_, "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    raise ValueError(f"Wrong date string format. The format {format_} "
                     f"should be followed. {str(value)} passed")


def get_date_string(date: datetime, format_: str = "%Y-%m-%d"):
    """Generic function to get a string from a datetime object

    Args:
        date: The value to be validated.
        format_: A regex pattern to return the string with

    Returns:
        A string formatted

    Raises:
        ValueError: If the value violates any of the conditions.
    """
    if date is None:
        return ""

    return datetime.strftime(date, format_)


def string_setter(value: str, pattern: str = None,
                  enumeration: List[str] = None):
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
            raise ValueError(f"Error setting the string. Pattern "
                             f"'{pattern}' not respected")
        elif enumeration is not None:
            if value in enumeration:
                return value
            raise ValueError(
                f"Error setting the string. Enumeration "
                f"{str(enumeration)} not respected")
        else:
            return value
    elif isinstance(value, int):
        return str(value)
    elif value is None:
        return None
    else:
        raise ValueError(f"Type should be a string, {type(value)} passed")


def date_setter(value: datetime):
    """Generic setter for datetime objects

    Args:
        value: The value to be validated.

    Raises:
        TypeError: If the value is not datetime or date
    """

    if isinstance(value, datetime) or value is None:
        return value
    if isinstance(value, str):
        return set_date_from_string(value)

    raise TypeError("Type should be datetime or date")


def bool_setter(value: bool):
    """Generic setter for bool objects

        Args:
            value: The value to be validated.

        Raises:
            TypeError: If the value is not bool
    """
    if isinstance(value, bool) or value is None:
        return value
    if value == "false":
        return False
    if value == "true":
        return True

    raise ValueError("Type should be bool")


def generic_setter(value, class_):
    """Generic setter for class objects

        Args:
            value: The value to be validated.
            class_: The class to validate with

        Raises:
            TypeError: If the value is not an instance of the class
    """
    if isinstance(value, class_) or value is None:
        return value

    raise TypeError(f"The value has to be an instance of the "
                    f"{class_.__name__} class. {type(value)} passed")


def int_setter(value: int):
    """Generic setter for integer objects

            Args:
                value: The value to be validated.

            Raises:
                TypeError: If the value is not an integer
        """

    if isinstance(value, int) or value is None:
        return value
    try:
        return int(value)
    except Exception:
        raise ValueError("Type should be int")


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

ACTION_SDMX_CSV_MAPPER = {
    ActionEnum.Append: 'A',
    ActionEnum.Replace: 'R',
    ActionEnum.Delete: 'D',
    ActionEnum.Information: 'I'
}

ACTION_SDMX_CSV_MAPPER_READING = {
    'A': ActionEnum.Append,
    'R': ActionEnum.Replace,
    'D': ActionEnum.Delete,
    'I': ActionEnum.Information
}

UsageStatus = ['UsageStatus', 'mandatory conditional']
FacetValueType = ['string', 'bigInteger', 'integer', 'long', 'short',
                  'decimal', 'float', 'double', 'boolean', 'uri',
                  'count', 'inclusiveValueRange', 'alpha', 'alphaNumeric',
                  'numeric', 'exclusiveValueRange',
                  'incremental', 'observationalTimePeriod',
                  'standardTimePeriod', 'basicTimePeriod',
                  'gregorianTimePeriod', 'gregorianYear', 'gregorianMonth',
                  'gregorianYearMonth',
                  'gregorianDay', 'reportingTimePeriod', 'reportingYear',
                  'reportingSemester',
                  'reportingTrimester', 'reportingQuarter', 'reportingMonth',
                  'reportingWeek',
                  'reportingDay', 'dateTime', 'timesRange', 'month',
                  'monthDay', 'day', 'time', 'duration', 'keyValues',
                  'identifiableReference', 'dataSetReference', 'Xhtml']
ConstraintRoleType = ['Allowed', 'Actual']
FacetType = ['isSequence', 'minLength', 'maxLength', 'minValue', 'maxValue',
             'startValue', 'endValue', 'interval', 'timeInterval', 'decimals',
             'pattern', 'startTime', 'endTime']

METADATA_ENDPOINT = '/ws/secure/sdmxapi/rest/'

STATUS_IN_PROCESS = ['Initialising', 'Analysing', 'Validating',
                     'Consolidating']

# The list of load status which means is an error
STATUS_ERRORS = ['IncorrectDSD', 'InvalidRef', 'MissingDSD',
                 'Error']

STATUS_COMPLETED = ["Complete"]


def generate_basic_auth_token(user, password):
    bytes_auth = bytes(f"{user}:{password}", 'utf-8')
    return 'Basic ' + b64encode(bytes_auth).decode('ascii')
