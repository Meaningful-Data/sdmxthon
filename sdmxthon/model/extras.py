from datetime import datetime, date, timedelta
from typing import List

from .base import MaintainableArtefact, InternationalString
from .component import ComponentList, Component
from .timePeriods import ObservationalTimePeriod
from .utils import generic_setter, ConstraintRoleType
from ..parsers.data_generic import ComponentValueType
from ..parsers.data_parser import DataParser


class MemberValue(ComponentValueType):

    def __init__(self, value: str, cascadeValues: bool):
        super(ComponentValueType).__init__(value)
        self.value_ = value
        self.cascadeValue = cascadeValues

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        self._value = generic_setter(value, str)

    @property
    def cascadeValue(self):
        return self._cascadeValue

    @cascadeValue.setter
    def cascadeValue(self, value):
        self._cascadeValue = generic_setter(value, bool)


class Period:
    def __init__(self, isInclusive: bool, period: ObservationalTimePeriod):
        self.isInclusive = isInclusive
        self.period = period

    @property
    def isInclusive(self):
        return self._isInclusive

    @isInclusive.setter
    def isInclusive(self, value):
        self._isInclusive = generic_setter(value, bool)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = generic_setter(value, datetime)


class RangePeriod(ComponentValueType):
    def __init__(self, start: Period, end: Period):
        super(RangePeriod).__init__()
        self.start = start
        self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = generic_setter(value, datetime)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = generic_setter(value, datetime)


class MemberSelection:

    def __init__(self, isIncluded: bool = False, valuesFor: Component = None, selValue: list = None):
        self.isIncluded = isIncluded
        self.valuesFor = valuesFor
        self.selValue = selValue

    @property
    def selValue(self):
        return self._selValue

    @selValue.setter
    def selValue(self, value):
        self._selValue = generic_setter(value, list)

    @property
    def valuesFor(self):
        return self._valuesFor

    @valuesFor.setter
    def valuesFor(self, value):
        self._valuesFor = generic_setter(value, Component)

    @property
    def isIncluded(self):
        return self._isIncluded

    @isIncluded.setter
    def isIncluded(self, value):
        self._isIncluded = generic_setter(value, bool)


class CubeRegion(DataParser):

    def __init__(self, isIncluded: bool = False, member: MemberSelection = None):
        super(CubeRegion).__init__()
        self.isIncluded = isIncluded

        self.member = member

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of CubeRegion"""
        return CubeRegion(*args_, **kwargs_)

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = generic_setter(value, MemberSelection)

    @property
    def isIncluded(self):
        return self._isIncluded

    @isIncluded.setter
    def isIncluded(self, value):
        self._isIncluded = value


class MetadataTargetRegion:

    def __init__(self, compList: ComponentList, isIncluded: bool = False, member: MemberSelection = None):
        self.isIncluded = isIncluded

        self.compList = compList

        self.member = member

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = generic_setter(value, MemberSelection)

    @property
    def compList(self):
        return self._compList

    @compList.setter
    def compList(self, value):
        self._compList = generic_setter(value, ComponentList)

    @property
    def isIncluded(self):
        return self._isIncluded

    @isIncluded.setter
    def isIncluded(self, value):
        self._isIncluded = generic_setter(value, bool)


class ReferencePeriod:
    def __init__(self, start: date, end: date):
        self.startDate = start
        self.endDate = end

    @property
    def startDate(self):
        return self._start

    @startDate.setter
    def startDate(self, value):
        self._start = generic_setter(value, date)

    @property
    def endDate(self):
        return self._end

    @endDate.setter
    def endDate(self, value):
        self._end = generic_setter(value, date)


class ReleaseCalendar:
    """
        javax.xml.datatype.Duration is substituted in this method with datetime.timedelta, as they have a similar
        meaning for the parsing methods used
    """

    def __init__(self, periodicity: timedelta, offset: timedelta, tolerance: timedelta):
        self.periodicity = periodicity
        self.offset = offset
        self.tolerance = tolerance

    @property
    def periodicity(self):
        return self._periodicity

    @periodicity.setter
    def periodicity(self, value):
        self._periodicity = generic_setter(value, timedelta)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = generic_setter(value, timedelta)

    @property
    def tolerance(self):
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = generic_setter(value, timedelta)


class Constraint(MaintainableArtefact):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, dataContentRegion: List[CubeRegion] = None,
                 metadataContentRegion: List[MetadataTargetRegion] = None,
                 availableDates: List[ReferencePeriod] = None, calendar: List[ReleaseCalendar] = None):
        if annotations is None:
            annotations = []
        super(Constraint, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                         name=name, description=description,
                                         version=version, validFrom=validFrom, validTo=validTo,
                                         isFinal=isFinal, isExternalReference=isExternalReference,
                                         serviceUrl=serviceUrl, structureUrl=structureUrl)
        self.metadataContentRegion = metadataContentRegion
        self.dataContentRegion = dataContentRegion
        self.availableDates = availableDates
        self.calendar = calendar

    @property
    def dataContentRegion(self):
        return self._dataContentRegion

    @dataContentRegion.setter
    def dataContentRegion(self, value):
        self._dataContentRegion = generic_setter(value, List[CubeRegion])

    @property
    def metadataContentRegion(self):
        return self._metadataContentRegion

    @metadataContentRegion.setter
    def metadataContentRegion(self, value):
        self._metadataContentRegion = generic_setter(value, List[MetadataTargetRegion])

    @property
    def availableDates(self):
        return self._availableDates

    @availableDates.setter
    def availableDates(self, value):
        self._availableDates = generic_setter(value, ReferencePeriod)

    @property
    def calendar(self):
        return self._calendar

    @calendar.setter
    def calendar(self, value):
        self._calendar = generic_setter(value, ReleaseCalendar)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Constraint, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Constraint, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)


class AttachmentConstraint(DataParser):
    pass


class ContentConstraint(Constraint):
    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, dataContentRegion: List[CubeRegion] = None,
                 metadataContentRegion: List[MetadataTargetRegion] = None,
                 availableDates: List[ReferencePeriod] = None, calendar: List[ReleaseCalendar] = None,
                 role: str = None):
        if annotations is None:
            annotations = []
        super(ContentConstraint, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
                                                name=name, description=description,
                                                version=version, validFrom=validFrom, validTo=validTo,
                                                isFinal=isFinal, isExternalReference=isExternalReference,
                                                serviceUrl=serviceUrl, structureUrl=structureUrl,
                                                dataContentRegion=dataContentRegion,
                                                metadataContentRegion=metadataContentRegion,
                                                availableDates=availableDates, calendar=calendar)
        if role not in ConstraintRoleType:
            raise ValueError('ConstraintRole must be either "allowableContent" or "actualContent"')
        self._role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in ConstraintRoleType:
            raise ValueError('ConstraintRole must be either "allowableContent" or "actualContent"')
        else:
            self._role = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ContentConstraint, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(ContentConstraint, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

        if nodeName_ == 'ConstraintAttachment':
            obj_ = AttachmentConstraint._factory()
            obj_._build(child_, gds_collector_=gds_collector_)

        elif nodeName_ == 'CubeRegion':
            obj_ = CubeRegion._factory()
            obj_._build(child_, gds_collector_=gds_collector_)


class ConstrainableArtifact(DataParser):

    def __init__(self, content: ContentConstraint, attachment: AttachmentConstraint):
        super().__init__()
        self.content = content
        self.attachment = attachment

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = generic_setter(value, ContentConstraint)

    @property
    def attachment(self):
        return self._attachment

    @attachment.setter
    def attachment(self, value):
        self._attachment = generic_setter(value, AttachmentConstraint)
