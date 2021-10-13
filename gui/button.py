# -*- coding: utf-8 -*-
from typing import Union

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QToolButton, QWidget, QPushButton


class Button(QPushButton):
    def __init__(self,
                 label: str = '',
                 color: Union[str, None] = None,
                 icon: Union[str, None] = None,
                 size: tuple = (70, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, color, icon, size)

    def setupUi(self, label, color, icon, size):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyle(color, size)
        if icon is not None:
            qicon = QIcon()
            qicon.addFile(f":/bootstrap/icons/{icon}.svg", QSize(16, 16),
                          QIcon.Normal, QIcon.Off)
            self.setIcon(qicon)
        self.setText(label)

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
