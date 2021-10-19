# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional
from at.logger import log, ERROR, WARNING, SUCCESS, INFO


class Result:
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR
    SUCCESS = SUCCESS

    def __init__(self,
                 result: Optional[str] = '',
                 msg: Optional[str] = '',
                 details: Optional[dict] = None) -> None:
        self.result = result
        self.msg = msg
        self.details = dict() if details is None else details

    @classmethod
    def msg(cls, msg: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.info(msg)
        return cls(INFO, msg, details)

    @classmethod
    def warning(cls, msg: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.warning(msg)
        return cls(WARNING, msg, details)

    @classmethod
    def error(cls, msg: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.error(msg)
        return cls(ERROR, msg, details)

    @classmethod
    def success(cls, msg: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.success(msg)
        return cls(SUCCESS, msg, details)
