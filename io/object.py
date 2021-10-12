# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path
from shutil import copy, copy2, copytree
from typing import Union

from at.logger import log

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
                self.shapefile == True
                self.shapefile_aux = all(
                    [self.src.with_suffix(ext).exists() for ext in SHP_EXTS])

    def __hash__(self) -> int:
        return hash((self.src, self.dst, self.srctype))

    def copy(self, copymode: str = 'normal'):
        if copymode == 'normal':
            copyfunc = copy2
        else:
            copyfunc = copy

        if self.directory:
            return copytree(self.src, self.dst, copy_function=copyfunc)
        else:
            if self.shapefile:
                if self.shapefile_aux:
                    dst_is_dir = self.dst.is_dir()

                    for ext in SHP_EXTS:
                        _src = self.src.with_suffix(ext)
                        _dst = self.dst if dst_is_dir else self.dst.with_suffix(
                            ext)
                        return copyfunc(_src, _dst)
                else:
                    log.warning(f"'{str(self.src)}' missing auxiliary files")
                    return None
            else:
                return copyfunc(self.src, self.dst)
