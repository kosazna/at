# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, List, Union


@dataclass
class QueryObject:
    query: str
    data: Union[dict, List[tuple]]
    kind: str = 'data' # 'data', 'datastream'
    fetch: str = 'one' # 'one', 'singlerow', 'multirow', 'singlecol'
    cols: bool = False
    default: Any = None

    def __post_init__(self):
        if isinstance(self.data, list):
            self.kind = 'datastream'


a = QueryObject('', {}, fetch='all')
print(a)
