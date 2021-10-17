# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Optional, Union

from at.logger import log
from at.singleton import Singleton


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

    def update_db(self) -> None:
        if self.db is not None:
            self.db.save_state(self)

    def get_state(self,
                  key: Optional[str] = None,
                  values_only: bool = False) -> Any:
        if key is None:
            if values_only:
                return {k: self.state[k]['value'] for k in self.state}
            return self.state
        else:
            self.state[key]

    def set_state(self,
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
        self.set_state(key, value)
