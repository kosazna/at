# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import Union


class PathEngine:
    def __init__(self, appname: str):
        self._home = Path.home()
        self._cwd = Path.cwd()
        self._app = self._home.joinpath(f".{appname}")
        self._auth = Path(os.environ.get('APPDATA')).joinpath(f".{appname}")
        self._static = self._app.joinpath("static")
        self._source = self._app.joinpath("source")
        self._logger = self._app.joinpath(f"{appname}.log")
        self._env = self._source.joinpath(f"{appname}/.env")
        self._sql = self._static.joinpath("sql")
        self._css = self._static.joinpath("css")
        self._db = self._app.joinpath(f"{appname}.db")
        self._settings = self._app.joinpath("settings.json")
        self._init_paths()

    def _init_paths(self):
        self._app.mkdir(parents=True, exist_ok=True)
        self._static.mkdir(parents=True, exist_ok=True)
        self._sql.mkdir(parents=True, exist_ok=True)
        self._sql.joinpath("init").mkdir(parents=True, exist_ok=True)
        self._css.mkdir(parents=True, exist_ok=True)
        self._auth.mkdir(parents=True, exist_ok=True)

    def get_home(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._home
        return self._home.as_posix()

    def get_cwd(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._cwd
        return self._cwd.as_posix()

    def get_app(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._app
        return self._app.as_posix()

    def get_authfolder(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._auth
        return self._auth.as_posix()

    def get_static(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._static
        return self._static.as_posix()

    def get_source(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._source
        return self._source.as_posix()

    def get_logger(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._logger
        return self._logger.as_posix()

    def get_env(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._env
        return self._env.as_posix()

    def get_css(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._css
        return self._css.as_posix()

    def get_sql(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._sql
        return self._sql.as_posix()

    def get_init_sql(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._sql.joinpath("init")
        return self._sql.joinpath("init").as_posix()

    def get_db(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._db
        return self._db.as_posix()

    def get_settings(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._settings
        return self._settings.as_posix()

    def get_db_exe(self) -> str:
        return "C:/Program Files/DB Browser for SQLite/DB Browser for SQLite.exe"
