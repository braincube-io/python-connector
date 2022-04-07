from enum import Enum


class PeriodUnitType(Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    QUARTER = 'QUARTER'
    YEAR = 'YEAR'
    CUSTOM = 'CUSTOM'
    ALL = 'ALL'


class Period(object):

    def __init__(
        self, begin: int, end: int, period_unit_type: PeriodUnitType, quantity: int, calendar_quantity: int,
            offset: int, offset_quantity: int
    ) -> None:
        self.begin = begin
        self.end = end
        self.period_unit_type = period_unit_type
        self.quantity = quantity
        self.calendar_quantity = calendar_quantity
        self.offset = offset
        self.offset_quantity = offset_quantity


