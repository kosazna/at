# -*- coding: utf-8 -*-

from pathlib import Path
from subprocess import Popen
from typing import Union

from at.logger import log
from at.path import PathEngine
from at.sql.action import db_insert, db_script, db_select, db_update
from at.sql.utils import QueryObject, load_app_queries
from at.state import State


class SQLiteEngine:
    def __init__(self,
                 db: Union[str, Path],
                 app_paths: PathEngine) -> None:
        self.db = str(db)
        self.paths = app_paths
        self.init_queries = load_app_queries(self.paths.get_init_sql())
        self._db_init()

    def _db_init(self):
        if Path(self.db).exists():
            if self.init_queries is not None:
                for query_name, query in self.init_queries.items():
                    if query_name.startswith('new'):
                        db_script(self.db, query)
                        sql_name = f"{query_name}.sql"
                        sql_folder = self.paths.get_init_sql(True)
                        sql_file = sql_folder.joinpath(sql_name)
                        sql_file.unlink(missing_ok=True)
        else:
            if self.init_queries is not None:
                for query_name, query in self.init_queries.items():
                    if query_name.startswith('init'):
                        db_script(self.db, query)

    def open_db(self, executable: Union[str, Path]):
        if Path(executable).exists():
            Popen([str(executable), self.db])
        else:
            log.warning('To view database install DB Browser (SQLite) (64-bit)')

    def update(self, query_obj: QueryObject):
        db_update(db=self.db, query_obj=query_obj)

    def insert(self, query_obj: QueryObject):
        db_insert(db=self.db, query_obj=query_obj)

    def select(self, query_obj: QueryObject):
        return db_select(db=self.db, query_obj=query_obj)

    def script(self, query_obj: QueryObject):
        db_script(db=self.db, script=query_obj)

    def load_state(self):
        pass

    def save_state(self, state: State):
        pass
