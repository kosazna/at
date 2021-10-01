# -*- coding: utf-8 -*-
import re
from typing import Type, Union, Tuple


def replace_all(text: str, replacements: dict) -> str:
    for key, val in replacements.items():
        text = text.replace(f"<{key}>", val)
    return text


def remove_overspace(text: str) -> str:
    return re.sub('\s{2,}', ' ', str(text)).strip()


def parse_xlsx_filepath(text: str) -> Tuple[str, Union[str, int]]:
    _text = text
    if '@' in _text:
        _split = _text.split('@')
        _path = _split[0]
        _sheet = _split[1]
        return _path, _sheet
    else:
        return _text, 0


def stringify(iterable: Union[list, tuple, set, dict],
              return_type: Type = list) -> Union[list, tuple, set]:

    if isinstance(iterable, (list, tuple, set, dict)):
        return return_type(map(str, iterable))
    else:
        raise TypeError(f"Not supported type for iterable: {type(iterable)}")
