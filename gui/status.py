# -*- coding: utf-8 -*-
from helper import *

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget, QProgressBar)


class StatusIndicator(QWidget):
    def __init__(self,
                 label='',
                 status='',
                 parent=None,
                 size=70,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, status, size)

    def setupUi(self, label, status, size):
        layout = QHBoxLayout()
        self.button = QToolButton()
        self.button.setText(status)
        self.button.setEnabled(False)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if label:
            self.label = QLabel()
            self.label.setText(label)
            self.label.setObjectName(f"Label{size}")
            layout.addWidget(self.label)
            self.button.setObjectName("StatusSmallOffline")
            layout.addWidget(self.button, 1, alignment=Qt.AlignLeft)
            self.has_label = True
        else:
            self.button.setObjectName("StatusBigDisabled")
            layout.addWidget(self.button)
            self.has_label = False

        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        self.setLayout(layout)

    def disable(self, text=''):
        self.button.setEnabled(False)
        self.setText(text)
        if self.has_label:
            self.setStyle(f"StatusSmall{text.capitalize()}")
        else:
            self.setStyle("StatusBigDisabled")

    def enable(self, text=''):
        self.button.setEnabled(True)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.setText(text)
        if self.has_label:
            self.setStyle(f"StatusSmall{text.capitalize()}")
        else:
            self.setStyle("StatusBigEnabled")

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
