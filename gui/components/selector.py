# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from at.gui.components.combo import ComboInput
from at.gui.components.input import StrInput
from at.gui.components.io import FileInput, FileOutput, FolderInput
from at.gui.components.check import CheckInput
from at.gui.utils import HORIZONTAL, VERTICAL, set_size
from at.io.object import FilterObject
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


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

        if self.mapping:
            first_mapping_item = list(self.mapping)[0]
            self.combo.setCurrentText(first_mapping_item)
        
        self.onComboChange()

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
        return self.combo.getCurrentText()

    def setCurrentText(self, text: str):
        self.combo.setCurrentText(text)
        self.onComboChange()

    def getCurrentIndex(self):
        return self.combo.getCurrentIndex()

    def addItems(self, items: dict):
        self.combo.addItems(items.keys())
        self.mapping.update(items)
        first_mapping_item = list(items)[0]
        self.setCurrentText(first_mapping_item)

    def clearItems(self):
        self.combo.clearItems()
        self.mapping = {}

    def getText(self):
        return self.path.getText()

    def setText(self, text: str):
        self.path.setText(text)

    def setPlaceholder(self, text: str):
        self.path.setPlaceholder(text)

    def subscribe(self, func):
        self.combo.subscribe(func)


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

        self.onComboChange()

        if orientation == HORIZONTAL:
            layout = QHBoxLayout()
            layout.setSpacing(4)
            if label:
                self.label = QLabel(parent=self)
                self.label.setText(label)
                set_size(widget=self.label, size=labelsize)
                layout.addWidget(self.label)
            layout.addWidget(self.combo)
            layout.addWidget(self.input, stretch=1, alignment=Qt.AlignLeft)
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
            inner.addWidget(self.input, stretch=1, alignment=Qt.AlignLeft)
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
        return self.combo.getCurrentText()

    def setCurrentText(self, text: str):
        self.combo.setCurrentText(text)
        self.onComboChange()

    def getCurrentIndex(self):
        return self.combo.getCurrentIndex()

    def addItems(self, items: dict):
        self.combo.addItems(items.keys())
        self.mapping.update(items)
        first_mapping_item = list(items)[0]
        self.setCurrentText(first_mapping_item)

    def clearItems(self):
        self.combo.clearItems()
        self.mapping = {}

    def getText(self):
        return self.input.getText()

    def setText(self, text: str):
        self.input.setText(text)

    def subscribe(self, func):
        self.combo.subscribe(func)


class FilterFileSelector(QWidget):
    def __init__(self,
                 label: str = '',
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 24),
                 combosize: tuple = (100, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.mapping = {'exact': FilterObject,
                        'startwith': FilterObject.startswith,
                        'endwith': FilterObject.endswith,
                        'contain': FilterObject.contains}
        self.keep = ('all', 'files', 'dirs')
        self.setupUi(label, orientation, labelsize, combosize, editsize)

    def setupUi(self, label, orientation, labelsize, combosize, editsize):
        self.combo = ComboInput(items=self.mapping.keys(),
                                combosize=combosize,
                                parent=self)
        self.keepCombo = ComboInput(items=self.keep,
                                    combosize=(60, 24),
                                    parent=self)
        self.input = StrInput(editsize=editsize,
                              parent=self)
        self.recursive = CheckInput("recursive")
        self.recursive.toggle()

        if self.mapping:
            first_mapping_item = list(self.mapping)[2]
            self.combo.setCurrentText(first_mapping_item)

        self.keepCombo.setCurrentText(self.keep[1])

        if orientation == HORIZONTAL:
            layout = QHBoxLayout()
            layout.setSpacing(4)
            if label:
                self.label = QLabel(parent=self)
                self.label.setText(label)
                set_size(widget=self.label, size=labelsize)
                layout.addWidget(self.label)
            layout.addWidget(self.keepCombo)
            layout.addWidget(self.combo)
            layout.addWidget(self.input, stretch=2)
            layout.addWidget(self.recursive)
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
            layout.addWidget(self.keepCombo)
            inner.addWidget(self.combo)
            inner.addWidget(self.input, stretch=2)
            inner.addWidget(self.recursive)
            layout.addLayout(inner)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def setText(self,
                combo1: Optional[str] = None,
                combo2: Optional[str] = None,
                text: Optional[str] = None):
        if combo1 is not None:
            self.combo.setCurrentText(combo1)
        if combo2 is not None:
            self.keepCombo.setCurrentText(combo2)
        if text is not None:
            self.input.setText(text)

    def getCurrentText(self):
        return self.combo.getCurrentText()

    def getCurrentIndex(self):
        return self.combo.getCurrentIndex()

    def getText(self):
        return self.input.getText()

    def getKeepValue(self):
        return self.keepCombo.getCurrentText()

    def getFilterObject(self) -> FilterObject:
        filter_type = self.getCurrentText()
        filters = self.getText()
        recursive = self.recursive.isChecked()

        return self.mapping[filter_type](filters, recursive)
