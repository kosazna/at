# -*- coding: utf-8 -*-
from typing import Tuple, Union

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget


class FileNameInput(QWidget):
    def __init__(self,
                 label: str = '',
                 placeholder: str = '',
                 labelsize: Tuple[int] = (70, 22),
                 editsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, labelsize, editsize)

    def setupUi(self, label, placeholder, labelsize, editsize):
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
        regexp = QRegExp('[^\.\<\>:\"/\\\|\?\*]*')
        validator = QRegExpValidator(regexp, self.lineEdit)
        self.lineEdit.setValidator(validator)
        self.setPlaceholder(placeholder)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)
        self.setLayout(layout)

    def getText(self, suffix=None):
        if suffix is not None:
            _stem = self.lineEdit.text()
            _suffix = suffix if suffix.startswith('.') else f".{suffix}"
            _filename = f"{_stem}{_suffix}"
            return _filename
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)
