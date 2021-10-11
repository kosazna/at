# -*- coding: utf-8 -*-
from typing import Tuple

from colorama import Fore, init

from at.singleton import Singleton

init(autoreset=True)

INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
SUCCESS = 'SUCCESS'

color = {INFO: '#0D6EFD',
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


def guinormal(string: str) -> str:
    prefix, suffix = parse_newlines(string)
    return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span">{string.strip()}</span></p>{suffix}'


def guiwarning(string: str) -> str:
    prefix, suffix = parse_newlines(string)
    return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[WARNING]};font-weight:bold;">{string.strip()}</span></p>{suffix}'


def guierror(string: str) -> str:
    prefix, suffix = parse_newlines(string)
    return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[ERROR]};font-weight:bold;">{string.strip()}</span></p>{suffix}'


def guisuccess(string: str) -> str:
    prefix, suffix = parse_newlines(string)
    return f'{prefix}<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{color[SUCCESS]};font-weight:bold;">{string.strip()}</span></p>{suffix}'


class Logger(metaclass=Singleton):
    def __init__(self, mode='CLI'):
        self.mode = mode
        self.content = []

    def set_mode(self, mode: str):
        self.mode = mode

    def get_mode(self) -> str:
        return self.mode

    def info(self, content: str):
        if self.mode == 'GUI':
            print(guinormal(content))
        else:
            print(content)

    def warning(self, content: str):
        if self.mode == 'GUI':
            print(guiwarning(content))
        else:
            print(strfwarning(content))

    def error(self, content: str):
        if self.mode == 'GUI':
            print(guierror(content))
        else:
            print(strferror(content))

    def success(self, content: str):
        if self.mode == 'GUI':
            print(guisuccess(content))
        else:
            print(strfsuccess(content))


log = Logger(mode='CLI')
