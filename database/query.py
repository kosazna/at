# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Union

SQLITE_PARAM_REGEX = r':\w+'
MYSQL_PARAM_REGEX = r'\%\((\w*)\)s'
UNIVERSAL_TABLE_NAME = r'<%table_name%>'


@dataclass
class Query:
    sql: str
    fetch: str = 'one'  # 'one', 'row', 'rows', 'col'
    columns: bool = False
    default: Any = None
    params: Union[dict, None] = None
    data: Union[List[tuple], None] = None

    @classmethod
    def from_file(cls, filepath: Union[str, Path]) -> Query:
        _path = Path(filepath)
        _query = _path.read_text(encoding='utf-8')

        return cls(sql=_query)

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
        if re.search(UNIVERSAL_TABLE_NAME, self.sql):
            table_name = kwargs.get("table_name", None)
            if table_name is not None:
                self.sql = re.sub(UNIVERSAL_TABLE_NAME, table_name, self.sql)
            else:
                raise ValueError(f"<table_name> parameter was not provided")
                
        if 'datastream' in kwargs:
            self.data = kwargs['datastream']
        else:
            if self.params is not None:
                for param in self.params:
                    value = kwargs.get(param, None)
                    self.params[param] = value
        return self
