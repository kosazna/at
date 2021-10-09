# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

from at.date import timestamp
from at.io import file_copy, load_json, load_pickle, unzip, write_pickle
from at.text import create_hex_string


def create_temp_auth(authdata: Union[str, Path],
                     appname: str,
                     licfolder: Union[str, Path, None],
                     date: Union[str, None] = None):
    if date is None:
        date_str = timestamp(time=False)
    else:
        date_str = date

    temp_auth = create_hex_string(f"{appname}-{date_str}")
    dst = Path(licfolder).joinpath(f"{temp_auth}.lic")

    if isinstance(authdata, dict):
        data = authdata
    else:
        auth_path = Path(authdata)
        if auth_path.suffix == '.json':
            data = load_json(auth_path)
        else:
            data = load_pickle(auth_path)

    write_pickle(dst, data)


def load_temp_auth(filepath: Union[str, Path],
                   licfolder: Union[str, Path]):
    file_path = Path(filepath)
    licfolder_path = Path(licfolder)

    if file_path.suffix == '.zip':
        unzip(file_path, licfolder_path)
    else:
        file_copy(file_path, licfolder_path)


def show_lic(appname: str, licfolder: Union[str, Path]) -> str:
    licfolder_path = Path(licfolder)
    date_str = timestamp(time=False)
    temp_auth = create_hex_string(f"{appname}-{date_str}")
    licfile = licfolder_path.joinpath(f"{temp_auth}.lic")
    print(load_pickle(licfile))
