# -*- coding: utf-8 -*-
from typing import Union
from helper import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QToolButton, QWidget


class Button(QToolButton):
    def __init__(self,
                 label: str = '',
                 color: Union[str, None] = None,
                 size: tuple = (70, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, color, size)

    def setupUi(self, label, color, size):
        self.setText(label)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyle(color, size)

    def disable(self, color='grey', size=None):
        self.setEnabled(False)
        self.setStyle(color, size)
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, color=None, size=None):
        self.setEnabled(True)
        self.setStyle(color, size)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def setStyle(self, color=None, size=None):
        if color is None:
            self.setObjectName("")
        else:
            self.setObjectName(f"{color}Button")

        self.setStyleSheet(self.styleSheet())

        if size is not None:
            self.setFixedSize(*size)

    def subscribe(self, func):
        self.clicked.connect(func)
