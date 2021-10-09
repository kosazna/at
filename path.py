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
        self._db = self._app.joinpath(f"{appname}.db")
        self._settings = self._app.joinpath("settings.json")
        self._init_paths()

    def _init_paths(self):
        if not self._app.exists():
            self._app.mkdir(parents=True, exist_ok=True)
        if not self._static.exists():
            self._static.mkdir(parents=True, exist_ok=True)
        if not self._auth.exists():
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

    def get_db(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._db
        return self._db.as_posix()

    def get_settings(self, obj: bool = False) -> Union[str, Path]:
        if obj:
            return self._settings
        return self._settings.as_posix()
