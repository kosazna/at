# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Optional, Union, Iterable, Any
from pathlib import Path
from at.io.utils import write_json
from at.utils import purge_dict


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
    many: bool = False
    loc: Optional[int] = None
    default: Optional[Any] = None
    children: Optional[Union[Element, Iterable[Element]]] = None
    parent: Optional[str] = None

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

    def to_dict(self) -> dict:
        _attrs_set = asdict(self)
        props = {}
        for _attr, _value in _attrs_set.items():
            if _attr == 'children' and _value is not None:
                if isinstance(_value, (list, tuple)):
                    children = [purge_dict(child_data) for child_data in _value]
                else:
                    children = purge_dict(_value)
                props[_attr] = children
            else:
                if _value is not None:
                    props[_attr] = _value

        return props

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
    filters: Optional[Element] = None
    follow: Optional[Element] = None

    @classmethod
    def from_json_config(cls, json_config_elements: dict) -> ElementStore:
        _cookies = None
        _paginator = None
        _data = None
        _filters = None
        _follow = None

        if 'interaction' in json_config_elements:
            interaction = json_config_elements.pop('interaction')
            if 'cookies' in interaction:
                cookies = interaction.pop('cookies')
                _cookies = Element.from_dict(cookies)
            if 'paginator' in interaction:
                paginator = interaction.pop('paginator')
                _paginator = Element.from_dict(paginator)
        if 'data' in json_config_elements:
            data_elems = json_config_elements.pop('data')
            _data = Element.from_dict(data_elems)
        if 'filters' in json_config_elements:
            filter_elems = json_config_elements.pop('filters')
            _filters = Element.from_dict(filter_elems)
        if 'follow' in json_config_elements:
            follow_elems = json_config_elements.pop('follow')
            _follow = Element.from_dict(follow_elems)

        return cls(_cookies, _paginator, _data, _filters, _follow)

    def to_json_config(self, filepath: Union[str, Path]):
        config = {
            'elements': {
                'interaction': {},
                'filters': None,
                'data': None,
                'follow': None
            }
        }

        if self.cookies is not None:
            config['elements']['interaction']['cookies'] = self.cookies.to_dict()
        if self.paginator is not None:
            config['elements']['interaction']['paginator'] = self.paginator.to_dict()
        if self.data is not None:
            config['elements']['data'] = self.data.to_dict()
        if self.filters is not None:
            config['elements']['filters'] = self.filters.to_dict()
        if self.follow is not None:
            config['elements']['follow'] = self.follow.to_dict()

        write_json(filepath=filepath, data=config)
