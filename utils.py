# -*- coding: utf-8 -*-
import os
from typing import Tuple, Union


def user() -> str:
    os.environ.get('USERNAME')


def parse_xlsx_filepath(text: str) -> Tuple[str, Union[str, int]]:
    _text = text
    if '@' in _text:
        _split = _text.split('@')
        _path = _split[0]
        _sheet = _split[1]
        return _path, _sheet
    else:
        return _text, 0
