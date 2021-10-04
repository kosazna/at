# -*- coding: utf-8 -*-
import json
import os
import random
import shutil
import string
from pathlib import Path
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
            shutil.copyfileobj(r.raw, f)
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
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copytree(src_path, dst_path.joinpath(save_name),
                            dirs_exist_ok=True)
    else:
        src_suffix = src_path.suffix

        if src_suffix not in SHP_EXTS:
            if save_name is None:
                shutil.copy2(src_path, dst_path)
            else:
                if dst_is_dir:
                    d = dst_path.joinpath(f"{save_name}{src_suffix}")
                else:
                    d = dst_path.with_name(save_name).with_suffix(src_suffix)

                shutil.copy2(src_path, d)
        else:
            all_exist = all([src_path.with_suffix(ext).exists()
                            for ext in SHP_EXTS])

            if all_exist:
                for ext in SHP_EXTS:
                    if save_name is None:
                        shutil.copy2(src_path.with_suffix(ext), dst_path)
                    else:
                        if dst_is_dir:
                            d = dst_path.joinpath(f"{save_name}{ext}")
                        else:
                            d = dst_path.with_name(save_name).with_suffix(ext)

                        shutil.copy2(src_path.with_suffix(ext), d)
            else:
                print(f"'{str(src)}' missing auxiliary shapefile files.")


def structure_copy(src: Union[str, Path],
                   dst: Union[str, Path],
                   folders: Union[str, List[str], Tuple[str]]):
    src_path = Path(src)
    dst_path = Path(dst)

    if isinstance(folders, str):
        folders = [folders]

    src_len = len(src_path.parts)

    for folder in folders:
        for p in src_path.rglob(folder):
            parts = p.parts
            parts_len = len(parts)
            keep = src_len - parts_len

            subdirs = '/'.join(p.parts[keep:])
            d = dst_path.joinpath(subdirs)

            file_copy(src=p, dst=d)


def pattern_copy(src_path: Union[str, Path],
                 dst_path: Union[str, Path],
                 file_filter: str,
                 pattern_read: str,
                 pattern_out: Union[str, None] = None,
                 recursive: bool = False,
                 save_name: Union[str, None] = None):
    src_path = Path(src)
    dst_path = Path(dst)

    pattern = FilePattern(pattern_read)

    if recursive:
        file_filter = f"**/{file_filter}"

    for p in src_path.glob(file_filter):
        if pattern.kind == 'FolderPattern':
            parts = pattern.match_from_path(p)
        else:
            parts = pattern.match(p.stem)

        parts['%filename%'] = p.stem

        if save_name is None:
            name = save_name
        else:
            name = replace_all(save_name, parts)

        if pattern_out is None:
            d = dst_path
        else:
            sub_dst = replace_all(pattern_out, parts)
            d = dst_path.joinpath(sub_dst)

        file_copy(src=p, dst=d, save_name=name)


if __name__ == "__main__":
    src = "D:/.temp/KT5-16_ΠΑΡΑΔΟΣΗ_30-09-2021/ΕΝΔΙΑΜΕΣΗ ΥΠΟΒΟΛΗ ΚΤΗΜΑΤΟΛΟΓΙΚΗΣ ΒΑΣΗΣ ΧΩΡΙΚΩΝ ΣΤΟΙΧΕΙΩΝ/SHAPE"
    dst = "D:/.temp/copy_tests"

    pattern_read = "<ota$2><shapefile$1>"
    pattern_out = "KT5-16/<shapefile>"
    save_name = "<%filename%>_<ota>"

    pattern_copy(src_path=src,
                 dst_path=dst,
                 file_filter='ASTENOT.shp',
                 pattern_read=pattern_read,
                 pattern_out=pattern_out,
                 recursive=True,
                 save_name=save_name)
