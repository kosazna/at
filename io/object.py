# -*- coding: utf-8 -*-
from __future__ import annotations
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Union

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

    def copy(self, copymode: str = 'normal'):
        if copymode == 'normal':
            copyfunc = shutil.copy2
        else:
            copyfunc = shutil.copy

        if self.directory:
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
        self.filters = filters
        self.recursive = recursive
        self._post_init()


    def _post_init(self):
        filters = []
        _filters = FilterObject._parse(self.filters)
        print(_filters)
        for f in _filters:
            if self.recursive:
                filters.append(f"**/{f}")
            else:
                filters.append(f)

        self.filters = filters

    @classmethod
    def contains(cls,
                 filters: Union[str, Iterable[str]],
                 recursive: bool = False) -> FilterObject:
        _filters = []
        __filters = FilterObject._parse(filters)

        for f in __filters:
            _filters.append(f"*{f}*")

        return cls(filters=_filters, recursive=recursive)

    @staticmethod
    def _parse(_filters: Union[str, Iterable[str]]) -> list:
        if isinstance(_filters, str):
            __filters = parse_filters(_filters)
        else:
            __filters = _filters

        return __filters

    def __iter__(self):
        return iter(self.filters)

    def __len__(self):
        return len(self.filters)

a = FilterObject.contains("22003|22022", recursive=True)
for i in a:
    print(i)
