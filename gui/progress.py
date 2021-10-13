# -*- coding: utf-8 -*-
from typing import Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar, QWidget


class ProgressBar(QProgressBar):
    def __init__(self,
                 size: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(size)

    def setupUi(self, size):
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        _width = size[0]
        _height = size[1]
        if _width is not None:
            self.setFixedWidth(_width)
        if _height is not None:
            self.setFixedHeight(_height)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def setStyle(self, object_name):
        self.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def setValueMaximum(self, current_value, maximum):
        self.setMaximum(maximum)
        self.setValue(current_value)
