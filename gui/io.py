# -*- coding: utf-8 -*-
import os
from typing import Optional, Tuple

from at.gui.utils import HORIZONTAL, PATH_PLACEHOLDER, VERTICAL, set_size
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QToolButton, QVBoxLayout, QWidget)


class IOWidget(QWidget):
    lastVisit = ''
    ok = ("ok", "Path OK")
    warning = ("warning", "Path Warning")
    error = ("error", "Path does not exist")

    def __init__(self,
                 label: str = '',
                 placeholder: str = PATH_PLACEHOLDER,
                 orientation: str = HORIZONTAL,
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
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
        set_size(widget=self.label, size=labelsize)

        self.lineEdit = QLineEdit()
        set_size(widget=self.lineEdit, size=editsize)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)

        self.button = QToolButton(self)
        qicon = QIcon()
        qicon.addFile(f":/bootstrap/icons/folder-symlink.svg", QSize(16, 16),
                      QIcon.Normal, QIcon.Off)
        self.button.setIcon(qicon)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setFixedSize(editsize[1], editsize[1] - 2)

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
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         labelsize=labelsize,
                         editsize=editsize,
                         *args,
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
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         labelsize=labelsize,
                         editsize=editsize,
                         *args,
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
                 labelsize: Tuple[int] = (70, 24),
                 editsize: Tuple[Optional[int]] = (None, 24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         labelsize=labelsize,
                         editsize=editsize,
                         *args,
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
