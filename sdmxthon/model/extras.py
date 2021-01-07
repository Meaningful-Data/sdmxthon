from datetime import datetime, date, timedelta

from SDMXThon.model.base import MaintainableArtefact, InternationalString
from SDMXThon.model.dataTypes import ConstraintRoleType
from SDMXThon.model.structure import ComponentList, List, Component
from SDMXThon.model.timePeriods import ObservationalTimePeriod
from SDMXThon.model.utils import qName, genericSetter


class SelectionValue:
    pass


class MemberValue(SelectionValue):

    def __init__(self, value: str, cascadeValues: bool):
        self.value_ = value
        self.cascadeValue = cascadeValues

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        self._value = genericSetter(value, str)

    @property
    def cascadeValue(self):
        return self._cascadeValue

    @cascadeValue.setter
    def cascadeValue(self, value):
        self._cascadeValue = genericSetter(value, bool)


class TimeRangeValue(SelectionValue):
    pass


class Period:
    def __init__(self, isInclusive: bool, period: ObservationalTimePeriod):
        self.isInclusive = isInclusive
        self.period = period

    @property
    def isInclusive(self):
        return self._isInclusive

    @isInclusive.setter
    def isInclusive(self, value):
        self._isInclusive = genericSetter(value, bool)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = genericSetter(value, ObservationalTimePeriod)


class BeforePeriod(Period):
    pass


class AfterPeriod(Period):
    pass


class StartPeriod(Period):
    pass


class EndPeriod(Period):
    pass


class RangePeriod(TimeRangeValue):
    def __init__(self, start: Period, end: Period):
        self.start = start
        self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = genericSetter(value, StartPeriod)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = genericSetter(value, EndPeriod)


class MemberSelection:

    def __init__(self, isIncluded: bool = False, valuesFor: Component = None, selValue: List[SelectionValue] = None):
        self.isIncluded = isIncluded
        self.valuesFor = valuesFor
        self.selValue = selValue

    @property
    def selValue(self):
        return self._selValue

    @selValue.setter
    def selValue(self, value):
        self._selValue = genericSetter(value, List[SelectionValue])

    @property
    def valuesFor(self):
        return self._valuesFor

    @valuesFor.setter
    def valuesFor(self, value):
        self._valuesFor = genericSetter(value, Component)

    @property
    def isIncluded(self):
        return self._isIncluded

    @isIncluded.setter
    def isIncluded(self, value):
        self._isIncluded = genericSetter(value, bool)


class CubeRegion:

    def __init__(self, isIncluded: bool = False, member: MemberSelection = None):
        self.isIncluded = isIncluded

        self.member = member

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = genericSetter(value, MemberSelection)

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
        self._member = genericSetter(value, MemberSelection)

    @property
    def compList(self):
        return self._compList

    @compList.setter
    def compList(self, value):
        self._compList = genericSetter(value, ComponentList)

    @property
    def isIncluded(self):
        return self._isIncluded

    @isIncluded.setter
    def isIncluded(self, value):
        self._isIncluded = genericSetter(value, bool)


class ReferencePeriod:
    def __init__(self, start: date, end: date):
        self.startDate = start
        self.endDate = end

    @property
    def startDate(self):
        return self._start

    @startDate.setter
    def startDate(self, value):
        self._start = genericSetter(value, date)

    @property
    def endDate(self):
        return self._end

    @endDate.setter
    def endDate(self, value):
        self._end = genericSetter(value, date)


class ReleaseCalendar:
    """
        javax.xml.datatype.Duration is substituted in this method with timedelta, as they have a similar meaning
        for the parsing methods used
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
        self._periodicity = genericSetter(value, timedelta)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = genericSetter(value, timedelta)

    @property
    def tolerance(self):
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = genericSetter(value, timedelta)


class Constraint(MaintainableArtefact):
    _urnType = "datastructure"
    _qName = qName("str", "Constraint")

    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, dataContentRegion: List[CubeRegion] = None,
                 metadataContentRegion: List[MetadataTargetRegion] = None,
                 availableDates: List[ReferencePeriod] = None, calendar: List[ReleaseCalendar] = None):
        if annotations is None:
            annotations = []
        super(Constraint, self).__init__(id_=id_, uri=uri, annotations=annotations,
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
        self._dataContentRegion = genericSetter(value, List[CubeRegion])

    @property
    def metadataContentRegion(self):
        return self._metadataContentRegion

    @metadataContentRegion.setter
    def metadataContentRegion(self, value):
        self._metadataContentRegion = genericSetter(value, List[MetadataTargetRegion])

    @property
    def availableDates(self):
        return self._availableDates

    @availableDates.setter
    def availableDates(self, value):
        self._availableDates = genericSetter(value, ReferencePeriod)

    @property
    def calendar(self):
        return self._calendar

    @calendar.setter
    def calendar(self, value):
        self._calendar = genericSetter(value, ReleaseCalendar)


class AttachmentConstraint(Constraint):
    pass


class ContentConstraint(Constraint):
    def __init__(self, id_: str = None, uri: str = None, annotations=None,
                 name: InternationalString = None, description: InternationalString = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None,
                 structureUrl: str = None, dataContentRegion: List[CubeRegion] = None,
                 metadataContentRegion: List[MetadataTargetRegion] = None,
                 availableDates: List[ReferencePeriod] = None, calendar: List[ReleaseCalendar] = None,
                 role: str = None):
        if annotations is None:
            annotations = []
        super(ContentConstraint, self).__init__(id_=id_, uri=uri, annotations=annotations,
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


class ConstrainableArtifact:

    def __init__(self, content: ContentConstraint, attachment: AttachmentConstraint):
        self.content = content
        self.attachment = attachment

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = genericSetter(value, ContentConstraint)

    @property
    def attachment(self):
        return self._attachment

    @attachment.setter
    def attachment(self, value):
        self._attachment = genericSetter(value, AttachmentConstraint)
