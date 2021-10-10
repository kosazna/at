# -*- coding: utf-8 -*-
from at.singleton import Singleton
from colorama import init, Fore

init(autoreset=True)


class Logger(metaclass=Singleton):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    GUI_EMPTY = '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#e7af06;"><br /></p>'

    color = {
        INFO: '#0D6EFD',
        WARNING: '#E7AF06',
        ERROR: '#EF3E4F',
        SUCCESS: '#2AD66B'
    }

    def __init__(self, mode='CLI'):
        self.mode = mode
        self.content = []

    def _add(self, content: str, modified: str):
        if content.startswith('\n'):
            self.content.append(self.GUI_EMPTY)
        self.content.append(modified)
        if content.endswith('\n'):
            self.content.append(self.GUI_EMPTY)

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def get_content(self):
        to_show = ''.join(self.content)
        return to_show

    def clear(self):
        self.content = []

    def info(self, content: str):
        if self.mode == 'GUI':
            _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span">{content.strip()}</span></p>'
            self._add(content=content, modified=_c)
        else:
            print(content)

    def waring(self, content: str):
        if self.mode == 'GUI':
            _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{self.color[self.WARNING]};">{content.strip()}</span></p>'
            self._add(content=content, modified=_c)
        else:
            print(Fore.LIGHTYELLOW_EX + content)

    def error(self, content: str):
        if self.mode == 'GUI':
            _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{self.color[self.ERROR]};">{content.strip()}</span></p>'
            self._add(content=content, modified=_c)
        else:
            print(Fore.LIGHTRED_EX + content)

    def success(self, content: str):
        if self.mode == 'GUI':
            _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="color:{self.color[self.SUCCESS]};">{content.strip()}</span></p>'
            self._add(content=content, modified=_c)
        else:
            print(Fore.LIGHTGREEN_EX + content)

log = Logger(mode='GUI')
log.info('kostas')
log.waring('kostas')
log.error('kostas')
log.success('kostas')
print(log.get_content())
