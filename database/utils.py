# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Dict, Union

from at.database.query import Query


def load_app_queries(folder: Union[str, Path]) -> Dict[str, Query]:
    queries = {}

    for p in Path(folder).glob('*.sql'):
        queries[p.stem] = Query.from_file(p)

    return queries
