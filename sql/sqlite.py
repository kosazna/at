# -*- coding: utf-8 -*-

from contextlib import closing
from datetime import datetime
from pathlib import Path
from sqlite3 import Connection, Cursor, Error, connect
from subprocess import Popen
from typing import List, Union

from at.sql.object import QueryObject


def select(cursor: Cursor, query_object: QueryObject):
    cursor.execute(query_object.query, query_object.data)

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
    cursor.execute(query_object.query, query_object.data)
    connection.commit()


def insert(connection: Connection, cursor: Cursor, query_object: QueryObject):
    if query_object.kind == 'datastream':
        cursor.executemany(query_object.query, query_object.data)
    else:
        cursor.execute(query_object.query, query_object.data)
    connection.commit()


class AtcrawlSQL:
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
        Popen([str(executable), self.db])

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

    # def backup(self, process: str, parameters: dict, collection: ItemCollection):
    #     table = process.split('.')[0]
    #     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(get_site_counter, {'site': process})
    #                 site_counter = cur.fetchone()[0] + 1

    #                 params = {'site': process,
    #                           'site_counter': site_counter,
    #                           'collected_at': date,
    #                           'parameters': parameters,
    #                           'records': collection.nitems,
    #                           'out_file': ''}
    #                 cur.execute(update_job, params)

    #                 cur.execute(get_last_jobid)
    #                 val = cur.fetchone()
    #                 last_job = 1 if val is None else val[0]

    #                 tables = {'antallaktikaonline': update_antallaktika,
    #                           'rellasamortiser': update_rellas}
    #                 query = tables[table]
    #                 cur.executemany(query, collection.get_data('tuple'))
    #                 con.commit()

    #                 tables = {'antallaktikaonline': update_jobid_antallaktika,
    #                           'rellasamortiser': update_jobid_rellas}
    #                 query = tables[table]
    #                 cur.execute(query, {'job_id': last_job})

    #                 con.commit()
    #     except Error as e:
    #         print(str(e) + " from " + self.db)


if __name__ == '__main__':
    # Popen(["C:/Program Files/DB Browser for SQLite/DB Browser for SQLite.exe", "C:/Users/aznavouridis.k/.atcrawl/atcrawl.db"])
    asql = AtcrawlSQL("C:/Users/aznavouridis.k/.atcrawl/atcrawl.db")

    print(asql.get_params_from_jobid(5))
