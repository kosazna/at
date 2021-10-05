# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication
from at.gui.button import Button
from at.gui.check import CheckInput
from at.gui.combo import ComboInput
from at.gui.filename import FileNameInput
from at.gui.input import StrInput, IntInput
from at.gui.io import FileInput, FileOutput, FolderInput
from at.gui.progress import ProgressBar
from at.gui.status import StatusIndicator
from at.gui.list import ListWidget

from pathlib import Path

from at.gui.helper import *

cssGuide = Path("D:/.temp/.dev/.aztool/at/gui/style.css").read_text()


class Dummy(QWidget):
    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.i = 0
        self.button1.clicked.connect(self.changeProgress)

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.layout = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutGeneral = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutComboCheck = QHBoxLayout()
        self.folderInput = FolderInput("Folder", parent=self, size=70)
        self.fileInput = FileInput("File In", parent=self, size=70)
        self.fileOutput = FileOutput("File Out", parent=self, size=70)
        self.filename = FileNameInput(
            "Filename", parent=self, size=(70, 200))
        self.input = StrInput(
            "Input", parent=self, completer=['Astota', 'Asttom'], size=(70, 200))
        self.inputInt = IntInput("Int", parent=self, size=(70, 200))
        self.combo = ComboInput(
            "Combo", items=["1", "2", "3"], parent=self, size=(70, 100))
        self.check = CheckInput("Check", parent=self)
        self.status = StatusIndicator(parent=self)
        self.statusSmall = StatusIndicator(
            label='Status', status='offline', parent=self, size=70)
        self.button1 = Button("accept", parent=self)
        self.button2 = Button("decline", parent=self)
        self.button3 = Button("process", parent=self)

        self.progress = ProgressBar()

        self.listWidget = ListWidget('Select Shapefiles', ['ASTENOT', 'ASTOTA',
                                                           'ASTTOM', 'PST',
                                                           'ROADS', 'VST',
                                                           'FBOUND'])

        self.layoutGeneral.addWidget(self.folderInput)
        self.layoutGeneral.addWidget(self.fileInput)
        self.layoutGeneral.addWidget(self.fileOutput)
        self.layoutGeneral.addWidget(self.filename)
        self.layoutGeneral.addWidget(self.input)
        self.layoutGeneral.addWidget(self.inputInt)

        self.layoutComboCheck.addWidget(self.combo)
        self.layoutComboCheck.addWidget(self.check, 1)
        self.layoutGeneral.addLayout(self.layoutComboCheck)
        self.layoutGeneral.addWidget(self.statusSmall)
        self.layoutGeneral.addWidget(self.listWidget)

        self.layoutButtons.addWidget(self.button1)
        self.layoutButtons.addWidget(self.button2)
        self.layoutButtons.addWidget(self.button3)

        self.layoutTop.addLayout(self.layoutGeneral)
        self.layoutTop.addLayout(self.layoutButtons)

        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.progress)

        self.setLayout(self.layout)

    def changeProgress(self):
        if self.i < self.progress.maximum():
            self.i += 10
            self.progress.setValueMaximum(self.i, 100)

        else:
            self.button2.enable('red')
            self.statusSmall.enable('Online')
            self.input.disable()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Dummy()
    ui.show()
    sys.exit(app.exec_())
