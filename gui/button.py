# -*- coding: utf-8 -*-
from helper import *

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget, QProgressBar)


class Button(QToolButton):
    def __init__(self, label='', parent:QWidget=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label)

    def setupUi(self, label):
        self.setText(label)
        self.setObjectName("BlueButton")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def disable(self):
        self.setEnabled(False)
        self.setStyle(f"GreyButton")
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self, color):
        self.setEnabled(True)
        self.setStyle(f"{color.name.capitalize()}Button")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def subscribe(self, func):
        self.clicked.connect(func)

    def setStyle(self, object_name):
        self.setObjectName(object_name)
        self.setStyleSheet(cssGuide)
