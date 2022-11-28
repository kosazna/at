# -*- coding: utf-8 -*-

from dataclasses import asdict, astuple, dataclass, make_dataclass, field


@dataclass
class Item:
    def asdict(self) -> dict:
        return asdict(self)

    def astuple(self) -> tuple:
        return astuple(self)


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
