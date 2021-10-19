# -*- coding: utf-8 -*-
from typing import Optional, Tuple, Union

from at.gui.button import Button
from at.gui.check import CheckInput
from at.gui.popup import Popup, pbutton
from at.gui.utils import set_size
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractScrollArea,
                             QHBoxLayout, QLabel, QListView, QListWidget,
                             QListWidgetItem, QVBoxLayout, QWidget)


class ListWidget(QWidget):
    def __init__(self,
                 label: str = '',
                 items: Optional[Union[list, tuple]] = None,
                 labelsize: tuple = (100, 24),
                 widgetsize: Tuple[Optional[int]] = (None, 250),
                 parent: Optional[QWidget] = None,
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
        set_size(widget=self, size=widgetsize)

        self.label = QLabel()
        self.label.setText(label)
        set_size(widget=self.label, size=labelsize)
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

    def toggle(self):
        self.checkBox.toggle()

    def selectAll(self):
        if self.checkBox.isChecked():
            if self.items:
                for item in self.items:
                    self.items[item]['widget'].setCheckState(Qt.Checked)
                    self.items[item]['checked'] = self.items[item]['widget'].checkState()
            self.checkBox.setText('Unselect All')
        else:
            if self.items:
                for item in self.items:
                    self.items[item]['widget'].setCheckState(Qt.Unchecked)
                    self.items[item]['checked'] = self.items[item]['widget'].checkState()
            self.checkBox.setText('Select All')

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
        self.checkBox.setText('Select All')

    def hideButtons(self):
        self.buttonLoad.hide()
        self.buttonClear.hide()
