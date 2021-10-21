# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List, Tuple, Union

from at.io.utils import load_json, write_json
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


def file_counter(src: Union[str, Path],
                 filters: Union[str, List[str], Tuple[str]],
                 recursive: bool = True) -> dict:
    src_path = Path(src)
    file_filters = []
    file_counter = {}

    if isinstance(filters, str):
        if recursive:
            file_filters.append(f"**/{filters}")
    else:
        for _filter in filters:
            if recursive:
                file_filters.append(f"**/{_filter}")
            else:
                file_filters.append(_filter)

    for file_filter in file_filters:
        for p in src_path.glob(file_filter):
            if p.is_file():
                filename = p.stem
                ext = p.suffix
                if ext not in file_counter:
                    file_counter[ext] = {}

                if filename in file_counter[ext]:
                    file_counter[ext][filename] += 1
                else:
                    file_counter[ext][filename] = 1

    return file_counter
