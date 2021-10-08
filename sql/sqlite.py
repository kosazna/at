# -*- coding: utf-8 -*-

from contextlib import closing
from pathlib import Path
from sqlite3 import Connection, Cursor, Error, connect
from subprocess import Popen
from typing import List, Union

from at.sql.object import QueryObject, load_sql_queries


def select(cursor: Cursor, query_object: QueryObject):
    if query_object.params is None:
        cursor.execute(query_object.query)
    else:
        cursor.execute(query_object.query, query_object.params)

    if query_object.fetch == 'one':
        r = cursor.fetchone()
        return query_object.default if r is None else r[0]
    elif query_object.fetch == 'singlerow':
        r = cursor.fetchone()
        if r is not None and query_object.cols == True:
            cols = [d[0] for d in cursor.description]
            return cols, r
        else:
            return query_object.default if r is None else r
    else:
        r = cursor.fetchall()
        if query_object.fetch == 'multirow':
            if r is not None and query_object.cols == True:
                cols = [d[0] for d in cursor.description]
                return cols, r
            else:
                return query_object.default if r is None else r
        elif query_object.fetch == 'singlecol':
            content = [i[0] for i in r]
            return query_object.default if r is None else content


def update(connection: Connection, cursor: Cursor, query_object: QueryObject):
    cursor.execute(query_object.query, query_object.params)
    connection.commit()


def insert(connection: Connection, cursor: Cursor, query_object: QueryObject):
    if query_object.data is not None:
        cursor.executemany(query_object.query, query_object.data)
    else:
        cursor.execute(query_object.query, query_object.params)
    connection.commit()


class SQLiteEngine:
    def __init__(self,
                 db: Union[str, Path],
                 create_queries: Union[List[str], None] = None) -> None:
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
                        for query in self.create_queries:
                            cur.execute(query)

    def open_db(self, executable: Union[str, Path]):
        if Path(executable).exists():
            Popen([str(executable), self.db])
        else:
            print('Instal DB Browser (SQLite) to view database.')

    def update(self, query_object: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    update(connection=con, cursor=cur,
                           query_object=query_object)
        except Error as e:
            print(str(e) + " from " + self.db)

    def insert(self, query_object: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    insert(connection=con, cursor=cur,
                           query_object=query_object)
        except Error as e:
            print(str(e) + " from " + self.db)

    def select(self, query_object: QueryObject):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    return select(cursor=cur, query_object=query_object)
        except Error as e:
            print(str(e) + " from " + self.db)


if __name__ == '__main__':
    engine = SQLiteEngine("C:/Users/aznavouridis.k/.atcrawl/atcrawl.db")

    queries = load_sql_queries("D:/.temp/.dev/.aztool/atcrawl/static/queries")

    quer = 'update_job'

    print(engine.insert(QueryObject(queries[quer]).set(site='antallaktikaonline.gr',
                                                       site_counter=10,
                                                       collected_at='2021-10-08 12:51:11',
                                                       parameters="{'meta0': '', 'meta1': '', 'meta2': '', 'meta3': '', 'meta4': '', 'meta5': '', 'meta6': '', 'meta7': '', 'meta_check': True}",
                                                       records=1080,
                                                       out_file="D:/.temp/.dev/.aztool/atcrawl/static/queries")))
