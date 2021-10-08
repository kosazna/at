# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Union
from hashlib import sha256

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
        return load_json(settings_file)
    except FileNotFoundError:
        write_json(settings_file, default_settings)
        print(f"No app setting detected. Empty settings file created")
        
        return default_settings

def check_auth_file(filepath: Union[str, Path], ref_hour: int = 12):
    authfile = Path(filepath)
    if authfile.exists():
        current_time = timestamp(return_object=True)
        creation_time = datetime.fromtimestamp(os.stat(filepath).st_ctime)

        if timedelta(minutes=ref_hour) < current_time - creation_time:
            print("Refresh credentials")
            authfile.unlink()
            return False
        else:
            return True
    else:
        print("Authentication file does not exist")
        return False

def create_temporary_authentication(appname:str, date:str):
    string = f"{appname}-{date}"
    temp_auth = sha256(string=string).hexdigest()
