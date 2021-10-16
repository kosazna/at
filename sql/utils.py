# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Union

from at.sql.object import QueryObject


def load_app_queries(folder: Union[str, Path]) -> Dict[str, str]:
    queries = {}
    for p in Path(folder).glob('*.sql'):
        stem = p.stem
        queries[stem] = p.read_text(encoding='utf-8')

    return queries


def load_init_queries(folder: Union[str, Path]) -> List[QueryObject]:
    queries = []
    for p in Path(folder).glob('*.sql'):
        queries.append(QueryObject(p.read_text(encoding='utf-8')))

    return queries


def load_settings_queries(folder: Union[str, Path]):
    queries = {}
    for p in Path(folder).glob('*.sql'):
        stem = p.stem
        queries[stem] = p.read_text(encoding='utf-8')
