# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, List, Union
from pathlib import Path

SQLITE_PARAM_REGEX = r':\w+'
MYSQL_PARAM_REGEX = r'\%\((\w*)\)s'


@dataclass
class Query:
    sql: str
    fetch: str = 'one'  # 'one', 'row', 'rows', 'col'
    columns: bool = False
    default: Any = None
    params: Union[dict, None] = None
    data: Union[List[tuple], None] = None

    @classmethod
    def from_file(cls, filepath: Union[str, Path]):
        _path = Path(filepath)
        _query = _path.read_text(encoding='utf-8')

        return cls(_query)

    def __post_init__(self):
        result_params = re.search(r'{.*}', self.sql)
        if result_params is not None:
            result_params_dict = eval(result_params.group())
            if result_params_dict:
                self.attrs(**result_params_dict)
            self.sql = re.sub(r'--{.*}', '', self.sql).strip()

        mysql_params = re.findall(MYSQL_PARAM_REGEX, self.sql)
        sqlite_params = re.findall(SQLITE_PARAM_REGEX, self.sql)

        if mysql_params:
            params = {}
            for p in mysql_params:
                params[p] = None
            self.params = params
        elif sqlite_params:
            params = {}
            parameters = [p.strip(':') for p in sqlite_params]
            for p in parameters:
                params[p] = None
            self.params = params

    def __str__(self) -> str:
        return f"<Query(fetch={self.fetch}, colname={self.columns}, default={self.default}, params={self.params})>\n{self.sql}\n"

    def attrs(self, **kwargs: Any) -> Query:
        for param in self.__dict__:
            value = kwargs.get(param, None)
            if value is not None:
                self.__dict__[param] = value

        return self

    def set(self, **kwargs: Any) -> Query:
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
