# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

from at.date import daterange, timestamp
from at.io.copyfuncs import copy_file
from at.io.utils import (load_json, load_pickle, unzip_file, write_pickle,
                         zip_files)
from at.result import Result
from at.text import create_hex_string


def create_lic(authdata: Union[str, Path],
               appname: str,
               folder: Union[str, Path],
               date: Union[str, None] = None):
    if date is None:
        date_str = timestamp(time=False)
    else:
        date_str = date

    temp_auth = create_hex_string(f"{appname}-{date_str}")
    dst = Path(folder).joinpath(f"{temp_auth}.lic")

    if isinstance(authdata, dict):
        data = authdata
    else:
        auth_path = Path(authdata)
        if auth_path.suffix == '.json':
            data = load_json(auth_path)
        else:
            data = load_pickle(auth_path)

    write_pickle(dst, data)


def create_lic_zip(authdata: Union[str, Path],
                   appname: str,
                   folder: Union[str, Path, None],
                   periods: int,
                   start_date: Union[str, None] = None):

    dates = daterange(periods=periods, start_date=start_date)

    for date in dates:
        create_lic(authdata=authdata,
                   appname=appname,
                   folder=folder,
                   date=date)

    out_name = f"{start_date}_{periods}lic"
    zip_files(src=folder, dst=folder, save_name=out_name, file_filter='*.lic')

    for p in Path(folder).glob('*.lic'):
        p.unlink()

    return Result.success('License created successfully')


def load_lic(filepath: Union[str, Path],
             dst: Union[str, Path]):
    if filepath:
        file_path = Path(filepath)
        licfolder_path = Path(dst)

        if file_path.suffix == '.zip':
            unzip_file(file_path, licfolder_path)
        else:
            copy_file(file_path, licfolder_path)
        return Result.success("License uploaded successfully")
    else:
        return Result.error("No file was provided")


def check_lic(appname: str, licfolder: Union[str, Path]) -> str:
    licfolder_path = Path(licfolder)
    date_str = timestamp(time=False)
    temp_auth = create_hex_string(f"{appname}-{date_str}")
    licfile = licfolder_path.joinpath(f"{temp_auth}.lic")
    if licfile.exists():
        print(load_pickle(licfile))
    else:
        print({})
