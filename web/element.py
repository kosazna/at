# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Element:
    name: Optional[str] = None
    tag: Optional[str] = None
    _class: Optional[str] = None
    _id: Optional[str] = None
    _xpath: Optional[str] = None
    attribute: Optional[str] = None
    return_text: bool = True
    loc: Optional[int] = None
    default: Optional[str] = None
    child: Optional[Element] = None
    parent: Optional[Element] = None

    @property
    def props(self):
        _attrs = {}
        if self._class is not None:
            _attrs['class'] = self._class
        if self._id is not None:
            _attrs['id'] = self._id

        return _attrs

    def has_children(self):
        return False if self.child is None else True
