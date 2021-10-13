# -*- coding: utf-8 -*-
from typing import Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget


class Label(QWidget):
    def __init__(self,
                 icon: str,
                 label: str = '',
                 iconsize: Tuple[int] = (22, 22),
                 labelsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(icon, label, iconsize, labelsize)

    def setupUi(self, icon, label, iconsize, labelsize):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(4)

        self.iconLabel = QLabel(parent=self)
        self.iconLabel.setFixedSize(*iconsize)
        self.iconLabel.setPixmap(QPixmap(f":/bootstrap/icons/{icon}.svg"))
        self.iconLabel.setAlignment(Qt.AlignCenter)

        self.statusLabel = QLabel(parent=self)
        self.statusLabel.setObjectName('statusLabel')
        self.statusLabel.setText(label)
        self.statusLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        _width = labelsize[0]
        _height = labelsize[1]
        if _width is not None:
            self.statusLabel.setFixedWidth(_width)
        if _height is not None:
            self.statusLabel.setFixedHeight(_height)

        layout.addWidget(self.iconLabel)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)
