# -*- coding: utf-8 -*-

import os
from pathlib import Path
from sqlite3 import Connection, Row
from sqlite3 import connect as sqlite_connect
from subprocess import Popen
from typing import Optional, Union

from dotenv import load_dotenv

from at.database.action import db_insert, db_script, db_select, db_update
from at.database.utils import Query, load_app_queries
from at.logger import log
from at.path import PathEngine
from at.state import State

load_dotenv()


class SQLiteEngine:
    def __init__(self,
                 db: Union[str, Path],
                 app_paths: Optional[PathEngine] = None) -> None:
        self.db = str(db)
        self.db_exists = Path(db).exists()
        self.connection: Optional[Connection] = None
        self.open_connection()

        if app_paths is not None:
            self.paths = app_paths
            self.init_queries = load_app_queries(self.paths.get_init_sql())
            self._db_init()

    def _db_init(self):
        if self.init_queries is not None:
            for query_name, query in self.init_queries.items():
                if query_name.startswith('init'):
                    if not self.db_exists:
                        self.script(query)
                elif query_name.startswith('table'):
                    self.script(query)
                else:
                    self.script(query)
                    sql_name = f"{query_name}.sql"
                    sql_folder = self.paths.get_init_sql(True)
                    sql_file = sql_folder.joinpath(sql_name)
                    sql_file.unlink(missing_ok=True)

    def open_db(self, executable: Union[str, Path]):
        if Path(executable).exists():
            Popen([str(executable), self.db])
        else:
            log.warning('To view database install DB Browser (SQLite) (64-bit)')

    def open_connection(self):
        self.connection: Connection = sqlite_connect(
            self.db, check_same_thread=False)
        self.connection.row_factory = Row

        log.success("Connected to SQLite database.")

    def close_connection(self):
        self.connection.close()
        log.highlight("Connection to SQLite database closed.")

    def get_connection(self):
        return self.connection

    def update(self, query: Query):
        db_update(connection=self.connection, query=query)

    def insert(self, query: Query):
        db_insert(connection=self.connection, query=query)

    def select(self, query: Query, dictionary: bool = True):
        if query.fetch in ('row', 'rows'):
            result = db_select(connection=self.connection, query=query)

            if result is None:
                return dict() if dictionary else tuple()

            if isinstance(result, (list, tuple)):
                if dictionary:
                    return [dict(r) for r in result]
                return [tuple(r) for r in result]
            else:
                if dictionary:
                    return dict(result)
                return tuple(result)
        else:
            return db_select(connection=self.connection, query=query)

    def script(self, query: Query):
        db_script(connection=self.connection, script=query)

    def load_state(self) -> dict:
        pass

    def save_state(self, state: State):
        pass


class MySQLEngine:
    CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': os.getenv("MYSQL_PASSWORD")}

    def __init__(self,
                 database: str,
                 app_paths: Optional[PathEngine] = None,
                 config: Optional[dict] = None) -> None:
        self.open_connection(database=database, config=config)

        if app_paths is not None:
            self.paths = app_paths
            self.init_queries = load_app_queries(self.paths.get_init_sql())
            self._db_init()

    def _db_init(self):
        if self.init_queries is not None:
            for query_name, query in self.init_queries.items():
                if query_name.startswith('new'):
                    self.db_script(query)
                    sql_name = f"{query_name}.sql"
                    sql_folder = self.paths.get_init_sql(True)
                    sql_file = sql_folder.joinpath(sql_name)
                    sql_file.unlink(missing_ok=True)

    def open_db(self, executable: Union[str, Path]):
        if Path(executable).exists():
            Popen([str(executable), self.db])
        else:
            log.warning('To view database install DB Browser (SQLite) (64-bit)')

    def open_connection(self, database: str, config: Optional[dict]):
        try:
            from mysql.connector import MySQLConnection
            from mysql.connector import connect as mysql_connect

            if config is not None:
                self.connection: MySQLConnection = mysql_connect(**config,
                                                                 database=database)
            else:
                self.connection: MySQLConnection = mysql_connect(**self.CONFIG,
                                                                 database=database)
            log.success("Connected to MySQL database.")
        except ModuleNotFoundError:
            log.error("MySQL connector not installed.")

    def close_connection(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            log.highlight("Connection to database closed.")

    def update(self, query: Query):
        db_update(connection=self.connection, query=query)

    def insert(self, query: Query):
        db_insert(connection=self.connection, query=query)

    def select(self, query: Query, dictionary: bool = True):
        if query.fetch in ('row', 'rows'):
            return db_select(connection=self.connection,
                             query=query,
                             dictionary=dictionary)
        else:
            return db_select(connection=self.connection, query=query)

    def script(self, query: Query):
        db_script(connection=self.connection, script=query)

    def load_state(self) -> dict:
        pass

    def save_state(self, state: State):
        pass
