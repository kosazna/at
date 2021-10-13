# -*- coding: utf-8 -*-
from typing import Tuple, Union

from at.gui.button import Button
from at.gui.check import CheckInput
from at.gui.popup import Popup, pbutton
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractScrollArea,
                             QHBoxLayout, QLabel, QListView, QListWidget,
                             QListWidgetItem, QVBoxLayout, QWidget)


class ListWidget(QWidget):
    def __init__(self,
                 label: str = '',
                 items: Union[list, tuple, None] = None,
                 labelsize: tuple = (100, 22),
                 widgetsize: Tuple[Union[int, None]] = (None, 250),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.items = {}
        self.setupUi(label, items, labelsize, widgetsize)
        self.loadFunc = None
        self.checkBox.subscribe(self.selectAll)
        self.buttonLoad.subscribe(self.loadContent)
        self.buttonClear.subscribe(self.clearContent)

    def setupUi(self, label, items, labelsize, widgetsize):
        _width = widgetsize[0]
        _height = widgetsize[1]
        if _width is not None:
            self.setFixedWidth(_width)
        if _height is not None:
            self.setFixedHeight(_height)

        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedSize(*labelsize)
        self.label.setAlignment(Qt.AlignCenter)

        self.listWidget = QListWidget(self)
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
        self.buttonLoad = Button('Load', size=(60, 20), parent=self)
        self.buttonClear = Button('Clear', size=(60, 20), parent=self)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 4, 0, 4)
        self.layoutTop = QHBoxLayout()
        self.layoutTop.setSpacing(1)
        self.layoutBottom = QHBoxLayout()
        self.layoutTop.setSpacing(1)
        self.layoutTop.addWidget(self.label, alignment=Qt.AlignHCenter)
        self.layoutBottom.addWidget(self.checkBox)
        self.layoutBottom.addWidget(self.buttonLoad)
        self.layoutBottom.addWidget(self.buttonClear)
        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.listWidget)
        self.layout.addLayout(self.layoutBottom)
        self.setLayout(self.layout)

    def getCheckState(self, rtype='list'):
        if self.items:
            checked = [name for name in self.items if bool(
                self.items[name]['widget'].checkState())]
            if rtype == 'list':
                return checked
            elif rtype == 'string':
                return '-'.join(checked)
            else:
                return {name: bool(self.items[name]['widget'].checkState()) for name in self.items}
        else:
            if rtype == 'list':
                return list()
            elif rtype == 'string':
                return ''
            else:
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
        elif isinstance(items, (list, tuple)):
            items2add = items
        else:
            Popup().info("No items were added", buttons=[pbutton['ok']])
            return

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

    def hideButtons(self):
        self.buttonLoad.hide()
        self.buttonClear.hide()
