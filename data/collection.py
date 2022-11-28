# -*- coding: utf-8 -*-
from __future__ import annotations

import operator
from typing import Iterable, List, Union

from at.data.item import Item


class ItemCollection:
    def __init__(self, items: Union[List[Item], None] = None) -> None:
        self.items: list = items if items else list()
        self.nitems: int = len(self.items) if items else 0

    @classmethod
    def from_dicts(cls, base:Item, dicts:List[dict]):
        _items = list(map(lambda dict_data: base(**dict_data), dicts))

        return cls(items=_items)

    def __str__(self) -> str:
        return f"Collection(items={self.nitems})"

    def add(self, item: Union[Item, Iterable[Item], ItemCollection]) -> None:
        if isinstance(item, (list, tuple, set)):
            for _item in item:
                self.items.append(_item)
                self.nitems += 1
        elif isinstance(item, ItemCollection):
            for _item in item.items:
                self.items.append(_item)
                self.nitems += 1
        else:
            self.items.append(item)
            self.nitems += 1

    def clear(self) -> None:
        self.items = []
        self.nitems = 0

    def get_data(self, rtype: str = 'dict') -> List[dict]:
        if rtype == 'tuple':
            return [it.astuple() for it in self.items]
        return [it.asdict() for it in self.items]

    def is_empty(self):
        return False if self.nitems else True

    def sort(self, key: Union[str, list, tuple]):
        if isinstance(key, str):
            self.items = sorted(self.items, key=operator.attrgetter(key))
        else:
            self.items = sorted(self.items, key=operator.attrgetter(*key))

    def drop_duplicates(self):
        self.items = list(set(self.items))
        self.nitems = len(self.items)
