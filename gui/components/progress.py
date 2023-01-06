# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from at.gui.components.atpyqt import QProgressBar, Qt, QWidget
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
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def setStyle(self, object_name: str):
        self.setObjectName(object_name)
        self.setStyleSheet(self.styleSheet())

    def setValueMaximum(self, current_value: int, maximum: int):
        self.setMaximum(maximum)
        self.setValue(current_value)
