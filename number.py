# -*- coding: utf-8 -*-
import re
from typing import Union, Type


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
            print(f"String should contain only numbers -> {not_accepted}")
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
            print(f"String should contain only numbers -> {not_accepted}")
            return return_type()
    else:
        raise TypeError(f"Not supported type for iterable: {type(iterable)}")


def str2int(string_number: str, sep: str = ',') -> int:
    number = 0
    numbers = string_number.split(sep)
    ints = intify(numbers)

    for thousand_num, num in enumerate(ints[::-1]):
        if thousand_num == 0:
            number += num
        else:
            number += 1000**thousand_num * num

    return number
