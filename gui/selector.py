# -*- coding: utf-8 -*-
from typing import Optional, Tuple, Union

from at.gui.utils import HORIZONTAL, VERTICAL, set_size
from at.gui.combo import ComboInput
from at.gui.io import FolderInput, FileInput, FileOutput
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QCompleter, QHBoxLayout, QLabel, QLineEdit,
                             QVBoxLayout, QWidget)

from at.gui.input import StrInput


class PathSelector(QWidget):
    def __init__(self,
                 label: str = '',
                 selectortype='folder_in',
                 mapping: Optional[dict] = None,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 24),
                 combosize: tuple = (150, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.mapping = {} if mapping is None else mapping
        self.mapping.update({"Other...": ''})
        self.setupUi(label, selectortype, orientation,
                     labelsize, combosize, editsize)
        self.combo.subscribe(self.onComboChange)

    def setupUi(self, label, selectortype, orientation, labelsize, combosize, editsize):
        self.combo = ComboInput(items=self.mapping.keys(),
                                combosize=combosize,
                                parent=self)

        if selectortype == 'folder_in':
            self.path = FolderInput(editsize=editsize, parent=self)
        elif selectortype == 'file_in':
            self.path = FileInput(editsize=editsize, parent=self)
        elif selectortype == 'file_out':
            self.path = FileOutput(editsize=editsize, parent=self)

        if orientation == HORIZONTAL:
            layout = QHBoxLayout()
            layout.setSpacing(4)
            if label:
                self.label = QLabel(parent=self)
                self.label.setText(label)
                set_size(widget=self.label, size=labelsize)
                layout.addWidget(self.label)
            layout.addWidget(self.combo)
            layout.addWidget(self.path, stretch=2)
        else:
            layout = QVBoxLayout()
            layout.setSpacing(0)
            inner = QHBoxLayout()
            inner.setContentsMargins(0, 0, 0, 0)
            inner.setSpacing(4)
            if label:
                self.label = QLabel(parent=self)
                self.label.setText(label)
                set_size(widget=self.label, size=labelsize)
                layout.addWidget(self.label)
            inner.addWidget(self.combo)
            inner.addWidget(self.path, stretch=2)
            layout.addLayout(inner)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def onComboChange(self):
        current_text = self.combo.getCurrentText()

        if current_text == 'Other...':
            self.path.enable()
        else:
            self.path.disable()

        try:
            self.path.setText(self.mapping[current_text])
        except KeyError:
            self.path.setText('')

    def getCurrentText(self):
        return self.combo.currentText()

    def setCurrentText(self, text: str):
        self.combo.setCurrentText(text)
        self.onComboChange()

    def getCurrentIndex(self):
        return self.combo.currentIndex()

    def addItems(self, items: dict):
        self.combo.addItems(items.keys())
        self.mapping.update(items)

    def clearItems(self):
        self.combo.clearItems()
        self.mapping = {}

    def getText(self):
        return self.path.getText()

    def setText(self, text: str):
        self.path.setText(text)

    def setPlaceholder(self, text: str):
        self.path.setPlaceholder(text)


class StrSelector(QWidget):
    def __init__(self,
                 label: str = '',
                 mapping: Optional[dict] = None,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 24),
                 combosize: tuple = (150, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.mapping = {} if mapping is None else mapping
        self.mapping.update({"Other...": ''})
        self.setupUi(label, orientation, labelsize, combosize, editsize)
        self.combo.subscribe(self.onComboChange)

    def setupUi(self, label, orientation, labelsize, combosize, editsize):
        self.combo = ComboInput(items=self.mapping.keys(),
                                combosize=combosize,
                                parent=self)
        self.input = StrInput(completer=list(self.mapping.values()),
                              editsize=editsize,
                              parent=self)
        if self.mapping:
            first_mapping_item = list(self.mapping)[0]
            self.combo.setCurrentText(first_mapping_item)
            self.input.setText(self.mapping[first_mapping_item])

        if orientation == HORIZONTAL:
            layout = QHBoxLayout()
            layout.setSpacing(4)
            if label:
                self.label = QLabel(parent=self)
                self.label.setText(label)
                set_size(widget=self.label, size=labelsize)
                layout.addWidget(self.label)
            layout.addWidget(self.combo)
            layout.addWidget(self.input, stretch=2)
        else:
            layout = QVBoxLayout()
            layout.setSpacing(0)
            inner = QHBoxLayout()
            inner.setContentsMargins(0, 0, 0, 0)
            inner.setSpacing(4)
            if label:
                self.label = QLabel(parent=self)
                self.label.setText(label)
                set_size(widget=self.label, size=labelsize)
                layout.addWidget(self.label)
            inner.addWidget(self.combo)
            inner.addWidget(self.input, stretch=2)
            layout.addLayout(inner)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def onComboChange(self):
        current_text = self.combo.getCurrentText()

        if current_text == 'Other...':
            self.input.enable()
        else:
            self.input.disable()

        try:
            self.input.setText(self.mapping[current_text])
        except KeyError:
            self.input.setText('')

    def getCurrentText(self):
        return self.combo.currentText()

    def setCurrentText(self, text: str):
        self.combo.setCurrentText(text)
        self.onComboChange()

    def getCurrentIndex(self):
        return self.combo.currentIndex()

    def addItems(self, items: dict):
        self.combo.addItems(items.keys())
        self.mapping.update(items)

    def clearItems(self):
        self.combo.clearItems()
        self.mapping = {}

    def getText(self):
        return self.input.getText()

    def setText(self, text: str):
        self.input.setText(text)
