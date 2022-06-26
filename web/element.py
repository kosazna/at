# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Optional, Union, Iterable, Any


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
    default: Optional[Any] = None
    children: Optional[Union[Element, Iterable[Element]]] = None

    def __repr__(self):
        _attrs_set = asdict(self)
        description = ''
        for _attr in _attrs_set:
            if _attrs_set[_attr] is not None:
                if description:
                    description += ", "
                description += f"{_attr}='{_attrs_set[_attr]}'"
        return f"Element({description})"

    def __str__(self):
        _attrs_set = asdict(self)
        description = ''
        for _attr in _attrs_set:
            if _attrs_set[_attr] is not None:
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

    @classmethod
    def from_dict(cls, data: dict) -> Element:
        children = data.pop('children', None)

        if children is None:
            return cls(**data)
        else:
            if isinstance(children, (list, tuple)):
                _iterable = [cls.from_dict(child_data)
                             for child_data in children]
                return cls(**data, children=_iterable)
            else:
                return cls(**data, children=cls.from_dict(children))

    def has_children(self) -> bool:
        return False if self.children is None else True

    def selenium_props(self) -> dict:
        if self.css_selector is not None:
            return {
                "by": 'css selector',
                "value": self.css_selector
            }
        else:
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

        if self.tag_name is not None:
            return {
                "name": self.tag_name,
                "attrs": _attrs
            }
        else:
            raise ValueError("Tag property must be set for bs4")


@dataclass
class ElementStore:
    cookies: Optional[Element] = None
    paginator: Optional[Element] = None
    data: Optional[Element] = None

    @classmethod
    def from_json_config(cls, json_config_data: dict) -> ElementStore:
        if 'interaction' in json_config_data:
            interaction = json_config_data.pop('interaction')
            if 'cookies' in interaction:
                cookies = interaction.pop('cookies')
                _cookies = Element.from_dict(cookies)
            if 'paginator' in interaction:
                paginator = interaction.pop('paginator')
                _paginator = Element.from_dict(paginator)
        if 'data' in json_config_data:
            data_elems = json_config_data.pop('data')
            _data = Element.from_dict(data_elems)

        return cls(_cookies, _paginator, _data)
