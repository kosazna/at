# -*- coding: utf-8 -*-

from contextlib import closing
from pathlib import Path
from sqlite3 import Error, connect
from subprocess import Popen
from typing import Dict, List, Union

from at.logger import log
from at.sql.action import insert, select, update, executescript
from at.sql.utils import QueryObject
from at.state import State
from at.path import PathEngine


def load_app_queries(folder: Union[str, Path]) -> Dict[str, str]:
    queries = {}
    for p in Path(folder).glob('*.sql'):
        stem = p.stem
        queries[stem] = p.read_text(encoding='utf-8')

    return queries


class SQLiteEngine:
    def __init__(self,
                 db: Union[str, Path],
                 app_paths: PathEngine) -> None:
        self.db = str(db)
        self.paths = app_paths
        self.init_queries = load_app_queries(self.paths.get_init_sql())
        self._check_db_exists()

    def _check_db_exists(self):
        if Path(self.db).exists():
            if self.init_queries is not None:
                for query_name, query in self.init_queries.items():
                    if query_name.startswith('new'):
                        executescript(self.db, query)
                        sql_name = f"{query_name}.sql"
                        sql_folder = self.paths.get_init_sql(True)
                        sql_file = sql_folder.joinpath(sql_name)
                        sql_file.unlink(missing_ok=True)
        else:
            if self.init_queries is not None:
                for query_name, query in self.init_queries.items():
                    if query_name.startswith('init'):
                        executescript(self.db, query)

    def open_db(self, executable: Union[str, Path]):
        if Path(executable).exists():
            Popen([str(executable), self.db])
        else:
            log.info('Instal DB Browser (SQLite) to view database.')

    def update(self, query_obj: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    update(connection=con, cursor=cur, query_obj=query_obj)
        except Error as e:
            log.error(f"{str(e)} from {self.db}")

    def insert(self, query_obj: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    insert(connection=con, cursor=cur, query_obj=query_obj)
        except Error as e:
            log.error(f"{str(e)} from {self.db}")

    def select(self, query_obj: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    return select(cursor=cur, query_obj=query_obj)
        except Error as e:
            log.error(f"{str(e)} from {self.db}")

    def load_state(self):
        pass

    def save_state(self, state: State):
        pass
