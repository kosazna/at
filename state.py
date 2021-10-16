# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Union

from at.singleton import Singleton
from at.sql.object import QueryObject
from at.sql.sqlite import SQLiteEngine


class StateObject:

    def __init__(self,
                 state_name: Any,
                 state_value: Optional[Any] = None,
                 sql_get: Optional[QueryObject] = None,
                 sql_set: Optional[QueryObject] = None) -> None:
        if isinstance(state_name, dict):
            (self.state_name, self.state_value),  = state_name.items()
        else:
            self.state_name = state_name
            self.state_value = state_value
        self.sql_get = sql_get
        self.sql_set = sql_set
        self.altered = False

    def __str__(self):
        return f"State({self.state_name}={self.state_value}, sql={bool(self.sql_get)}|{bool(self.sql_set)})"

    def __repr__(self):
        return f"State({self.state_name}={self.state_value}, sql={bool(self.sql_get)}|{bool(self.sql_set)})"

    def __hash__(self) -> int:
        return hash((self.state_name))

    def as_dict(self):
        return {self.state_name: self.state_value}

    def update(self, value):
        if isinstance(value, StateObject):
            self.state_value = value.state_value
            self.altered = True
        elif isinstance(value, dict):
            (state_name, state_value),  = value.items()
            if state_name == self.state_name:
                self.state_value = state_value
                self.altered = True
            else:
                raise ValueError(
                    f"Can't update {self.state_name} with {state_name}")
        else:
            self.state_value = value
            self.altered = True


class State(metaclass=Singleton):
    def __init__(self,
                 states: Optional[Iterable[StateObject]],
                 db: Optional[SQLiteEngine] = None) -> None:
        self.state: Dict[str, StateObject] = {}
        self.db = db
        if states is not None:
            for so in states:
                self.state[so.state_name] = so

    def update_db(self):
        if self.db is not None:
            for stateobj in self.state.values():
                query = stateobj.sql_set
                if query is not None and stateobj.altered:
                    self.db.update(query.set(**stateobj.as_dict()))
                    stateobj.altered = False

    def get_state(self,
                  key: Optional[str] = None,
                  obj=False) -> Union[Any, StateObject]:
        if key is None:
            return self.state
        else:
            stateobj = self.state.get(key, None)
            if stateobj is not None:
                return stateobj.state_value if not obj else stateobj
            return stateobj

    def set_state(self,
                  key: Union[str, dict, list, tuple, StateObject],
                  value: Optional[Any] = None):
        if isinstance(key, StateObject):
            if key in self.state:
                self.state[key.state_name].update(key)
            else:
                self.state[key.state_name] = key
        elif isinstance(key, dict):
            for k, v in key.items():
                if isinstance(v, StateObject):
                    if k in self.state:
                        self.state[k].update(v)
                    else:
                        self.state[k] = v
                else:
                    if k in self.state:
                        self.state[k].update(v)
                    else:
                        self.state[k] = StateObject(state_name=k, state_value=v)
        elif isinstance(key, (list, tuple)):
            for s in key:
                if isinstance(s, StateObject):
                    if s.state_name in self.state:
                        self.state[s.state_name].update(s)
                    else:
                        self.state[s.state_name] = s
                else:
                    raise ValueError(
                        "When setting state from iterable all items must be 'StateObject' items")
        else:
            if value is not None:
                if key in self.state:
                    self.state[key].update(value)
                else:
                    self.state[key] = StateObject(
                        state_name=key, state_value=value)
            else:
                raise ValueError("Value parameter must be provided")

        self.update_db()


s = State([StateObject('status', 'offline', 'dfdf'), (StateObject('web', 'on'))])

s.set_state({'status': 'online', 'kostas': True})
print(s.get_state())
