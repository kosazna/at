# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Dict, Union

from at.sql.object import QueryObject


def load_app_queries(folder: Union[str, Path]) -> Dict[str, QueryObject]:
    queries = {}

    for p in Path(folder).glob('*.sql'):
        queries[p.stem] = QueryObject(p.read_text(encoding='utf-8'))

    return queries
