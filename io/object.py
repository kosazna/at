# -*- coding: utf-8 -*-
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Union

from at.logger import log
from at.text import parse_filters

SHP_EXTS = ('.shp', '.shx', '.dbf')


@dataclass
class CopyObject:
    src: Union[str, Path]
    dst: Union[str, Path]
    directory: bool = False
    shapefile: bool = False
    shapefile_aux: bool = False

    def __post_init__(self):
        self.src = Path(self.src)
        self.dst = Path(self.dst)
        if self.src.is_dir():
            self.directory = True
        else:
            if self.src.suffix == '.shp':
                self.shapefile = True
                self.shapefile_aux = all(
                    [self.src.with_suffix(ext).exists() for ext in SHP_EXTS])

    def __hash__(self) -> int:
        return hash((self.src, self.dst, self.srctype))

    def copy(self,
             copymode: str = 'normal',
             ignore: Optional[Iterable[str]] = None):
        if copymode == 'normal':
            copyfunc = shutil.copy2
        else:
            copyfunc = shutil.copy

        if self.directory:
            if ignore is not None:
                return shutil.copytree(self.src,
                                       self.dst,
                                       copy_function=copyfunc,
                                       ignore=shutil.ignore_patterns(*ignore),
                                       dirs_exist_ok=True)
            else:
                return shutil.copytree(self.src,
                                       self.dst,
                                       copy_function=copyfunc,
                                       dirs_exist_ok=True)
        else:
            if self.shapefile:
                if self.shapefile_aux:
                    dst_is_dir = self.dst.is_dir()

                    for ext in SHP_EXTS:
                        _src = self.src.with_suffix(ext)
                        _dst = self.dst if dst_is_dir else self.dst.with_suffix(
                            ext)
                        copyfunc(_src, _dst)
                    return self.dst
                else:
                    log.warning(f"'{str(self.src)}' missing auxiliary files")
                    return None
            else:
                return copyfunc(self.src, self.dst)


class FilterObject:

    def __init__(self,
                 filters: Union[str, Iterable[str]],
                 recursive: bool = False) -> None:
        self.filters = self._parse_filters(filters, recursive)

    def _parse_filters(self, filters, recursive):
        _filters = []
        __filters = FilterObject._parse(filters)
        for f in __filters:
            if recursive:
                _filters.append(f"**/{f}")
            else:
                _filters.append(f)

        return _filters

    @staticmethod
    def _parse(_filters: Union[str, Iterable[str]]) -> list:
        if isinstance(_filters, str):
            __filters = parse_filters(_filters)
        else:
            __filters = _filters

        return __filters if __filters is not None else list()

    def __iter__(self):
        return iter(self.filters)

    def __len__(self):
        return len(self.filters)

    @classmethod
    def contains(cls,
                 filters: Union[str, Iterable[str]],
                 recursive: bool = False) -> FilterObject:
        _filters = []
        __filters = FilterObject._parse(filters)

        for f in __filters:
            _filters.append(f"*{f}*")

        return cls(filters=_filters, recursive=recursive)

    @classmethod
    def startswith(cls,
                   filters: Union[str, Iterable[str]],
                   recursive: bool = False) -> FilterObject:
        _filters = []
        __filters = FilterObject._parse(filters)

        for f in __filters:
            _filters.append(f"{f}*")

        return cls(filters=_filters, recursive=recursive)

    @classmethod
    def endswith(cls,
                 filters: Union[str, Iterable[str]],
                 recursive: bool = False) -> FilterObject:
        _filters = []
        __filters = FilterObject._parse(filters)

        for f in __filters:
            _filters.append(f"*{f}")

        return cls(filters=_filters, recursive=recursive)

    def search(self, directory: Union[str, Path], keep: Optional[str] = None):
        dir_path = Path(directory)
        files: List[Path] = []

        if self.filters:
            for f in self.filters:
                files.extend(list(dir_path.glob(f)))
        else:
            files.extend(list(dir_path.iterdir()))

        if keep == 'files':
            return [p for p in files if p.is_file()]
        elif keep == 'dirs':
            return [p for p in files if p.is_dir()]
        else:
            return files
