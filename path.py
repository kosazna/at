# -*- coding: utf-8 -*-
from pathlib import Path
import os


class PathEngine:
    def __init__(self, appname: str):
        self._home = Path.home()
        self._cwd = Path.cwd()
        self._app = self._home.joinpath(f".{appname}")
        self._appdata = Path(os.environ.get('APPDATA')).joinpath(f".{appname}")
        self._static = self._app.joinpath("static")
        self._db = self._app.joinpath(f"{appname}.db")
        self._settings = self._app.joinpath("settings.json")
        self._authfile = self._appdata.joinpath("auth.json")
        self._init_paths()

    def _init_paths(self):
        if not self._app.exists():
            self._app.mkdir(parents=True, exist_ok=True)
        if not self._static.exists():
            self._static.mkdir(parents=True, exist_ok=True)
        if not self._appdata.exists():
            self._appdata.mkdir(parents=True, exist_ok=True)

    def get_home(self) -> str:
        return self._home.as_posix()

    def get_cwd(self) -> str:
        return self._cwd.as_posix()

    def get_app(self) -> str:
        return self._app.as_posix()

    def get_appdata(self) -> str:
        return self._appdata.as_posix()

    def get_static(self) -> str:
        return self._static.as_posix()

    def get_db(self) -> str:
        return self._db.as_posix()

    def get_settings(self) -> str:
        return self._settings.as_posix()

    def get_authfile(self) -> str:
        return self._authfile.as_posix()


p = PathEngine('atcrawl')
