# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Union


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
                return dt.strftime("%Y-%m-%d--%H-%M-%S")
            else:
                return dt.strftime("%Y-%m-%d %H:%M:%S")

    elif date and not time:
        if return_object:
            return dt.date()
        else:
            return dt.strftime("%Y-%m-%d")
    else:
        if return_object:
            return dt.time()
        else:
            if filename_compatible:
                return dt.strftime("%H-%M-%S")
            else:
                return dt.strftime("%H:%M:%S")


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
    return [dt.strftime("%Y-%m-%d") for dt in date_list]
