from datetime import datetime, date, timedelta

from SDMXThon.model.utils import generic_setter
from SDMXThon.parsers.data_generic import ComponentValueType


class Period:
    def __init__(self, isInclusive: bool, period: datetime):
        self.is_inclusive = isInclusive
        self.period = period

    @property
    def is_inclusive(self):
        return self._isInclusive

    @is_inclusive.setter
    def is_inclusive(self, value):
        self._isInclusive = generic_setter(value, bool)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = generic_setter(value, datetime)


class RangePeriod(ComponentValueType):
    def __init__(self, start: Period, end: Period):
        super(RangePeriod, self).__init__()
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


class ReferencePeriod:
    def __init__(self, start: date, end: date):
        self.start_date = start
        self.end_date = end

    @property
    def start_date(self):
        return self._start

    @start_date.setter
    def start_date(self, value):
        self._start = generic_setter(value, date)

    @property
    def end_date(self):
        return self._end

    @end_date.setter
    def end_date(self, value):
        self._end = generic_setter(value, date)


class ReleaseCalendar:
    """
    javax.xml.datatype.Duration is substituted in this method with
    datetime.timedelta, as they have a similar meaning for the parsing
    methods used
    """

    def __init__(self, periodicity: timedelta, offset: timedelta,
                 tolerance: timedelta):
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
