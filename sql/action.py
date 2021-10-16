# -*- coding: utf-8 -*-

from sqlite3 import Connection, Cursor

from at.sql.object import QueryObject


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
            return tuple(cols), r
        else:
            return query_obj.default if r is None else r
    else:
        r = cursor.fetchall()
        if query_obj.fetch == 'multirow':
            if r is not None and query_obj.cols == True:
                cols = [d[0] for d in cursor.description]
                return tuple(cols), r
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
