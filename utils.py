# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import Tuple, Union

from at.io import load_json, write_json
from at.logger import log


def user() -> str:
    return os.environ.get('USERNAME')


def parse_xlsx_filepath(text: str) -> Tuple[str, Union[str, int]]:
    _text = text
    if '@' in _text:
        _split = _text.split('@')
        _path = _split[0]
        _sheet = _split[1]
        return _path, _sheet
    else:
        return _text, 0


def load_user_settings(settings_file: Union[str, Path],
                       default_settings: dict) -> dict:
    try:
        return load_json(settings_file)
    except FileNotFoundError:
        write_json(settings_file, default_settings)
        log.warning("No app setting detected. Empty settings file created")

        return default_settings
