# -*- coding: utf-8 -*-
from at.singleton import Singleton

class Logger(metaclass=Singleton):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    color = {
        INFO: '#0D6EFD',
        WARNING: '#FD7E14',
        ERROR: '#EF3E4F'
    }

    def __init__(self, mode=None):
        self._mode = mode
        self._content = []

    @staticmethod
    def _display(content, kind=None):
        if kind is None:
            return content
        else:
            return f"[{kind}] - {content}"

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

    def get_content(self):
        to_show = '\n'.join(self._content)
        return to_show

    def erase(self):
        self._content = []

    def __call__(self, content=None, kind=None):
        if self._mode == 'CLI':
            if content is None:
                print('\n')
            else:
                print(self._display(content, kind))
        else:
            if content is None:
                _c = '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>'
            else:
                if kind is None:
                    _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{content}</p>'
                else:
                    _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">[<span style="color:{self.color[kind]};">{kind}</span>] - {content}</p>'

            self._content.append(_c)

    def info(self, content=None):
        if self.mode == 'CLI':
            if content is None:
                print('\n')
            else:
                print(Fore.WHITE + content)
        elif self.mode == 'GUI':
            _c = f'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">[<span style="color:{self.color[self.INFO]};">{self.INFO}</span>] - {content}</p>'


print(Style.BRIGHT + 'KOSTAS')
