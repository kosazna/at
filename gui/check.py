# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QCheckBox, QWidget


class CheckInput(QCheckBox):
    def __init__(self,
                 label: str = '',
                 checked: bool = True,
                 height: int = 22,
                 parent: QWidget = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, checked, height)

    def setupUi(self, label, checked, height):
        self.setText(label)
        self.setObjectName("Check")
        self.setChecked(checked)
        self.setFixedHeight(height)

    def enable(self, text=''):
        self.setEnabled(True)
        self.setText(text)

    def disable(self):
        self.setEnabled(False)
        self.setText('')

    def subscribe(self, func):
        self.stateChanged.connect(func)
