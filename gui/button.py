# -*- coding: utf-8 -*-
from typing import Optional

from at.gui.utils import set_size
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton, QWidget


class Button(QPushButton):
    def __init__(self,
                 label: str = '',
                 color: Optional[str] = None,
                 icon: Optional[str] = None,
                 size: tuple = (70, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, color, icon, size)

    def setupUi(self, label, color, icon, size):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if icon is not None:
            qicon = QIcon()
            qicon.addFile(f":/bootstrap/icons/{icon}.svg", QSize(12, 12),
                          QIcon.Normal, QIcon.Off)
            self.setIcon(qicon)
        self.setText(label)
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
            set_size(widget=self, size=size)

    def subscribe(self, func):
        self.clicked.connect(func)
