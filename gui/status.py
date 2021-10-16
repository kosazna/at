# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from at.gui.utils import set_size
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QWidget)


class StatusButton(QWidget):
    def __init__(self,
                 status: str = '',
                 size: Tuple[Optional[int]] = (None, 22),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(status, size)

    def setupUi(self, status, size):
        layout = QHBoxLayout()
        self.button = QPushButton()
        self.button.setText(status)
        self.button.setEnabled(False)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if status:
            self.enable()
        else:
            self.disable()

        set_size(widget=self.button, size=size)

        layout.addWidget(self.button)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        self.setLayout(layout)

    def disable(self, text=''):
        self.setText(text)
        self.button.setEnabled(False)
        self.setStyle("statusOff")
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, text):
        if text:
            self.setText(text)
        self.button.setEnabled(True)
        self.setStyle("statusOn")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def setText(self, text):
        self.button.setText(text)

    def getText(self):
        return self.button.text()

    def setStyle(self, object_name):
        self.button.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def subscribe(self, func):
        self.button.clicked.connect(func)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)


class StatusLabel(QWidget):
    def __init__(self,
                 label: str = '',
                 status: str = '',
                 labelsize: Tuple[int] = (70, 22),
                 statussize: Tuple[int] = (100, 22),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, status, labelsize, statussize)

    def setupUi(self, label, status, labelsize, statussize):
        self.label = QLabel()
        self.label.setText(label)
        set_size(widget=self.label, size=labelsize)

        self.status = QLabel()
        self.status.setText(status)
        set_size(widget=self.status, size=statussize)
        self.status.setObjectName('statusNeutral')
        self.status.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.status, 1, alignment=Qt.AlignLeft)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        self.setLayout(layout)

    def changeStatus(self, status, object_name):
        self.setText(status)
        self.setStyle(object_name)

    def setText(self, text):
        self.status.setText(text)

    def getText(self):
        return self.status.text()

    def setStyle(self, object_name):
        self.status.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)
