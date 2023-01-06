# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from at.gui.components.atpyqt import (QFont, QHBoxLayout, QLabel, QPixmap, Qt,
                                      QWidget)
from at.gui.utils import set_size


class Label(QWidget):
    def __init__(self,
                 icon: str,
                 label: str = '',
                 fontsize=9,
                 italic=False,
                 iconsize: Tuple[int] = (24, 24),
                 labelsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(icon, label, fontsize, italic, iconsize, labelsize)

    def setupUi(self, icon, label, fontsize, italic, iconsize, labelsize):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(4)

        SEGOE = QFont("Segoe UI", fontsize)
        SEGOE.setItalic(italic)

        self.iconLabel = QLabel(parent=self)
        self.iconLabel.setFixedSize(*iconsize)
        self.iconLabel.setPixmap(QPixmap(f":/bootstrap/icons/{icon}.svg"))
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.statusLabel = QLabel(parent=self)
        self.statusLabel.setObjectName('infoLabel')
        self.statusLabel.setFont(SEGOE)
        self.statusLabel.setText(label)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        set_size(widget=self.statusLabel, size=labelsize)

        layout.addWidget(self.iconLabel)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def setText(self, text: str):
        self.statusLabel.setText(text)
