# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor

from pathlib import Path
from shutil import copy2, copytree, copy
from typing import List, Tuple, Union

from at.input import DIR, FILE
from at.logger import log
from at.pattern import FilePattern
from at.text import replace_all

SHP_EXTS = ('.shp', '.shx', '.dbf')


def make_paths(src: Union[str, Path],
               dst: Union[str, Path],
               save_name: Union[str, None] = None) -> Union[dict, list, None]:
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        log.error(f"File '{str(src)}' does not exist.")
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
            # copytree(src_path, dst_path, dirs_exist_ok=True)
            return {'src': src_path,
                    'dst': dst_path,
                    'type': DIR}
        else:
            # copytree(src_path, dst_path.joinpath(save_name), dirs_exist_ok=True)
            # return (src_path, dst_path.joinpath(save_name), DIR)
            return {'src': src_path,
                    'dst': dst_path.joinpath(save_name),
                    'type': DIR}
    else:
        src_suffix = src_path.suffix

        if src_suffix not in SHP_EXTS:
            if save_name is None:
                # copy2(src_path, dst_path)
                return {'src': src_path,
                        'dst': dst_path,
                        'type': FILE}
            else:
                if dst_is_dir:
                    d = dst_path.joinpath(f"{save_name}{src_suffix}")
                else:
                    d = dst_path.with_name(save_name).with_suffix(src_suffix)

                # copy2(src_path, d)
                return {'src': src_path,
                        'dst': d,
                        'type': FILE}
        else:
            all_exist = all([src_path.with_suffix(ext).exists()
                            for ext in SHP_EXTS])

            if all_exist:
                files2copy = []
                for ext in SHP_EXTS:
                    if save_name is None:
                        # copy2(src_path.with_suffix(ext), dst_path)
                        files2copy.append({'src': src_path.with_suffix(ext),
                                           'dst': dst_path,
                                           'type': FILE})
                    else:
                        if dst_is_dir:
                            d = dst_path.joinpath(f"{save_name}{ext}")
                        else:
                            d = dst_path.with_name(save_name).with_suffix(ext)

                        # copy2(src_path.with_suffix(ext), d)
                        files2copy.append({'src': src_path.with_suffix(ext),
                                           'dst': d,
                                           'type': FILE})
                return files2copy
            else:
                log.warning(f"'{str(src)}' missing auxiliary shapefile files.")
                return None


def _copy(src: Union[str, Path],
          dst: Union[str, Path],
          save_name: Union[str, None] = None,
          copymode: str = 'normal'):

    if copymode == 'normal':
        copyfunc = copy2
    else:
        copyfunc = copy

    copyobj = make_paths(src=src, dst=dst, save_name=save_name)

    if copyobj is not None:
        if isinstance(copyobj, dict):
            copyfunc(copyobj["src"], copyobj["dst"])
        else:
            for item in copyobj:
                copyfunc(item["src"], item["dst"])


def copy_file(src: Union[str, Path],
              dst: Union[str, Path],
              save_name: Union[str, None] = None):
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        log.error(f"File '{str(src)}' does not exist.")
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
