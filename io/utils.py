# -*- coding: utf-8 -*-
import json
import pickle
from os import startfile
from pathlib import Path
from shutil import unpack_archive
from typing import Any, List, Tuple, Union
from zipfile import ZipFile


def open_excel(filepath: Union[str, Path]) -> None:
    startfile(filepath)


def load_json(filepath: Union[str, Path]) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(filepath: Union[str, Path],
               data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_pickle(filepath: Union[str, Path]) -> Any:
    with open(Path(filepath), 'rb') as pf:
        return pickle.load(pf)


def write_pickle(filepath: Union[str, Path],
                 data: dict) -> None:
    with open(filepath, 'wb') as pf:
        pickle.dump(data, pf, protocol=pickle.DEFAULT_PROTOCOL)


def zip_file(src: Union[str, Path],
             dst: Union[str, Path, None] = None,
             save_name: Union[str, None] = None,
             file_filter: Union[str, None] = None,
             schema: bool = False):
    src_path = Path(src)

    if dst is None:
        dst_path = src_path
    else:
        dst_path = Path(dst)

    if save_name is None:
        d = dst_path.joinpath(f"{src_path.stem}.zip")
    else:
        d = dst_path.joinpath(f"{save_name}.zip")

    if file_filter is None:
        files2zip = tuple(src_path.iterdir())
    else:
        files2zip = tuple(src_path.glob(file_filter))

    if files2zip:
        with ZipFile(d, 'w') as zf:
            for filepath in files2zip:
                if schema:
                    zf.write(filepath)
                else:
                    zf.write(filepath, arcname=filepath.name)


def unzip_file(zipfile: Union[str, Path], dst: Union[str, Path]):
    dst_path = Path(dst)
    if not dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)
    unpack_archive(zipfile, dst_path)


def unzip_file_pro(src: Union[str, Path],
                   dst: Union[str, Path],
                   filters: Union[str, List[str], Tuple[str], None] = None,
                   filter_type: str = 'name'):

    if filters is not None:
        if isinstance(filters, str):
            file_filters = [filters]
        else:
            file_filters = filters

    with ZipFile(src, 'r') as f:
        if filters is None:
            f.extractall(dst)
        else:
            files = {filename: Path(filename) for filename in f.namelist()}
            if filter_type == 'suffix':
                for fn, p in files.items():
                    if p.suffix in file_filters:
                        f.extract(fn, dst)
            elif filter_type == 'filename':
                for fn, p in files.items():
                    if p.stem in file_filters:
                        f.extract(fn, dst)
            elif filter_type == 'dir':
                for fn, p in files.items():
                    for filter_item in file_filters:
                        if filter_item in p.parts:
                            f.extract(fn, dst)
