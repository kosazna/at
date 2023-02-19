# -*- coding: utf-8 -*-
from typing import Callable, Iterable, Optional, Tuple, Union

from at.gui.components.atpyqt import (QCompleter, QHBoxLayout, QIntValidator,
                                      QLabel, QLineEdit, Qt, QVBoxLayout,
                                      QWidget)
from at.gui.utils import HORIZONTAL, VERTICAL, set_size


class StrInput(QWidget):
    def __init__(self,
                 label: str = '',
                 orientation: str = HORIZONTAL,
                 completer: Optional[Union[list, tuple]] = None,
                 hidden: bool = False,
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, hidden, labelsize, editsize)
        self.setCompleter(completer)

    def setupUi(self, label, orientation, hidden, labelsize, editsize):
        self.lineEdit = QLineEdit(parent=self)
        set_size(widget=self.lineEdit, size=editsize)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if hidden:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()

        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        if label:
            self.label = QLabel(parent=self)
            self.label.setText(label)
            if orientation == HORIZONTAL:
                set_size(widget=self.label, size=labelsize)
            layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

        self.setLayout(layout)

    def disable(self):
        self.lineEdit.setEnabled(False)
        self.setStyle('off')

    def enable(self):
        self.lineEdit.setEnabled(True)
        self.setStyle("")

    def setStyle(self, object_name: str):
        self.lineEdit.setObjectName(object_name)
        self.lineEdit.setStyleSheet(self.styleSheet())

    def textChanged(self, function: Callable):
        self.lineEdit.textChanged.connect(function)

    def setText(self, text: str):
        self.lineEdit.setText(text)

    def setLabel(self, text: str):
        self.label.setText(text)

    def getText(self):
        return self.lineEdit.text()

    def setPlaceholder(self, text: str):
        self.lineEdit.setPlaceholderText(text)

    def setCompleter(self, items: Iterable[str]):
        if items is not None:
            _completer = QCompleter(items)
            _completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
            _completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            _completer.setModelSorting(QCompleter.ModelSorting.CaseInsensitivelySortedModel)
            _completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.lineEdit.setCompleter(_completer)


class IntInput(QWidget):
    def __init__(self,
                 label: str = '',
                 orientation: str = HORIZONTAL,
                 value_range: Optional[Union[list, tuple]] = None,
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, orientation, value_range, labelsize, editsize)

    def setupUi(self, label, orientation, value_range, labelsize, editsize):
        self.validator = QIntValidator()
        if value_range is not None:
            self.validator.setRange(*value_range)

        self.lineEdit = QLineEdit(parent=self)
        set_size(widget=self.lineEdit, size=editsize)
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        if orientation == VERTICAL:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()

        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        if label:
            self.label = QLabel(parent=self)
            self.label.setText(label)
            if orientation == HORIZONTAL:
                set_size(widget=self.label, size=labelsize)
            layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

        self.setLayout(layout)

    def disable(self):
        self.lineEdit.setEnabled(False)
        self.setStyle('off')

    def enable(self):
        self.lineEdit.setEnabled(True)
        self.setStyle("")

    def textChanged(self, function: Callable):
        self.lineEdit.textChanged.connect(function)

    def setStyle(self, object_name: str):
        self.lineEdit.setObjectName(object_name)
        self.lineEdit.setStyleSheet(self.styleSheet())

    def setText(self, text: str):
        self.lineEdit.setText(text)

    def setLabel(self, text: str):
        self.label.setText(text)

    def getText(self):
        try:
            return int(self.lineEdit.text())
        except ValueError:
            return 0

    def getInt(self):
        return int(self.lineEdit.text())

    def setPlaceholder(self, text: str):
        self.lineEdit.setPlaceholderText(text)
