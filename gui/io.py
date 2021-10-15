# -*- coding: utf-8 -*-
import os
from typing import Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QToolButton, QVBoxLayout, QWidget)

from at.gui.utils import *


class IOWidget(QWidget):
    lastVisit = ''
    ok = ("ok", "Path OK")
    warning = ("warning", "Path Warning")
    error = ("error", "Path does not exist")

    def __init__(self,
                 label: str = '',
                 placeholder: str = PATH_PLACEHOLDER,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 25),
                 editsize: Tuple[Union[int, None]] = (None, 25),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation, labelsize, editsize)
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))
        self.browseCallback = None

    def setupUi(self, label, placeholder, orientation, labelsize, editsize):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setFixedSize(*labelsize)

        self.lineEdit = QLineEdit()
        _width = editsize[0]
        _height = editsize[1]
        if _width is not None:
            self.lineEdit.setFixedWidth(_width)
        if _height is not None:
            self.lineEdit.setFixedHeight(_height)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)

        self.button = QToolButton(self)
        self.button.setText('...')
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setFixedSize(_height + 2, _height - 1)

        if orientation == HORIZONTAL:
            layout = QHBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.lineEdit)
            layout.addWidget(self.button)
        else:
            layout = QVBoxLayout()
            inner = QHBoxLayout()
            layout.addWidget(self.label)
            inner.addWidget(self.lineEdit)
            inner.addWidget(self.button)
            layout.addLayout(inner)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)
        self.setLayout(layout)

    @classmethod
    def setLastVisit(cls, folder):
        cls.lastVisit = folder

    def setBrowseCallback(self, func):
        self.browseCallback = func

    def getText(self):
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)
        self.lastVisit = text

    def setPlaceholder(self, text):
        self.lineEdit.setPlaceholderText(text)

    def setOffset(self, offset):
        self.label.setFixedWidth(offset)

    def setMaximumEditWidth(self, maxw):
        self.lineEdit.setMaximumWidth(maxw)

    def setMinimumEditWidth(self, minw):
        self.lineEdit.setMinimumWidth(minw)

    def setMaximumLabelWidth(self, maxw):
        self.label.setMaximumWidth(maxw)

    def setMinimumLabelWidth(self, minw):
        self.label.setMinimumWidth(minw)

    def updateStyle(self, status):
        self.lineEdit.setObjectName(status)
        self.lineEdit.setStyleSheet(self.styleSheet())
        if status == self.ok[0]:
            self.lineEdit.setToolTip(self.ok[1])
        elif status == self.warning[0]:
            self.lineEdit.setToolTip(self.warning[1])
        elif status == self.error[0]:
            self.lineEdit.setToolTip(self.error[1])
        else:
            self.lineEdit.setToolTip("")

    def browse(self):
        pass

    def pathExists(self, path):
        pass


class FolderInput(IOWidget):
    warning = ("warning", "Path should be a folder")

    def __init__(self,
                 label: str = '',
                 placeholder: str = PATH_PLACEHOLDER,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 22),
                 editsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         labelsize=labelsize,
                         editsize=editsize,
                         * args,
                         **kwargs)

    def browse(self):
        file_path = QFileDialog.getExistingDirectory(directory=self.lastVisit)
        if file_path:
            self.lineEdit.setText(file_path)
            IOWidget.setLastVisit(file_path)

            if self.browseCallback is not None:
                self.browseCallback()

    def pathExists(self, path):
        if path:
            if os.path.exists(path):
                if os.path.isdir(path):
                    self.updateStyle("ok")
                else:
                    self.updateStyle("warning")
            else:
                self.updateStyle("error")
        else:
            self.updateStyle("")


class FileInput(IOWidget):
    warning = ("warning", "Path should be a file")

    def __init__(self,
                 label: str = '',
                 placeholder: str = PATH_PLACEHOLDER,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 22),
                 editsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         labelsize=labelsize,
                         editsize=editsize,
                         * args,
                         **kwargs)

    def browse(self):
        filename = QFileDialog.getOpenFileName(directory=self.lastVisit)
        file_path = filename[0]
        if file_path:
            self.lineEdit.setText(file_path)
            IOWidget.setLastVisit(file_path)

            if self.browseCallback is not None:
                self.browseCallback()

    def pathExists(self, path):
        if path:
            if os.path.exists(path):
                if os.path.isfile(path):
                    self.updateStyle("ok")
                else:
                    self.updateStyle("warning")
            else:
                self.updateStyle("error")
        else:
            self.updateStyle("")


class FileOutput(IOWidget):
    def __init__(self,
                 label: str = '',
                 placeholder: str = PATH_PLACEHOLDER,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 22),
                 editsize: Tuple[Union[int, None]] = (None, 22),
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         labelsize=labelsize,
                         editsize=editsize,
                         * args,
                         **kwargs)

    def browse(self):
        filename = QFileDialog.getSaveFileName(directory=self.lastVisit,
                                               caption="Save file as")

        file_path = filename[0]

        # if filename[0].endswith('.xlsx'):
        #     file_path = filename[0]
        # else:
        #     file_path = filename[0] + '.xlsx'

        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path
