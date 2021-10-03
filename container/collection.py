# -*- coding: utf-8 -*-

import operator
from typing import List, Union

from .item import Item


class ItemCollection:
    def __init__(self, items: Union[List[Item], None] = None) -> None:
        self.items: list = items if items else list()
        self.types: Union[dict, None] = items[0].types() if items else None
        self.nitems: int = len(self.items) if items else 0

    def __str__(self) -> str:
        return f"Collection(items={self.nitems})"

    def add(self, item: Item) -> None:
        self.items.append(item)
        self.nitems += 1
        if self.types is None:
            self.types = item.types()

    def clear(self) -> None:
        self.items = []
        self.types = None
        self.nitems = 0

    def get_data(self, rtype: str = 'dict') -> List[dict]:
        if rtype == 'tuple':
            return [it.astuple() for it in self.items]
        return [it.asdict() for it in self.items]

    def get_types(self) -> Union[dict, None]:
        return self.types

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
