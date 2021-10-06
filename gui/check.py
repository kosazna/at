# -*- coding: utf-8 -*-
from helper import *

from PyQt5.QtWidgets import QCheckBox, QWidget


class CheckInput(QCheckBox):
    def __init__(self,
                 label: str = '',
                 checked: bool = True,
                 parent: QWidget = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, checked)

    def setupUi(self, label, checked):
        self.setText(label)
        self.setObjectName("Check")
        self.setChecked(checked)

    def enable(self, text=''):
        self.setEnabled(True)
        self.setText(text)

    def disable(self):
        self.setEnabled(False)
        self.setText('')

    def subscribe(self, func):
        self.stateChanged.connect(func)
