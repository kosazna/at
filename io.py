# -*- coding: utf-8 -*-
import json
import os
import random
import string
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from shutil import copy2, copyfileobj, copytree
from typing import List, Tuple, Union

import requests

from pattern import FilePattern
from text import replace_all

SHP_EXTS = ('.shp', '.shx', '.dbf')


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
            copyfileobj(r.raw, f)
            print(f"Saved -> {filename}")
    else:
        print(f"Request failed -> {url}")


def file_copy(src: Union[str, Path],
              dst: Union[str, Path],
              save_name: Union[str, None] = None):
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        print(f"File '{str(src)}' does not exist.")
        return

    src_is_dir = src_path.is_dir()
    dst_is_dir = not bool(dst_path.suffix)

    if dst_is_dir:
        if not dst_path.exists():
            dst_path.mkdir(parents=True, exist_ok=True)
    else:
        if not dst.parent.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)

    if src_is_dir:
        if save_name is None:
            copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            copytree(src_path, dst_path.joinpath(save_name),
                     dirs_exist_ok=True)
    else:
        src_suffix = src_path.suffix

        if src_suffix not in SHP_EXTS:
            if save_name is None:
                copy2(src_path, dst_path)
            else:
                if dst_is_dir:
                    d = dst_path.joinpath(f"{save_name}{src_suffix}")
                else:
                    d = dst_path.with_name(save_name).with_suffix(src_suffix)

                copy2(src_path, d)
        else:
            all_exist = all([src_path.with_suffix(ext).exists()
                            for ext in SHP_EXTS])

            if all_exist:
                for ext in SHP_EXTS:
                    if save_name is None:
                        copy2(src_path.with_suffix(ext), dst_path)
                    else:
                        if dst_is_dir:
                            d = dst_path.joinpath(f"{save_name}{ext}")
                        else:
                            d = dst_path.with_name(save_name).with_suffix(ext)

                        copy2(src_path.with_suffix(ext), d)
            else:
                print(f"'{str(src)}' missing auxiliary shapefile files.")


def pattern_copy(src: Union[str, Path],
                 dst: Union[str, Path],
                 filters: Union[str, List[str], Tuple[str]],
                 read_pattern: str,
                 save_pattern: Union[str, None] = None,
                 save_name: Union[str, None] = None,
                 recursive: bool = False):
    src_path = Path(src)
    dst_path = Path(dst)

    pattern = FilePattern(read_pattern)
    file_filters = []

    if isinstance(filters, str):
        if recursive:
            file_filters.append(f"**/{filters}")
    else:
        for _filter in filters:
            if recursive:
                file_filters.append(f"**/{_filter}")
            else:
                file_filters.append(_filter)

    with ThreadPoolExecutor() as executor:
        for file_filter in file_filters:
            for p in src_path.glob(file_filter):
                if pattern.kind == 'FolderPattern':
                    parts = pattern.match_from_path(p)
                else:
                    parts = pattern.match(p.stem)

                parts['%name%'] = p.stem
                parts['%parent%'] = p.parent

                if save_name is None:
                    name = save_name
                else:
                    name = replace_all(save_name, parts)

                if save_pattern is None:
                    d = dst_path
                else:
                    sub_dst = replace_all(save_pattern, parts)
                    d = dst_path.joinpath(sub_dst)

                executor.submit(file_copy, p, d, name)


if __name__ == "__main__":
    src = "D:/.temp/KT5-16_ΠΑΡΑΔΟΣΗ_30-09-2021/ΕΝΔΙΑΜΕΣΗ ΥΠΟΒΟΛΗ ΚΤΗΜΑΤΟΛΟΓΙΚΗΣ ΒΑΣΗΣ ΧΩΡΙΚΩΝ ΣΤΟΙΧΕΙΩΝ/SHAPE"
    dst = "D:/.temp/copy_tests"

    pattern_read = "<ota$1><folder$0>"
    pattern_out = "<ota>/<folder>"
    # save_name = "<%filename%>_<ota>"
    save_name = None

    pattern_copy(src=src,
                 dst=dst,
                 filters=['ASTENOT', 'ASTOTA', 'PST'],
                 read_pattern=pattern_read,
                 save_pattern=pattern_out,
                 recursive=True,
                 save_name=save_name)

    # structure_copy(src, dst, ['ASTENOT', 'ASTOTA', 'PST'])
