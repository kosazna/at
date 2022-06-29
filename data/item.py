# -*- coding: utf-8 -*-

from dataclasses import asdict, astuple, dataclass, make_dataclass, field
from typing import Union, Optional


def _get_types_from_template(dc_template) -> Union[dict, None]:
    cast_map = {'str': 'string',
                'int': 'int64',
                'float': 'float64'}

    if dc_template is not None:
        dctypes = dc_template.__annotations__
        dtypes = {}
        for key, value in dctypes.items():
            value_name = value.__name__
            try:
                dtypes[key] = cast_map[value_name]
            except KeyError:
                dtypes[key] = value_name
        return dtypes
    return None


@dataclass
class Item:
    def asdict(self) -> dict:
        return asdict(self)

    def astuple(self) -> tuple:
        return astuple(self)

    def types(self) -> Union[dict, None]:
        return _get_types_from_template(self)


def item_factory(cls_name: str, fields: dict):
    _fields = []
    for _name, _specs in fields.items():
        _type = _specs.get('type')
        _default = _specs.get('default')

        _fields.append((_name, _type, field(default=_default)))

    return make_dataclass(cls_name=cls_name, fields=_fields, bases=(Item,))


@dataclass
class ExampleItem(Item):
    sku: str
    new_price: float
    old_price: float

    def __post_init__(self):
        pass

    def __hash__(self) -> int:
        return hash((self.sku, self.new_price, self.old_price))
