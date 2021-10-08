# -*- coding: utf-8 -*-

from contextlib import closing
from pathlib import Path
from sqlite3 import Error, connect
from subprocess import Popen
from typing import List, Union

from at.sql.action import insert, select, update
from at.sql.query import QueryObject


class SQLiteEngine:
    def __init__(self,
                 db: Union[str, Path],
                 create_queries: Union[List[QueryObject], None] = None) -> None:
        self.db = str(db)
        self.create_queries = create_queries
        self._check_db_exists()

    def _check_db_exists(self):
        if Path(self.db).exists():
            pass
        else:
            if self.create_queries is not None:
                with closing(connect(self.db)) as con:
                    with closing(con.cursor()) as cur:
                        for query_obj in self.create_queries:
                            cur.execute(query_obj.query)

    def open_db(self, executable: Union[str, Path]):
        if Path(executable).exists():
            Popen([str(executable), self.db])
        else:
            print('Instal DB Browser (SQLite) to view database.')

    def update(self, query_obj: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    update(connection=con, cursor=cur, query_obj=query_obj)
        except Error as e:
            print(f"{str(e)} from {self.db}")

    def insert(self, query_obj: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    insert(connection=con, cursor=cur, query_obj=query_obj)
        except Error as e:
            print(f"{str(e)} from {self.db}")

    def select(self, query_obj: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    return select(cursor=cur, query_obj=query_obj)
        except Error as e:
            print(f"{str(e)} from {self.db}")
