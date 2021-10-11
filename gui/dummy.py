# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from time import sleep

from at.gui.button import Button
from at.gui.check import CheckInput
from at.gui.combo import ComboInput
from at.gui.filename import FileNameInput
from at.gui.input import IntInput, StrInput
from at.gui.io import FileInput, FileOutput, FolderInput
from at.gui.list import ListWidget
from at.gui.popup import Popup
from at.gui.progress import ProgressBar
from at.gui.status import StatusButton, StatusLabel
from at.gui.textbox import TextBox
from at.gui.utils import *
from at.gui.worker import run_thread
from at.logger import log
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

cssGuide = Path("D:/.temp/.dev/.aztool/at/gui/_style.css").read_text()

log.set_mode("GUI")

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
        self.button3.clicked.connect(self.button3action)
        self.threadpool = QThreadPool(parent=self)

    def setupUi(self):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.resize(700, 700)
        self.layout = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutGeneral = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutComboCheck = QHBoxLayout()

        self.pop = Popup("atcrawl")

        self.folderInput = FolderInput(label="Folder",
                                       placeholder=PATH_PLACEHOLDER,
                                       orientation=HORIZONTAL,
                                       labelsize=(70, 22),
                                       editsize=(None, 22),
                                       parent=self)
        self.fileInput = FileInput(label="File In",
                                   placeholder=PATH_PLACEHOLDER,
                                   orientation=HORIZONTAL,
                                   labelsize=(70, 22),
                                   editsize=(None, 22),
                                   parent=self)
        self.fileOutput = FileOutput(label="File Out",
                                     placeholder=PATH_PLACEHOLDER,
                                     orientation=HORIZONTAL,
                                     labelsize=(70, 22),
                                     editsize=(None, 22),
                                     parent=self)
        self.filename = FileNameInput(label="Filename",
                                      placeholder='',
                                      labelsize=(70, 22),
                                      editsize=(None, 22),
                                      parent=self)
        self.input = StrInput(label="Input",
                              orientation=HORIZONTAL,
                              completer=['Astota', 'Asttom'],
                              hidden=False,
                              labelsize=(70, 22),
                              editsize=(None, 22),
                              parent=self)
        self.inputInt = IntInput(label="Int",
                                 orientation=HORIZONTAL,
                                 value_range=None,
                                 labelsize=(70, 22),
                                 editsize=(None, 22),
                                 parent=self)
        self.combo = ComboInput(label="Combo",
                                items=["1", "2", "3"],
                                labelsize=(70, 22),
                                combosize=(150, 22),
                                parent=self)
        self.check = CheckInput(label="Check",
                                checked=True,
                                height=22,
                                parent=self)
        self.status = StatusButton(status='',
                                   size=(None, 22),
                                   parent=self)
        self.statusSmall = StatusLabel(label='Status',
                                       status='offline',
                                       labelsize=(70, 22),
                                       statussize=(100, 22),
                                       parent=self)
        self.button1 = Button(label="accept",
                              color=None,
                              size=(70, 22),
                              parent=self)
        self.button2 = Button(label="decline",
                              color=None,
                              size=(70, 22),
                              parent=self)
        self.button3 = Button(label="process",
                              color=None,
                              size=(70, 22),
                              parent=self)
        self.progress = ProgressBar(size=(None, 22),
                                    parent=self)
        self.listWidget = ListWidget(label='Select Shapefiles',
                                     labelsize=(200, 22),
                                     widgetsize=(None, 220),
                                     parent=self)
        self.listWidget.assignLoadFunc(self.load_content)
        self.textBox = TextBox(size=(None, 200), parent=self)

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
        self.layout.addWidget(self.textBox)

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
        log.warning('Ok\n')
        log.error('Wrong')
        log.success('Done')
        log.info('\nfinished\n')

    def button3action(self):
        run_thread(self.threadpool, self.execute)
        self.threadpool.clear()

    def execute(self, _progress, _popup):
        log.info("Starting Process")
        sleep(1)
        log.info("Processing...\n")
        sleep(2)
        log.success("Finished")

    def load_content(self):
        return ("ASTOTA", "ASTENOT", "ASTIK", "ROADS", "PST")


if __name__ == '__main__':

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = Dummy()
    ui.show()

    sys.exit(app.exec_())
