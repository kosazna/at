# -*- coding: utf-8 -*-
import sys
from typing import Tuple, Union

from at.logger import GUI_EMPTY
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextBrowser, QWidget


class TextStream(QObject):
    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg: str):
        if not self.signalsBlocked():
            self.messageWritten.emit('%s%s' % (msg, GUI_EMPTY))

    @staticmethod
    def stdout():
        if not TextStream._stdout:
            TextStream._stdout = TextStream()
            sys.stdout = TextStream._stdout
        return TextStream._stdout

    @staticmethod
    def stderr():
        if not TextStream._stderr:
            TextStream._stderr = TextStream()
            sys.stderr = TextStream._stderr
        return TextStream._stderr


class TextBox(QTextBrowser):
    def __init__(self,
                 size: Tuple[Union[int, None]] = (None, None),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        TextStream.stdout().messageWritten.connect(lambda text: self.addText(text))
        TextStream.stderr().messageWritten.connect(lambda text: self.addText(text))
        self.setupUi(size)

    def setupUi(self, size):
        self.setReadOnly(True)
        lew = size[0]
        leh = size[1]
        if lew is not None:
            self.setFixedWidth(lew)
        if leh is not None:
            self.setFixedHeight(leh)

    def addText(self, text):
        self.insertHtml(text)
        self.moveCursor(QTextCursor.End)
