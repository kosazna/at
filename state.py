# -*- coding: utf-8 -*-
from typing import Any, Optional, Union

from at.singleton import Singleton


class State(metaclass=Singleton):
    def __init__(self, state: Optional[dict] = None) -> None:
        self.state = state if state is not None else dict()

    def get_state(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self.state
        return self.state.get(key, None)

    def set_state(self, key: Union[str, dict], value: Optional[Any] = None):
        if isinstance(key, str):
            if value is not None:
                self.state[key] = value
            else:
                raise ValueError("Value parameter must be provided")
        elif isinstance(key, dict):
            self.state = {**self.state, **key}
        else:
            raise ValueError(f"Not accepted type for key: {type(key)}")
