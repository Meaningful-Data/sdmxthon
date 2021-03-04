from datetime import datetime, date


class ObservationalTimePeriod:
    pass


class StandardTimePeriod(ObservationalTimePeriod):
    pass


class BasicTimePeriod(StandardTimePeriod):
    pass


class ReportingTimePeriod(StandardTimePeriod):
    pass


class TimeRange(ObservationalTimePeriod):
    pass


class GregorianTimePeriod(BasicTimePeriod):
    pass


class GregorianDate(GregorianTimePeriod):
    def __init__(self, year: int, month: int = 1, day: int = 1):
        self.date = date(year=year, month=month, day=day)

    @property
    def year(self):
        return self.date.strftime('%Y')

    @property
    def year_month(self):
        return self.date.strftime('%Y-%m')

    @property
    def day(self):
        return self.date.strftime('%Y-%m-%d')


class DateTime:
    def __init__(self, year: int, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0, second: int = 0):
        self.datetime = datetime(year=year, month=month, day=day, hour=hour,
                                 minute=minute, second=second, microsecond=0)

    @property
    def value(self):
        return self.datetime.strftime('%Y-%m-%dT%H:%M:%S')
