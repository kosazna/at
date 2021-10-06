# -*- coding: utf-8 -*-
from typing import Union
from helper import *

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget, QProgressBar)


class ComboInput(QWidget):
    def __init__(self,
                 label: str = '',
                 items: Union[list, tuple, None] = None,
                 labelsize: tuple = (70, 22),
                 combosize: tuple = (150, 22),
                 parent: QWidget = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, items, labelsize, combosize)

    def setupUi(self, label, items, labelsize, combosize):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedSize(*labelsize)
        self.comboEdit = QComboBox()
        self.comboEdit.setFixedSize(*combosize)
        self.comboEdit.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comboEdit, 1, alignment=Qt.AlignLeft)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)
        self.setLayout(layout)
        if items is not None:
            self.comboEdit.addItems(items)

    def getCurrentText(self):
        return self.comboEdit.currentText()

    def getCurrentIndex(self):
        return self.comboEdit.currentIndex()

    def addItems(self, items):
        self.comboEdit.addItems(items)

    def clearItems(self):
        self.comboEdit.clear()

    def setOffset(self, offset):
        self.label.setMinimumWidth(offset)

    def subscribe(self, func):
        self.comboEdit.currentIndexChanged.connect(func)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)
