# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Union


def load_sql_queries(folder: Union[str, Path]) -> Dict[str, str]:
    queries = {}
    for p in Path(folder).glob('*.sql'):
        stem = p.stem
        queries[stem] = p.read_text(encoding='utf-8')

    return queries


def load_create_queries(folder: Union[str, Path]) -> List[QueryObject]:
    queries = []
    for p in Path(folder).glob('*.sql'):
        queries.append(QueryObject(p.read_text(encoding='utf-8')))

    return queries


@dataclass
class QueryObject:
    query: str
    fetch: str = 'one'  # 'one', 'singlerow', 'multirow', 'singlecol'
    cols: bool = False
    default: Any = None
    params: Union[dict, None] = None
    data: Union[List[tuple], None] = None

    def __post_init__(self):
        if ':' in self.query:
            params = {}
            parameters = [p.strip(':') for p in re.findall(r':\w+', self.query)]
            for p in parameters:
                params[p] = None
            self.params = params

    def set(self, **kwargs: Any) -> QueryObject:
        if 'datastream' in kwargs:
            self.data = kwargs['datastream']
        else:
            for param in self.params:
                value = kwargs.get(param, None)
                if value is None:
                    raise ValueError(f"'{param}' was not given a value.")
                else:
                    self.params[param] = value

        return self
