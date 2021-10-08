# -*- coding: utf-8 -*-
from pathlib import Path


class PathEngine:
    def __init__(self, appname: str):
        self._home = Path.home()
        self._cwd = Path.cwd()
        self._app = self.home.joinpath(f".{appname}")
        self._static = self._app.joinpath("static")
        self._db = self._app.joinpath(f"{appname}.db")
        self._init_paths()

    def _init_paths(self):
        if not self._app.exists():
            self._app.mkdir(parents=True, exist_ok=True)
        if not self._static.exists():
            self._app.mkdir(parents=True, exist_ok=True)

    def get_home(self):
        return self._home.as_posix()

    def get_cwd(self):
        return self._cwd.as_posix()

    def get_app(self):
        return self._app.as_posix()

    def get_static(self):
        return self._static.as_posix()

    def get_db(self):
        return self._db.as_posix()
