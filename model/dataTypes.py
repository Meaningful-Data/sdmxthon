"""
    Adapted from PandasSDMX
"""

from enum import Enum


ActionType = Enum('ActionType', 'delete replace append information', type=str)

UsageStatus = Enum('UsageStatus', 'mandatory conditional')

# NB three diagrams in the spec show this enumeration containing
#    'gregorianYearMonth' but not 'gregorianYear' or 'gregorianMonth'. The
#    table in §3.6.3.3 Representation Constructs does the opposite. One ESTAT
#    query (via SGR) shows a real-world usage of 'gregorianYear'; while one NB
#    query shows usage of 'gregorianYearMonth'; so all three are included.
FacetValueType = Enum(
    'FacetValueType',
    """string bigInteger integer long short decimal float double boolean uri
    count inclusiveValueRange alpha alphaNumeric numeric exclusiveValueRange
    incremental observationalTimePeriod standardTimePeriod basicTimePeriod
    gregorianTimePeriod gregorianYear gregorianMonth gregorianYearMonth
    gregorianDay reportingTimePeriod reportingYear reportingSemester
    reportingTrimester reportingQuarter reportingMonth reportingWeek
    reportingDay dateTime timesRange month monthDay day time duration keyValues
    identifiableReference dataSetReference Xhtml""")

ConstraintRoleType = Enum('ConstraintRoleType', 'allowableContent actualContent')

FacetType = Enum("FacetType", """isSequence minLength maxLength minValue maxValue 
                                startValue endValue interval timeInterval decimals 
                                pattern startTime endTime""" )
