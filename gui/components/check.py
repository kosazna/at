# -*- coding: utf-8 -*-
from typing import Optional

from at.gui.components import QCheckBox, QWidget
from at.gui.utils import set_size


class CheckInput(QCheckBox):
    def __init__(self,
                 label: str = '',
                 checked: bool = True,
                 height: int = 24,
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, checked, height)

    def setupUi(self, label, checked, height):
        self.setText(label)
        self.setObjectName("Check")
        self.setChecked(checked)
        set_size(widget=self, height=height)

    def enable(self, text=''):
        self.setEnabled(True)
        self.setText(text)

    def disable(self):
        self.setEnabled(False)
        self.setText('')

    def subscribe(self, func):
        self.stateChanged.connect(func)

    def setLabel(self, text:str):
        self.setText(text)
