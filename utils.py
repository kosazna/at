# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Union

from at.date import timestamp
from at.io import load_json, write_json


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
        load_json(settings_file)
    except FileNotFoundError:
        write_json(settings_file, default_settings)

    print(f"There are no settings for user '{user()}'. Empty settings created")
    return default_settings

def check_auth_file(filepath: str, ref_hour: int = 12):
    if os.path.exists(filepath):
        current_time = timestamp(return_object=True)
        creation_time = datetime.fromtimestamp(os.stat(filepath).st_ctime)

        if timedelta(minutes=ref_hour) < current_time - creation_time:
            print("Refresh credentials")
            return False
        else:
            return True
    else:
        print("Authentication file does not exist")
        return False
