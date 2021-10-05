# -*- coding: utf-8 -*-
import os

from helper import *
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QCursor, QFont, QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QSizePolicy, QStackedLayout, QStyle,
                             QToolButton, QVBoxLayout, QWidget, QProgressBar)


class IOWidget(QWidget):
    lastVisit = ''
    ok = ("InputOk", "Path OK")
    warning = ("InputWarn", "Path Warning")
    error = ("InputError", "Path does not exist")

    def __init__(self,
                 label='',
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size=70,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(label, placeholder, orientation, size)
        self.button.clicked.connect(self.browse)
        self.lineEdit.textChanged.connect(lambda x: self.pathExists(x))
        self.browseCallback = None

    def setupUi(self, label, placeholder, orientation, size):
        self.label = QLabel()
        self.label.setText(label)
        self.label.setObjectName(f"Label{size}")
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("InputDefault")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPlaceholder(placeholder)
        self.button = QToolButton()
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setText("2")
        self.button.setObjectName("Browse")
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
    warning = ("InputWarn", "Path should be a folder")

    def __init__(self,
                 label="",
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size=70,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         size=size,
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
                    self.updateStyle("InputOk")
                else:
                    self.updateStyle("InputWarn")
            else:
                self.updateStyle("InputError")
        else:
            self.updateStyle("InputDefault")


class FileInput(IOWidget):
    warning = ("InputWarn", "Path should be a folder")

    def __init__(self,
                 label="",
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size=70,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         size=size,
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
                    self.updateStyle("InputOk")
                else:
                    self.updateStyle("InputWarn")
            else:
                self.updateStyle("InputError")
        else:
            self.updateStyle("InputDefault")


class FileOutput(IOWidget):
    def __init__(self,
                 label="",
                 placeholder=PATH_PLACEHOLDER,
                 parent=None,
                 orientation=HORIZONTAL,
                 size=70,
                 *args,
                 **kwargs):
        super().__init__(label=label,
                         placeholder=placeholder,
                         parent=parent,
                         orientation=orientation,
                         size=size,
                         *args,
                         **kwargs)

    def browse(self):
        filename = QFileDialog.getSaveFileName(directory=self.lastVisit,
                                               caption="Save file as",
                                               initialFilter='*.xlsx')

        file_path = None

        if filename[0].endswith('.xlsx'):
            file_path = filename[0]
        else:
            file_path = filename[0] + '.xlsx'

        if file_path:
            self.lineEdit.setText(file_path)
            self.lastVisit = file_path
