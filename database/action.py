# -*- coding: utf-8 -*-

from contextlib import closing
from sqlite3 import Connection, Cursor, Error, connect
from typing import Union

from at.logger import log
from at.database.object import QueryObject


def select(cursor: Cursor, query_obj: QueryObject):
    if query_obj.params is None:
        cursor.execute(query_obj.query)
    else:
        cursor.execute(query_obj.query, query_obj.params)

    if query_obj.fetch == 'one':
        r = cursor.fetchone()
        return query_obj.default if r is None else r[0]
    elif query_obj.fetch == 'row':
        r = cursor.fetchone()
        if r is not None and query_obj.colname == True:
            cols = [d[0] for d in cursor.description]
            return tuple(cols), r
        else:
            return query_obj.default if r is None else r
    else:
        r = cursor.fetchall()
        if query_obj.fetch == 'rows':
            if r is not None and query_obj.colname == True:
                cols = [d[0] for d in cursor.description]
                return tuple(cols), r
            else:
                return query_obj.default if r is None else r
        elif query_obj.fetch == 'col':
            content = [i[0] for i in r]
            return query_obj.default if r is None else tuple(content)


def update(connection: Connection, cursor: Cursor, query_obj: QueryObject):
    cursor.execute(query_obj.query, query_obj.params)
    connection.commit()


def insert(connection: Connection, cursor: Cursor, query_obj: QueryObject):
    if query_obj.data is not None:
        cursor.executemany(query_obj.query, query_obj.data)
    else:
        cursor.execute(query_obj.query, query_obj.params)
    connection.commit()


def db_select(db: str, query_obj: QueryObject):
    try:
        with closing(connect(db)) as con:
            with closing(con.cursor()) as cur:
                return select(cursor=cur, query_obj=query_obj)
    except Error as e:
        log.error(f"{str(e)} from {db}")


def db_update(db: str, query_obj: QueryObject):
    try:
        with closing(connect(db)) as con:
            with closing(con.cursor()) as cur:
                update(connection=con, cursor=cur, query_obj=query_obj)
    except Error as e:
        log.error(f"{str(e)} from {db}")


def db_insert(db: str, query_obj: QueryObject):
    try:
        with closing(connect(db)) as con:
            with closing(con.cursor()) as cur:
                insert(connection=con, cursor=cur, query_obj=query_obj)
    except Error as e:
        log.error(f"{str(e)} from {db}")


def db_script(db: str, script: Union[str, QueryObject]):
    with closing(connect(db)) as con:
        with closing(con.cursor()) as cur:
            if isinstance(script, QueryObject):
                cur.executescript(script.query)
            else:
                cur.executescript(script)
