# -*- coding: utf-8 -*-

from pathlib import Path

from at.gui.button import Button
from at.gui.check import CheckInput
from at.gui.combo import ComboInput
from at.gui.filename import FileNameInput
from at.gui.helper import *
from at.gui.input import IntInput, StrInput
from at.gui.io import FileInput, FileOutput, FolderInput
from at.gui.list import ListWidget
from at.gui.progress import ProgressBar
from at.gui.status import StatusButton, StatusLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

cssGuide = Path("D:/.temp/.dev/.aztool/at/gui/_style.css").read_text()

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignLeft when adding widget to layout


class Dummy(QWidget):
    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi()
        self.i = 0
        self.button1.clicked.connect(self.button1action)
        self.button2.clicked.connect(self.button2action)

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.layout = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutGeneral = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutComboCheck = QHBoxLayout()
        self.folderInput = FolderInput("Folder", parent=self)
        self.fileInput = FileInput("File In", parent=self)
        self.fileOutput = FileOutput("File Out", parent=self)
        self.filename = FileNameInput("Filename", parent=self)
        self.input = StrInput(
            "Input", parent=self, completer=['Astota', 'Asttom'])
        self.inputInt = IntInput("Int", parent=self)
        self.combo = ComboInput(
            "Combo", items=["1", "2", "3"], parent=self)
        self.check = CheckInput("Check", parent=self)
        self.status = StatusButton(parent=self, size=600)
        self.statusSmall = StatusLabel(
            label='Status', status='offline', parent=self)
        self.button1 = Button("accept", parent=self)
        self.button2 = Button("decline", parent=self)
        self.button3 = Button("process", parent=self)

        self.progress = ProgressBar()

        self.listWidget = ListWidget('Select Shapefiles')
        self.listWidget.assignLoadFunc(self.button2action)

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
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status)

        self.setLayout(self.layout)

    def button1action(self):
        if self.i < self.progress.maximum():
            self.i += 10
            self.progress.setValueMaximum(self.i, 100)

            print(self.listWidget.getCheckState('list'))
        else:
            self.button2.enable('red')
            self.statusSmall.changeStatus('Done', 'statusOk')
            self.input.disable()

    def button2action(self):
        p = Path(
            "D:/.temp/KT5-16_ΠΑΡΑΔΟΣΗ_30-09-2021/ΕΝΔΙΑΜΕΣΗ ΥΠΟΒΟΛΗ ΚΤΗΜΑΤΟΛΟΓΙΚΗΣ ΒΑΣΗΣ ΧΩΡΙΚΩΝ ΣΤΟΙΧΕΙΩΝ/SHAPE")

        return [f.stem for f in p.glob('**/*.mdb')]


if __name__ == '__main__':
    import sys

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = Dummy()
    ui.show()

    sys.exit(app.exec_())
