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
                 info: Optional[str] = '',
                 details: Optional[dict] = None) -> None:
        self.result = result
        self.info = info
        self.details = dict() if details is None else details

    @classmethod
    def info(cls, info: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.info(info)
        return cls(INFO, info, details)

    @classmethod
    def warning(cls, info: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.warning(info)
        return cls(WARNING, info, details)

    @classmethod
    def error(cls, info: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.error(info)
        return cls(ERROR, info, details)

    @classmethod
    def success(cls, info: Optional[str] = '', details: Optional[dict] = None) -> Result:
        log.success(info)
        return cls(SUCCESS, info, details)
