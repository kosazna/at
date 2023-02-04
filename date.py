# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import Union

ISODATE = "%Y-%m-%d"
ISOTIME = "%H:%M:%S"
ISOTIME_COMP = "%H%M%S"
GRDATE = "%d/%m/%Y"
USDATE = "%m/%d/%Y"

DATE_MAPPER = {
    "DD/MM/YYYY": GRDATE,
    "MM/DD/YYYY": USDATE
}

def timestamp(date: bool = True,
              time: bool = True,
              return_object: bool = False,
              filename_compatible: bool = False) -> Union[str, datetime]:

    dt = datetime.now().replace(microsecond=0)

    if date and time:
        if return_object:
            return dt
        else:
            if filename_compatible:
                return dt.strftime(f"{ISODATE}_{ISOTIME_COMP}")
            else:
                return dt.strftime(f"{ISODATE} {ISOTIME}")

    elif date and not time:
        if return_object:
            return dt.replace(hour=0, minute=0, second=0)
        else:
            return dt.strftime(f"{ISODATE}")
    else:
        if return_object:
            return dt.time()
        else:
            if filename_compatible:
                return dt.strftime(f"{ISOTIME_COMP}")
            else:
                return dt.strftime(f"{ISOTIME}")


def daterange(periods: int,
              start_date: Union[str, None] = None,
              return_object: bool = False) -> Union[str, datetime]:
    if start_date is None:
        _start_date = datetime.today().date()
    else:
        components = tuple(map(int, start_date.split('-')))
        _start_date = datetime(*components).date()
    date_list = [_start_date + timedelta(days=d) for d in range(periods)]
    if return_object:
        return date_list
    return [dt.strftime(ISODATE) for dt in date_list]
