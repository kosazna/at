# -*- coding: utf-8 -*-
from typing import Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QCompleter, QHBoxLayout, QLabel, QLineEdit,
                             QVBoxLayout, QWidget)

from at.gui.utils import *


class StrInput(QWidget):
    def __init__(self,
                 label: str = '',
                 orientation: str = HORIZONTAL,
                 completer: Union[list, tuple, None] = None,
                 hidden: bool = False,
                 labelsize: Tuple[int] = (70, 22),
                 editsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, hidden, labelsize, editsize)
        self.setCompleter(completer)

    def setupUi(self, label, orientation, hidden, labelsize, editsize):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedSize(*labelsize)

        self.lineEdit = QLineEdit()
        _width = editsize[0]
        _height = editsize[1]
        if _width is not None:
            self.lineEdit.setFixedWidth(_width)
        if _height is not None:
            self.lineEdit.setFixedHeight(_height)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if hidden:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def disable(self):
        self.lineEdit.setEnabled(False)
        self.setStyle('off')

    def enable(self):
        self.lineEdit.setEnabled(True)
        self.setStyle("")

    def setStyle(self, object_name):
        self.lineEdit.setObjectName(object_name)
        self.lineEdit.setStyleSheet(self.styleSheet())

    def setText(self, text):
        self.lineEdit.setText(text)

    def setLabel(self, text):
        self.label.setText(text)

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def setCompleter(self, items):
        if items is not None:
            _completer = QCompleter(items)
            _completer.setCompletionMode(QCompleter.PopupCompletion)
            _completer.setCaseSensitivity(Qt.CaseInsensitive)
            _completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
            _completer.setFilterMode(Qt.MatchContains)
            self.lineEdit.setCompleter(_completer)


class IntInput(QWidget):
    def __init__(self,
                 label: str = '',
                 orientation: str = HORIZONTAL,
                 value_range: Union[list, tuple, None] = None,
                 labelsize: Tuple[int] = (70, 22),
                 editsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, value_range, labelsize, editsize)

    def setupUi(self, label, orientation, value_range, labelsize, editsize):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedSize(*labelsize)

        self.validator = QIntValidator()
        if value_range is not None:
            self.validator.setRange(*value_range)

        self.lineEdit = QLineEdit()
        _width = editsize[0]
        _height = editsize[1]
        if _width is not None:
            self.lineEdit.setFixedWidth(_width)
        if _height is not None:
            self.lineEdit.setFixedHeight(_height)
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def disable(self):
        self.lineEdit.setEnabled(False)
        self.setStyle('off')

    def enable(self):
        self.lineEdit.setEnabled(True)
        self.setStyle("")

    def setStyle(self, object_name):
        self.lineEdit.setObjectName(object_name)
        self.lineEdit.setStyleSheet(self.styleSheet())

    def setText(self, text):
        self.lineEdit.setText(text)

    def setLabel(self, text):
        self.label.setText(text)

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)
