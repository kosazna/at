# -*- coding: utf-8 -*-
from typing import Optional
from PyQt5.QtWidgets import QWidget, QFrame


class HLine(QFrame):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("HLine")
        self.setLineWidth(2)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
