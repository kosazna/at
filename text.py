# -*- coding: utf-8 -*-
import re
from hashlib import sha256
from typing import Type, Union


def replace_all(text: str, replacements: dict) -> str:
    for key, val in replacements.items():
        text = text.replace(f"<{key}>", val)
    return text


def remove_overspace(text: str) -> str:
    return re.sub('\s{2,}', ' ', str(text)).strip()


def stringify(iterable: Union[list, tuple, set, dict],
              return_type: Type = list) -> Union[list, tuple, set]:

    if isinstance(iterable, (list, tuple, set, dict)):
        return return_type(map(str, iterable))
    else:
        raise TypeError(f"Not supported type for iterable: {type(iterable)}")


def create_hex_string(string: str) -> str:
    return sha256(string=string.encode('utf-8')).hexdigest()
