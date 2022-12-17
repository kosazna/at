# -*- coding: utf-8 -*-

from datetime import datetime

from pandas import Timestamp
from pandas.tseries.holiday import (AbstractHolidayCalendar, Holiday,
                                    HolidayCalendarFactory)
from pandas.tseries.offsets import CustomBusinessDay


class GreeceHolidayCalendarBase(AbstractHolidayCalendar):
    rules = [
        Holiday(name="New Year's Eve", month=1, day=1),
        Holiday(name="Theofaneia", month=1, day=6),
        Holiday(name="25h Martiou", month=3, day=25),
        Holiday(name="Ergatikh Prwtomageia", month=5, day=1),
        Holiday(name="Koimisi ths Theotokou", month=8, day=15),
        Holiday(name="28h Oktwvriou", month=10, day=28),
        Holiday(name="Christmas Day", month=12, day=25),
        Holiday(name="2nd Christmas Day", month=12, day=26),
    ]


class GreeceMoveableHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday(name="Kathara Deutera 2022", year=2022, month=3, day=7),
        Holiday(name="Megalh Paraskeuh 2022", year=2022, month=4, day=22),
        Holiday(name="Megalo Savvato 2022", year=2022, month=4, day=23),
        Holiday(name="Kuriakh tou Pasxa 2022", year=2022, month=4, day=24),
        Holiday(name="Deutera tou Pasxa 2022", year=2022, month=4, day=25),
        Holiday(name="Kathara Deutera 2023", year=2023, month=2, day=27),
        Holiday(name="Megalh Paraskeuh 2023", year=2023, month=4, day=14),
        Holiday(name="Megalo Savvato 2023", year=2023, month=4, day=15),
        Holiday(name="Kuriakh tou Pasxa 2023", year=2023, month=4, day=16),
        Holiday(name="Deutera tou Pasxa 2023", year=2023, month=4, day=17),
    ]

    start_date = Timestamp(datetime(2022, 1, 1))
    end_date = Timestamp(datetime(2023, 12, 31))


BasicHolidaysGR = GreeceHolidayCalendarBase(name='Basic Greece Holidays')
MoveableHolidays_2022_2023 = GreeceMoveableHolidayCalendar(
    name='Greece Holidays for 2022-2023')

HolidayCalendarGR_2022_2023 = HolidayCalendarFactory(
    "Greece Holidays 2022-2023", BasicHolidaysGR, MoveableHolidays_2022_2023)

HolidaysGR = HolidayCalendarGR_2022_2023()

BusinessDaysGR = CustomBusinessDay(calendar=HolidaysGR) # to be used in "freq" parameter
