# -*- coding: utf-8 -*-
import json
import os
import random
import shutil
import string
from pathlib import Path
from typing import List, Tuple, Union

import requests


def open_excel(filepath: Union[str, Path]) -> None:
    os.startfile(filepath)


def load_json(filepath: Union[str, Path]) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File does not exist -> {filepath}")


def write_json(filepath: Union[str, Path],
               data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def download_image(url: str,
                   destination: str,
                   save_name: Union[str, None] = None) -> None:
    r = requests.get(url, stream=True)
    url_file = url.split("/")[-1]
    ext = os.path.splitext(url_file)[1]

    if ext:
        _ext = ext
    else:
        _ext = '.jpg'

    if save_name is None:
        basename = ''.join(random.choices(string.ascii_letters + string.digits,
                                          k=32))
        filename = f"{basename}{_ext}"
    elif save_name == 'original':
        if ext:
            filename = url_file
        else:
            filename = f"{url_file}{_ext}"
    else:
        basename = save_name
        filename = f"{basename}{_ext}"

    dst = os.path.join(destination, filename)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(dst, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print(f"Saved -> {filename}")
    else:
        print(f"Request failed -> {url}")

def copy_shp(src: Union[str, Path],
             dst: Union[str, Path],
             name: Union[str, None] = None,
             subdirs: Union[str, None] = None):
    _s = Path(src)
    _d = Path(dst)

    _name = _s.stem if name is None else name
    _subs = '' if subdirs is None else f'{subdirs}/'

    exts = ['.shp', '.shx', '.dbf']

    for ext in exts:
        _src = _s.with_suffix(ext)
        _dst = _d.joinpath(f'{_subs}{_name}{ext}')

        if not _dst.parent.exists():
            _dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy(_src, _dst)

def get_files(src: Union[str, Path],
              dst: Union[str, Path],
              folders: Union[List[str], Tuple[str]]):
    _src = Path(src)
    _dst = Path(dst)

    _src_len = len(_src.parts)

    for folder in folders:
        for p in _src.rglob(folder):
            parts = p.parts
            parts_len = len(parts)
            keep = _src_len - parts_len

            subdirs = '/'.join(p.parts[keep:])
            _d = _dst.joinpath(subdirs)

            shutil.copytree(p, _d)
