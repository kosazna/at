# -*- coding: utf-8 -*-
import re
from typing import Union, Type
from at.logger import log


def text2num(text: str):
    pattern = r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?'
    return re.findall(pattern, text)


def intify(iterable: Union[list, tuple, set, dict, str],
           return_type: Type = list) -> Union[list, tuple, set]:

    if isinstance(iterable, (list, tuple, set, dict, str)):
        try:
            return return_type(map(int, iterable))
        except ValueError:
            not_accepted = list(filter(lambda v: not v.isnumeric(), iterable))
            log.error(f"String should contain only numbers -> {not_accepted}")
            return return_type()
    else:
        raise TypeError(f"Not supported type for iterable: {type(iterable)}")


def floatify(iterable: Union[list, tuple, set, dict, str],
             return_type: Type = list) -> Union[list, tuple, set]:

    if isinstance(iterable, (list, tuple, set, dict, str)):
        try:
            return return_type(map(float, iterable))
        except ValueError:
            not_accepted = list(filter(lambda v: not v.isnumeric(), iterable))
            log.error(f"String should contain only numbers -> {not_accepted}")
            return return_type()
    else:
        raise TypeError(f"Not supported type for iterable: {type(iterable)}")


def str2num(string_number: str,
            decimal_sep: str = '.',
            thousand_sep: Union[str, None] = ',') -> int:
    total = 0

    split_decimals = string_number.split(decimal_sep)
    number = split_decimals[0]

    if len(split_decimals) == 1:
        decimal = ''
        ndecimals = 0
    else:
        decimal = split_decimals[1]
        ndecimals = len(decimal)
        decimal_number = float(decimal) / 10**len(decimal)
        total += decimal_number

    if thousand_sep is not None:
        numbers = number.split(thousand_sep)
    else:
        numbers = [number]

    ints = intify(numbers)

    for thousand_num, num in enumerate(ints[::-1]):
        if thousand_num == 0:
            total += num
        else:
            total += 1000**thousand_num * num

    return round(total, ndecimals) if ndecimals else total
