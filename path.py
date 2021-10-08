# -*- coding: utf-8 -*-
from pathlib import Path
import os


class PathEngine:
    def __init__(self, appname: str):
        self._home = Path.home()
        self._cwd = Path.cwd()
        self._app = self.home.joinpath(f".{appname}")
        self._appdata = Path(os.environ.get('APPDATA'))
        self._static = self._app.joinpath("static")
        self._db = self._app.joinpath(f"{appname}.db")
        self._init_paths()

    def _init_paths(self):
        if not self._app.exists():
            self._app.mkdir(parents=True, exist_ok=True)
        if not self._static.exists():
            self._app.mkdir(parents=True, exist_ok=True)

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