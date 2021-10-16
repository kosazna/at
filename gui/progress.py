# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar, QWidget
from at.gui.utils import set_size


class ProgressBar(QProgressBar):
    def __init__(self,
                 size: Tuple[Optional[int]] = (None, 22),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(size)

    def setupUi(self, size):
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        set_size(widget=self, size=size)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def setStyle(self, object_name):
        self.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def setValueMaximum(self, current_value, maximum):
        self.setMaximum(maximum)
        self.setValue(current_value)
