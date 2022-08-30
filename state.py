# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from at.io.utils import load_json
from at.logger import log
from at.singleton import Singleton


class AppState(metaclass=Singleton):
    def __init__(self,
                 appname: Optional[str] = None,
                 version: Optional[str] = None,
                 debug: bool = False,
                 temp: Optional[Any] = None,
                 db: Optional[Any] = None,
                 json: Optional[str | Path] = None) -> None:
        self.appname = appname
        self.version = version
        self.debug = debug
        self.temp = temp
        self.db = DBState(db)
        self.json = JSONState(json)


class DBState(metaclass=Singleton):
    def __init__(self, db) -> None:
        self.db = db
        self.state, self.changes = self.load()

    def load(self):
        if self.db is not None:
            db_state = self.db.load_state() or dict()
            changes = {k: False for k in db_state}

            return db_state, changes
        return dict(), dict()

    def save(self):
        changes = self.changes.values()
        if any(changes) and self.db is not None:
            self.db.save_state(self)

    def __getitem__(self, key: str) -> Any:
        return self.state.get(key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        try:
            self.state[key] = value
            self.changes[key] = True
        except KeyError:
            log.warning(f"State <{key}> is not in app db state")


class JSONState(metaclass=Singleton):
    def __init__(self, jsonfile: str | Path) -> None:
        self.jsonfile = jsonfile
        self.state, self.changes = self.load()

    def load(self):
        if self.jsonfile is not None:
            json_data = load_json(self.jsonfile)
            config = json_data.get('config')
            json_state = config or dict()
            changes = {k: False for k in json_state}
            return json_state, changes
        return dict(), dict()

    def save(self):
        pass

    def __getitem__(self, key: str) -> Any:
        return self.state.get(key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        try:
            self.state[key] = value
            self.changes[key] = True
        except KeyError:
            log.warning(f"State <{key}> is not in app json state")


class State(metaclass=Singleton):
    def __init__(self,
                 initial_state: Optional[dict] = None,
                 db: Optional[Any] = None) -> None:
        self.state = dict() if initial_state is None else initial_state
        self.db = db

    @classmethod
    def from_db(cls, db) -> State:
        db_state = db.load_state()
        initial_state = {}
        for k, v in db_state.items():
            initial_state[k] = {'value': v,
                                'origin': 'db',
                                'altered': False}
        return cls(initial_state, db)

    def __len__(self):
        return len(self.state)

    def __iter__(self):
        return iter(self.state)

    def __contains__(self, item: str) -> bool:
        return item in self.state

    def __getitem__(self, key: str) -> Any:
        state_key = self.state.get(key, None)
        if state_key is not None:
            state_value = state_key.get('value')
            if state_value is not None:
                return state_value
            else:
                log.warning(f"State <{key}> does not have a value")
                return '<null>'
        else:
            log.warning(f"State <{key}> is not in app state")
            return '<null>'

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def update_db(self) -> None:
        if self.db is not None:
            db_changes = False
            for s in self.state:
                if self.state[s]['origin'] == 'db':
                    if self.state[s]['altered']:
                        db_changes = True
                        break

            if db_changes:
                self.db.save_state(self)

    def get(self,
            key: Optional[str] = None,
            values_only: bool = False) -> Any:
        if key is None:
            if values_only:
                return {k: self.state[k]['value'] for k in self.state}
            return self.state
        else:
            return self.state[key]

    def set(self,
            key: Union[str, dict],
            value: Optional[Any] = None,
            origin: str = 'app') -> None:
        if isinstance(key, dict):
            for k, v in key.items():
                if k in self.state:
                    self.state[k]['value'] = v
                    self.state[k]['altered'] = True
                else:
                    self.state[k] = {'value': v,
                                     'origin': origin,
                                     'altered': False}
        else:
            if value is not None:
                if key in self.state:
                    self.state[key]['value'] = value
                    self.state[key]['altered'] = True
                else:
                    self.state[key] = {'value': value,
                                       'origin': origin,
                                       'altered': False}
            else:
                raise ValueError("Value parameter must be provided")
