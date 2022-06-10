# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, List, Union


@dataclass
class QueryObject:
    query: str
    fetch: str = 'one'  # 'one', 'row', 'rows', 'col'
    colname: bool = False
    default: Any = None
    params: Union[dict, None] = None
    data: Union[List[tuple], None] = None

    def __post_init__(self):
        result_params = re.search(r'{.*}', self.query)
        if result_params is not None:
            result_params_dict = eval(result_params.group())
            if result_params_dict:
                self.attrs(**result_params_dict)
            self.query = re.sub(r'--{.*}', '', self.query).strip()

        if ':' in self.query:
            params = {}
            parameters = [p.strip(':') for p in re.findall(r':\w+', self.query)]
            for p in parameters:
                params[p] = None
            self.params = params

    def __str__(self) -> str:
        return f"<Query(fetch={self.fetch}, colname={self.colname}, default={self.default}, params={self.params})>\n{self.query}\n"

    def attrs(self, **kwargs: Any) -> QueryObject:
        for param in self.__dict__:
            value = kwargs.get(param, None)
            if value is not None:
                self.__dict__[param] = value

        return self

    def set(self, **kwargs: Any) -> QueryObject:
        if 'datastream' in kwargs:
            self.data = kwargs['datastream']
        else:
            if self.params is not None:
                for param in self.params:
                    value = kwargs.get(param, None)
                    if value is None:
                        raise ValueError(f"'{param}' was not given a value.")
                    else:
                        self.params[param] = value

        return self
