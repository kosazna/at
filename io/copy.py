# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from shutil import copy2, copytree
from typing import Iterable, List, Tuple, Union

from at.io.object import CopyObject
from at.logger import log
from at.pattern import FilePattern
from at.text import replace_all

SHP_EXTS = ('.shp', '.shx', '.dbf')


def create_copy_obj(src: Union[str, Path],
                    dst: Union[str, Path],
                    save_name: Union[str, None] = None) -> CopyObject:
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        log.error(f"File '{str(src_path)}' does not exist.")
        return None

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
            _dst_path = dst_path
        else:
            _dst_path = dst_path.joinpath(save_name)
    else:
        src_suffix = src_path.suffix

        if save_name is None:
            _dst_path = dst_path
        else:
            if dst_is_dir:
                _dst_path = dst_path.joinpath(f"{save_name}{src_suffix}")
            else:
                _dst_path = dst_path.with_name(
                    save_name).with_suffix(src_suffix)

    return CopyObject(src=src_path, dst=_dst_path)


def copy_file(src: Union[str, Path],
              dst: Union[str, Path],
              save_name: Union[str, None] = None,
              copymode: str = 'normal') -> str:
    copyobj = create_copy_obj(src=src, dst=dst, save_name=save_name)

    if copyobj is not None:
        return copyobj.copy(copymode=copymode)
    return ''


def batch_copy_file(files: Iterable[CopyObject],
                    copymode: str = 'fast',
                    verbose: bool = False) -> None:
    with ThreadPoolExecutor() as executor:
        for idx, file2copy in enumerate(files, 1):
            future = executor.submit(file2copy.copy, copymode)
            if verbose:
                log.info(f"{idx:5d} - {future.result()}")


def copy_file_legacy(src: Union[str, Path],
                     dst: Union[str, Path],
                     save_name: Union[str, None] = None):
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        log.error(f"File '{str(src_path)}' does not exist.")
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
                log.warning(f"'{str(src)}' missing auxiliary shapefile files.")


def copy_pattern(src: Union[str, Path],
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

                executor.submit(copy_file, p, d, name)
