# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import sys

from at.io.utils import load_json, write_json
from at.logger import log

if sys.platform == "win32":
    from win32com.client import Dispatch


def user() -> str:
    return os.environ.get('USERNAME')


def purge_dict(data: dict) -> dict:
    new_dict = {}
    for key, value in data.items():
        if bool(value):
            new_dict[key] = value

    return new_dict


def dicts2list(dict_list: List[dict]) -> Dict[Any, list]:
    return {
        k: [d.get(k) for d in dict_list if k in d] for k in set().union(*dict_list)
    }


def make_shortcut(src: Union[str, Path],
                  dst: Union[str, Path],
                  shortcut_name: Optional[str] = None):
    src_path = Path(src)
    dst_path = Path(dst)

    if shortcut_name is None:
        shortcut_path = dst_path.joinpath(f"{src_path.stem}.lnk")
    else:
        shortcut_path = dst_path.joinpath(f"{shortcut_name}.lnk")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.Targetpath = str(src_path)
    shortcut.WindowStyle = 1
    shortcut.save()


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
