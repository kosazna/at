# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from at.gui.utils import set_size


class FileNameInput(QWidget):
    def __init__(self,
                 label: str = '',
                 placeholder: str = '',
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, labelsize, editsize)

    def setupUi(self, label, placeholder, labelsize, editsize):
        self.lineEdit = QLineEdit(parent=self)
        set_size(widget=self.lineEdit, size=editsize)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        regexp = QRegExp('[^\.\<\>:\"/\\\|\?\*]*')
        validator = QRegExpValidator(regexp, self.lineEdit)
        self.lineEdit.setValidator(validator)
        self.setPlaceholder(placeholder)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        if label:
            self.label = QLabel(parent=self)
            self.label.setText(label)
            set_size(widget=self.label, size=labelsize)
            layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

        self.setLayout(layout)

    def getText(self, suffix: Optional[str] = None):
        if suffix is not None:
            _stem = self.lineEdit.text()
            _suffix = suffix if suffix.startswith('.') else f".{suffix}"
            _filename = f"{_stem}{_suffix}"
            return _filename
        return self.lineEdit.text()

    def setText(self, text: str):
        self.lineEdit.setText(text)

    def setPlaceholder(self, text: str):
        self.lineEdit.setPlaceholderText(text)

    def setLabel(self, text: str):
        self.label.setText(text)
