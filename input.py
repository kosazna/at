# -*- coding: utf-8 -*-
import os
from typing import Union

from at.logger import log, strferror, strfsuccess, strfwarning

DIR = 'directory'
FILE = 'file'


def _ensure_path_type(path: str, path_type: str) -> bool:
    if path_type == DIR:
        return os.path.isdir(path)
    elif path_type == FILE:
        return os.path.isfile(path)
    else:
        raise ValueError("path_type must be either 'directory' or 'file'")


def input_filename(prompt: str, suffix: str = None) -> str:
    _user_input = input(prompt).strip()

    not_valid = ('.', '<', '>', ':', '"', '/', '\\', '|', '?', '*')

    valid = True

    for char in not_valid:
        if char in _user_input:
            valid = False

    if not valid:
        _banned = ' '.join(not_valid)
        log.warning(
            f"\nFilename must not contain these 10 characters: {_banned}\nTry again:")
        return input_filename('', suffix)
    else:
        if suffix is not None:
            return f"{_user_input}.{suffix}"
        else:
            return _user_input


def input_bool(prompt: str) -> bool:
    _yes_no = strfsuccess('[Y]/N')

    _prompt = prompt.strip('\n')
    _prompt = f"\n{_prompt}  -  {_yes_no}\n"

    while True:
        _user_input = input(_prompt).upper().strip()

        if _user_input not in ('Y', 'N', ''):
            continue
        else:
            _user_input = _user_input if _user_input else 'Y'
            break

    if _user_input == 'Y':
        return True
    return False


def input_path(prompt: str,
               accept_empty: bool = False,
               ensure: Union[str, None] = None) -> str:

    _path = input(prompt).replace('\\', '/').strip('"')

    if accept_empty and _path == '':
        return _path
    else:
        if os.path.exists(_path):
            if ensure is not None:
                _bool = _ensure_path_type(_path, ensure)
                if _bool:
                    return _path
                else:
                    log.warning(
                        f"Path must be a {ensure}. Give path again:")
                    return input_path('', accept_empty, ensure)
            return _path
        else:
            _, ext = os.path.splitext(_path)

            if ensure is not None:
                if ensure == DIR and ext != '':
                    log.warning(f"Path must be a {ensure}. Give path again:")
                    return input_path('', accept_empty, ensure)
                elif ensure == FILE and ext == '':
                    log.warning(f"Path must be a {ensure}. Give path again:")
                    return input_path('', accept_empty, ensure)
                else:
                    pass

            if ext != '':
                log.error("File does not exist. Give path again:")
                return input_path('', accept_empty, ensure)
            else:
                _display = "Directory does not exist. Create?"
                _create = input_bool(_display)

                if _create:
                    os.makedirs(_path)
                    return _path
                else:
                    _error = f"{_path} can't be used for any operation."
                    raise IOError(_error)
