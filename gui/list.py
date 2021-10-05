# -*- coding: utf-8 -*-
import os

from helper import *
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget, QProgressBar,
                             QListWidget, QListWidgetItem, QAbstractItemView,
                             QGroupBox)

from at.gui.check import CheckInput


class ListWidget(QWidget):
    def __init__(self, label='', items=None, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.items = {}
        self.setupUi(label, items)
        self.checkBox.subscribe(self.selectAll)

    def setupUi(self, label, items):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 4, 0, 4)

        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label150")

        self.setObjectName("ListWidget")
        self.listWidget = QListWidget(self)
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSpacing(1)
        self.listWidget.setSelectionMode(QAbstractItemView.NoSelection)
        for item in items:
            qlistwidgetitem = QListWidgetItem(self.listWidget)
            qlistwidgetitem.setCheckState(Qt.Unchecked)
            qlistwidgetitem.setText(item)
            self.items[item] = {'widget': qlistwidgetitem,
                                'checked': qlistwidgetitem.checkState()}

        self.checkBox = CheckInput('Select All', checked=False, parent=self)

        self.layout.addWidget(self.label,)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.checkBox, 0, Qt.AlignHCenter)

    def getCheckState(self):
        return {name: bool(self.items[name]['widget'].checkState()) for name in self.items}

    def selectAll(self):
        if self.checkBox.isChecked():
            for item in self.items:
                self.items[item]['widget'].setCheckState(Qt.Checked)
                self.items[item]['checked'] = self.items[item]['widget'].checkState()
        else:
            for item in self.items:
                self.items[item]['widget'].setCheckState(Qt.Unchecked)
                self.items[item]['checked'] = self.items[item]['widget'].checkState()
