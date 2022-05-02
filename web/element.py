# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Element:
    name: Optional[str] = None
    tag_name: Optional[str] = None
    class_name: Optional[str] = None
    id: Optional[str] = None
    xpath: Optional[str] = None
    css_selector: Optional[str] = None
    partial_link_text: Optional[str] = None
    link_text: Optional[str] = None
    attribute: Optional[str] = None
    loc: Optional[int] = None
    default: Optional[str] = None
    child: Optional[Element] = None
    parent: Optional[Element] = None
    html: Optional[str] = None

    def __repr__(self):
        _attrs_set = asdict(self)
        description = ''
        for _attr in _attrs_set:
            if _attrs_set[_attr] is not None and _attr != 'html':
                if description:
                    description += ", "
                description += f"{_attr}='{_attrs_set[_attr]}'"
        return f"Element({description})"

    @classmethod
    def from_text(cls, text: str) -> Element:
        _attr, _value = text.split('=', maxsplit=1)

        _attr = _attr.replace(' ', '_')

        _el = Element()
        _el.__dict__[_attr] = _value

        return _el

    def set_html(self, html_source: str) -> Element:
        self.html = html_source
        return self

    def has_children(self) -> bool:
        return False if self.child is None else True

    def selenium_props(self) -> dict:
        _by = None
        _value = None

        _attrs_set = asdict(self)
        for _attr in _attrs_set:
            if _attrs_set[_attr] is not None:
                _by = _attr.replace('_', ' ')
                _value = _attrs_set[_attr]
                break

        if _by is not None:
            return {
                "by": _by,
                "value": _value
            }
        else:
            raise ValueError(
                "At least an element property must be set for selenium")

    def bs4_props(self) -> dict:
        _attrs = {}

        if self.class_name is not None:
            _attrs['class'] = self.class_name
        if self.id is not None:
            _attrs['id'] = self.id

        if self.tag is not None:
            return {
                "name": self.tag,
                "attrs": _attrs
            }
        else:
            raise ValueError("Tag property must be set for bs4")
