# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path
from shutil import copy, copy2, copytree
from typing import Union

from at.input import DIR, FILE


@dataclass
class CopyObject:
    src: Union[str, Path]
    dst: Union[str, Path]
    srctype: str = ''

    def __post_init__(self):
        if Path(self.src).is_dir():
            self.srctype = DIR
        else:
            self.srctype = FILE

    def __hash__(self) -> int:
        return hash((self.src, self.dst, self.srctype))

    def copy(self, copymode: str = 'normal'):
        if copymode == 'normal':
            copyfunc = copy2
        else:
            copyfunc = copy

        if self.srctype == DIR:
            copytree(self.src, self.dst, copy_function=copyfunc)
        else:
            copyfunc(self.src, self.dst)
