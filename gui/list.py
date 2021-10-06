# -*- coding: utf-8 -*-
from at.gui.check import CheckInput
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QLabel, QListWidget,
                             QListWidgetItem, QVBoxLayout, QWidget, QHBoxLayout,
                             QAbstractScrollArea, QListView)
from at.gui.button import Button

from helper import *
from pathlib import Path


class ListWidget(QWidget):
    def __init__(self, label='', items=None, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.items = {}
        self.setupUi(label, items)
        self.loadFunc = None
        self.checkBox.subscribe(self.selectAll)
        self.buttonLoad.subscribe(self.loadContent)
        self.buttonClear.subscribe(self.clearContent)

    def setupUi(self, label, items):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 4, 0, 4)

        self.layoutTop = QHBoxLayout()
        self.layoutTop.setSpacing(1)

        self.layoutBottom = QHBoxLayout()
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
        self.listWidget.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.listWidget.setResizeMode(QListView.Adjust)

        if items is not None:
            for item in items:
                qlistwidgetitem = QListWidgetItem(self.listWidget)
                qlistwidgetitem.setCheckState(Qt.Unchecked)
                qlistwidgetitem.setText(item)
                self.items[item] = {'widget': qlistwidgetitem,
                                    'checked': qlistwidgetitem.checkState()}

        self.checkBox = CheckInput('Select All', checked=False, parent=self)
        self.buttonLoad = Button('Load')
        self.buttonClear = Button('Clear')

        self.layoutTop.addWidget(self.label)
        self.layoutTop.addWidget(self.checkBox, 0, Qt.AlignRight)

        self.layoutBottom.addWidget(self.buttonLoad)
        self.layoutBottom.addWidget(self.buttonClear)

        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.listWidget)
        self.layout.addLayout(self.layoutBottom)
        self.setLayout(self.layout)

    def getCheckState(self, rtype='list'):
        if self.items:
            if rtype == 'list':
                return [name for name in self.items if bool(self.items[name]['widget'].checkState())]
            return {name: bool(self.items[name]['widget'].checkState()) for name in self.items}
        else:
            if rtype == 'list':
                return list()
            return dict()

    def selectAll(self):
        if self.items:
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

    def assignLoadFunc(self, func):
        self.loadFunc = func

    def loadContent(self):
        if self.loadFunc is not None:
            result = self.loadFunc()
            self.addItems(result)

    def clearContent(self):
        self.listWidget.clear()
        self.items = {}
        self.checkBox.setCheckState(Qt.Unchecked)
