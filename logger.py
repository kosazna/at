# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
import sys
from typing import Optional, Tuple

from colorama import Fore, init

from at.singleton import Singleton

init(autoreset=True)

NORMAL = 'NORMAL'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
SUCCESS = 'SUCCESS'

color = {NORMAL: '#f8f8f8',
         INFO: '#258DEE',
         WARNING: '#E7AF06',
         ERROR: '#EF3E4F',
         SUCCESS: '#19CB5C'}

GUI_EMPTY = '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#e7af06;"><br /></p>'


def parse_newlines(string: str) -> Tuple[str]:
    if string.startswith('\n'):
        prefix = GUI_EMPTY
    else:
        prefix = ''
    if string.endswith('\n'):
        suffix = GUI_EMPTY
    else:
        suffix = ''

    return prefix, suffix


def strfwarning(string: str) -> str: return f"{Fore.LIGHTYELLOW_EX}{string}"
def strferror(string: str) -> str: return f"{Fore.LIGHTRED_EX}{string}"
def strfsuccess(string: str) -> str: return f"{Fore.LIGHTGREEN_EX}{string}"
def strfhighlight(string: str) -> str: return f"{Fore.LIGHTCYAN_EX}{string}"


def guinormal(string: str) -> str:
    if isinstance(string, str):
        prefix, suffix = parse_newlines(string)
        return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[NORMAL]};">{string.strip()}</span></p>{suffix}'
    else:
        return f'{GUI_EMPTY}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[NORMAL]};">{repr(string)}</span></p>{GUI_EMPTY}'


def guihighlight(string: str) -> str:
    if isinstance(string, str):
        prefix, suffix = parse_newlines(string)
        return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[INFO]};font-weight:bold;">{string.strip()}</span></p>{suffix}'
    else:
        return f'{GUI_EMPTY}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[INFO]};">{repr(string)}</span></p>{GUI_EMPTY}'


def guiwarning(string: str) -> str:
    if isinstance(string, str):
        prefix, suffix = parse_newlines(string)
        return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[WARNING]};font-weight:bold;">{string.strip()}</span></p>{suffix}'
    else:
        return f'{GUI_EMPTY}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[WARNING]};">{repr(string)}</span></p>{GUI_EMPTY}'


def guierror(string: str) -> str:
    if isinstance(string, str):
        prefix, suffix = parse_newlines(string)
        return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[ERROR]};font-weight:bold;">{string.strip()}</span></p>{suffix}'
    else:
        return f'{GUI_EMPTY}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[ERROR]};">{repr(string)}</span></p>{GUI_EMPTY}'


def guisuccess(string: str) -> str:
    if isinstance(string, str):
        prefix, suffix = parse_newlines(string)
        return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[SUCCESS]};font-weight:bold;">{string.strip()}</span></p>{suffix}'
    else:
        return f'{GUI_EMPTY}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[SUCCESS]};">{repr(string)}</span></p>{GUI_EMPTY}'


class Logger(metaclass=Singleton):
    def __init__(self, mode='CLI'):
        self.mode = mode
        self.content = []
        self.flushed = True
        self.logger: Optional[logging.Logger] = None

    def set_mode(self, mode: str):
        self.mode = mode
        if self.mode == "GUI":
            self.flushed = False

    def get_mode(self) -> str:
        return self.mode

    def flush(self):
        self.flushed = True
        for con in self.content:
            eval(con)

    def info(self, content: str):
        if self.mode == 'GUI':
            print(guinormal(content))
        else:
            print(content)

        if not self.flushed:
            self.content.append(f"self.info('{content}')")

    def highlight(self, content: str):
        if self.mode == 'GUI':
            print(guihighlight(content))
        else:
            print(strfhighlight(content))

        if not self.flushed:
            self.content.append(f"self.highlight('{content}')")

    def warning(self, content: str):
        if self.mode == 'GUI':
            print(guiwarning(content))
        else:
            print(strfwarning(content))

        if not self.flushed:
            self.content.append(f"self.warning('{content}')")

    def error(self, content: str):
        if self.mode == 'GUI':
            print(guierror(content))
        else:
            print(strferror(content))

        if not self.flushed:
            self.content.append(f"self.error('{content}')")

    def success(self, content: str):
        if self.mode == 'GUI':
            print(guisuccess(content))
        else:
            print(strfsuccess(content))

        if not self.flushed:
            self.content.append(f"self.success('{content}')")

    def set_exception_handling(self, logger_filepath: str, logger_name: str):
        logging.basicConfig(filename=logger_filepath,
                            filemode='a',
                            format='\n%(asctime)s %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)

        logger = logging.getLogger(logger_name)
        self.logger = logger

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            logger.error("--> Uncaught exception <--",
                        exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception


log = Logger(mode='CLI')
