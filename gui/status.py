# -*- coding: utf-8 -*-
from typing import Callable, Optional, Tuple

from at.gui.utils import set_size
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap
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
        self.button = QPushButton(parent=self)
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

    def disable(self, text: str = ''):
        self.setText(text)
        self.button.setEnabled(False)
        self.setStyle("statusOff")
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, text: str):
        if text:
            self.setText(text)
        self.button.setEnabled(True)
        self.setStyle("statusOn")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def setText(self, text: str):
        self.button.setText(text)

    def getText(self):
        return self.button.text()

    def setStyle(self, object_name: str):
        self.button.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def subscribe(self, func: Callable):
        self.button.clicked.connect(func)


class StatusLabel(QWidget):
    def __init__(self,
                 label: str = '',
                 icon: str = '',
                 status: str = '',
                 labelsize: Tuple[int] = (70, 22),
                 statussize: Tuple[int] = (100, 22),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, icon, status, labelsize, statussize)

    def setupUi(self, label, icon, status, labelsize, statussize):

        self.status = QLabel(parent=self)
        self.status.setText(status)
        set_size(widget=self.status, size=statussize)
        self.status.setObjectName('statusNeutral')
        self.status.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        if label:
            self.label = QLabel(parent=self)
            self.label.setText(label)
            set_size(widget=self.label, size=labelsize)
            layout.addWidget(self.label)
        else:
            if icon:
                self.iconLabel = QLabel(parent=self)
                self.iconLabel.setFixedSize(24, 24)
                self.iconLabel.setPixmap(
                    QPixmap(f":/bootstrap/icons/{icon}.svg"))
                self.iconLabel.setAlignment(Qt.AlignCenter)
                layout.addWidget(self.iconLabel)
        layout.addWidget(self.status, 1, alignment=Qt.AlignLeft)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(4)

        self.setLayout(layout)

    def changeStatus(self, status: str, object_name: str):
        self.setText(status)
        self.setStyle(object_name)

    def setText(self, text: str):
        self.status.setText(text)

    def getText(self):
        return self.status.text()

    def setStyle(self, object_name: str):
        self.status.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def setOffset(self, offset: str):
        self.label.setFixedWidth(offset)
