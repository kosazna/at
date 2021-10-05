# -*- coding: utf-8 -*-
from at.gui.check import CheckInput
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QLabel, QListWidget,
                             QListWidgetItem, QVBoxLayout, QWidget, QHBoxLayout)

from helper import *


class ListWidget(QWidget):
    def __init__(self, label='', items=None, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.items = {}
        self.setupUi(label, items)
        self.checkBox.subscribe(self.selectAll)

    def setupUi(self, label, items):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 4, 0, 4)

        self.layoutTop = QHBoxLayout()
        self.layoutTop.setSpacing(1)

        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label150")

        self.setObjectName("ListWidget")
        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName("ListWidget")
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

        self.layoutTop.addWidget(self.label)
        self.layoutTop.addWidget(self.checkBox, 0, Qt.AlignRight)
        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout)

    def getCheckState(self, rtype='list'):
        if rtype == 'list':
            return [name for name in self.items if bool(self.items[name]['widget'].checkState())]
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

    def addItems(self, items):
        if isinstance(items, str):
            items2add = [items]
        else:
            items2add = items

        for item in items2add:
            qlistwidgetitem = QListWidgetItem(self.listWidget)
            qlistwidgetitem.setCheckState(Qt.Unchecked)
            qlistwidgetitem.setText(item)
            self.items[item] = {'widget': qlistwidgetitem,
                                'checked': qlistwidgetitem.checkState()}
