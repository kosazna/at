# -*- coding: utf-8 -*-
from helper import *

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget, QProgressBar)


class ProgressBar(QProgressBar):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setStyle("ProgressBar")

    def setStyle(self, object_name):
        self.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def setValueMaximum(self, current_value, maximum):
        self.setMaximum(maximum)
        self.setValue(current_value)

        # if current_value == maximum:
        #     self.setStyle("ProgressBarFinished")
