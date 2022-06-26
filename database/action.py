# -*- coding: utf-8 -*-

from contextlib import closing
from typing import Union

from at.logger import log
from at.database.query import Query


def select(cursor, query: Query):
    if query.params is None:
        cursor.execute(query.sql)
    else:
        cursor.execute(query.sql, query.params)

    if query.fetch == 'one':
        r = cursor.fetchone()
        return query.default if r is None else r[0]
    elif query.fetch == 'row':
        r = cursor.fetchone()
        if r is not None and query.columns == True:
            cols = [d[0] for d in cursor.description]
            return tuple(cols), r
        else:
            return query.default if r is None else r
    else:
        r = cursor.fetchall()
        if query.fetch == 'rows':
            if r is not None and query.columns == True:
                cols = [d[0] for d in cursor.description]
                return tuple(cols), r
            else:
                return query.default if r is None else r
        elif query.fetch == 'col':
            content = [i[0] for i in r]
            return query.default if r is None else tuple(content)


def update(connection, cursor, query: Query):
    cursor.execute(query.sql, query.params)
    connection.commit()


def insert(connection, cursor, query: Query):
    if query.data is not None:
        cursor.executemany(query.sql, query.data)
    else:
        cursor.execute(query.sql, query.params)
    connection.commit()


def db_select(connection, query: Query):
    try:
        with closing(connection.cursor()) as cur:
            return select(cursor=cur, query=query)
    except Exception as e:
        log.error(str(e))


def db_update(connection, query: Query):
    try:
        with closing(connection.cursor()) as cur:
            update(connection=connection, cursor=cur, query=query)
    except Exception as e:
        log.error(str(e))


def db_insert(connection, query: Query):
    try:
        with closing(connection.cursor()) as cur:
            insert(connection=connection, cursor=cur, query=query)
    except Exception as e:
        log.error(str(e))


def db_script(connection, script: Union[str, Query]):
    with closing(connection.cursor()) as cur:
        if isinstance(script, Query):
            cur.executescript(script.sql)
        else:
            cur.executescript(script)
