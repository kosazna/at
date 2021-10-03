# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Union


@dataclass
class Element:
    NAME: Union[str, None] = None
    TAG: Union[str, None] = None
    CLASS: Union[str, None] = None
    ID: Union[str, None] = None
    XPATH: Union[str, None] = None
    TEXT: bool = True
    ATTRIBUTE: Union[str, None] = None
    SUB: Union[Element, None] = None
    LOC: Union[int, None] = None
    DEFAULT: Union[str, None] = None

    @property
    def attrs(self):
        _attrs = {}
        if self.CLASS is not None:
            _attrs['class'] = self.CLASS
        if self.ID is not None:
            _attrs['id'] = self.ID

        return _attrs
