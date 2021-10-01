# -*- coding: utf-8 -*-
import datetime
from typing import Union


def timestamp(date: bool = True,
              time: bool = True,
              return_object: bool = False,
              filename_compatible: bool = False) -> Union[str, datetime.datetime]:

    dt = datetime.datetime.now().replace(microsecond=0)

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
