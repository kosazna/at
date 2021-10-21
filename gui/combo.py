# -*- coding: utf-8 -*-
from typing import Iterable, Optional, Union

from at.gui.utils import set_size
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget


class ComboInput(QWidget):
    def __init__(self,
                 label: str = '',
                 items: Optional[Union[list, tuple]] = None,
                 labelsize: tuple = (70, 24),
                 combosize: tuple = (150, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, items, labelsize, combosize)

    def setupUi(self, label, items, labelsize, combosize):
        self.comboEdit = QComboBox()
        set_size(widget=self.comboEdit, size=combosize)
        self.comboEdit.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        if label:
            self.label = QLabel(parent=self)
            self.label.setText(label)
            set_size(widget=self.label, size=labelsize)
            layout.addWidget(self.label)
        layout.addWidget(self.comboEdit, 1, alignment=Qt.AlignLeft)
        self.setLayout(layout)

        if items is not None:
            self.comboEdit.addItems(items)

    def getCurrentText(self):
        return self.comboEdit.currentText()

    def setCurrentText(self, text: str):
        self.comboEdit.setCurrentText(text)

    def getCurrentIndex(self):
        return self.comboEdit.currentIndex()

    def addItems(self, items: Iterable[str]):
        self.comboEdit.addItems(items)

    def clearItems(self):
        self.comboEdit.clear()

    def setLabel(self, text: str):
        self.label.setText(text)

    def subscribe(self, func):
        self.comboEdit.currentTextChanged.connect(func)
