# -*- coding: utf-8 -*-

from contextlib import closing
from pathlib import Path
from sqlite3 import Connection, Cursor, Error, connect
from subprocess import Popen
from typing import List, Union

from at.sql.query import QueryObject


def select(cursor: Cursor, query_obj: QueryObject):
    if query_obj.params is None:
        cursor.execute(query_obj.query)
    else:
        cursor.execute(query_obj.query, query_obj.params)

    if query_obj.fetch == 'one':
        r = cursor.fetchone()
        return query_obj.default if r is None else r[0]
    elif query_obj.fetch == 'singlerow':
        r = cursor.fetchone()
        if r is not None and query_obj.cols == True:
            cols = [d[0] for d in cursor.description]
            return cols, r
        else:
            return query_obj.default if r is None else r
    else:
        r = cursor.fetchall()
        if query_obj.fetch == 'multirow':
            if r is not None and query_obj.cols == True:
                cols = [d[0] for d in cursor.description]
                return cols, r
            else:
                return query_obj.default if r is None else r
        elif query_obj.fetch == 'singlecol':
            content = [i[0] for i in r]
            return query_obj.default if r is None else content


def update(connection: Connection, cursor: Cursor, query_obj: QueryObject):
    cursor.execute(query_obj.query, query_obj.params)
    connection.commit()


def insert(connection: Connection, cursor: Cursor, query_obj: QueryObject):
    if query_obj.data is not None:
        cursor.executemany(query_obj.query, query_obj.data)
    else:
        cursor.execute(query_obj.query, query_obj.params)
    connection.commit()


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
