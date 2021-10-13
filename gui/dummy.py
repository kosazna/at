# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from time import sleep
from typing import Any, Tuple, Union

from at.io.copy import batch_copy_file, copy_file
from at.gui.label import Label
from at.path import PathEngine
from at.auth.client import licensed, Authorize, AuthStatus
from at.gui.button import Button
from at.gui.check import CheckInput
from at.gui.combo import ComboInput
from at.gui.filename import FileNameInput
from at.gui.input import IntInput, StrInput
from at.gui.io import FileInput, FileOutput, FolderInput
from at.gui.list import ListWidget
from at.gui.popup import Popup, show_popup
from at.gui.progress import ProgressBar
from at.gui.status import StatusButton, StatusLabel
from at.gui.console import Console
from at.gui.utils import *
from at.gui.worker import run_thread
from at.logger import log
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignLeft when adding widget to layout

cssGuide = Path("D:/.temp/.dev/.aztool/at/gui/_style.css").read_text()

log.set_mode("GUI")
APPNAME = 'ktima'
paths = PathEngine(APPNAME)
authenticator = Authorize(APPNAME, paths.get_authfolder())


class Dummy(QWidget):
    def __init__(self,
                 size: Tuple[Union[int, None]] = (None, None),
                 parent=None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(size)
        self.i = 0
        self.button1.clicked.connect(self.button1action)
        self.button2.clicked.connect(self.button2action)
        self.button3.clicked.connect(self.button3action)
        self.threadpool = QThreadPool(parent=self)

    def setupUi(self, size):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        _width = size[0]
        _height = size[1]
        if _width is not None:
            self.setMinimumWidth(_width)
        if _height is not None:
            self.setMinimumHeight(_height)

        self.total_layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.layoutTop = QHBoxLayout()
        self.layoutGeneral = QVBoxLayout()
        self.layoutButtons = QVBoxLayout()
        self.layoutComboCheck = QHBoxLayout()

        self.pop = Popup("ktima")

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
        self.console = Console(size=(400, None), parent=self)

        self.customLabel1 = Label(icon='people-fill', label='aznavouridis.k', parent=self)
        self.customLabel2 = Label(icon='calendar-range-fill', label='2021-10-13', parent=self)
        self.customLabel3 = Label(icon='bar-chart-fill', label='2829', parent=self)

        # self.console.hide()

        self.listWidget.assignLoadFunc(self.load_content)

        self.layoutGeneral.addWidget(self.folderInput)
        self.layoutGeneral.addWidget(self.fileInput)
        self.layoutGeneral.addWidget(self.fileOutput)
        self.layoutGeneral.addWidget(self.filename)
        self.layoutGeneral.addWidget(self.input)
        self.layoutGeneral.addWidget(self.inputInt)
        self.layoutGeneral.addWidget(self.customLabel1)
        self.layoutGeneral.addWidget(self.customLabel2)
        self.layoutGeneral.addWidget(self.customLabel3)

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

        self.total_layout.addLayout(self.layout)
        self.total_layout.addWidget(self.console)

        self.setLayout(self.total_layout)

    def updateProgress(self, metadata: dict):
        if metadata:
            progress_now = metadata.get('pbar', None)
            progress_max = metadata.get('pbar_max', None)
            status = metadata.get('status', None)

            if progress_now is not None:
                self.progress.setValue(progress_now)
            if progress_max is not None:
                self.progress.setValue(progress_max)
            if status is not None:
                self.status.disable(str(status))

    def updateResult(self, status: Any):
        if status is not None:
            if isinstance(status, AuthStatus):
                if not status.authorised:
                    self.pop.error(status.info)
            elif isinstance(status, str):
                self.status.enable(status)

    def updateFinish(self):
        pass

    def button1action(self):
        if self.i < self.progress.maximum():
            self.i += 10
            self.progress.setValueMaximum(self.i, 100)

            log.info(self.listWidget.getCheckState('string'))
        else:
            self.button2.enable('red')
            self.statusSmall.changeStatus('Done', 'statusOk')
            self.input.disable()

    def button2action(self):
        run_thread(threadpool=self.threadpool,
                   function=self.copy_files,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def button3action(self):
        run_thread(threadpool=self.threadpool,
                   function=self.execute,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    @licensed(appname=APPNAME, domain=None)
    def execute(self, _progress):
        log.info("Starting Process")
        log.warning("Warning")
        log.error("Error")
        _progress.emit({'pbar': 20, 'status': 'something'})
        sleep(1)
        log.info("Processing...\n")
        _progress.emit({'pbar': 60, 'status': 'Still processing...'})
        sleep(2)
        log.success("Finished")
        _progress.emit({'pbar': 100})

        return 'Everything OK'

    def load_content(self):
        return ("ASTOTA", "ASTENOT", "ASTIK", "ROADS", "PST")

    def copy_files(self, _progress):
        all_files = list(Path("D:/.temp/bootstrap-icons-1.5.0").iterdir())
        _progress.emit({'pbar_max': len(all_files), 'status': 'Copying Files'})
        for idx, p in enumerate(all_files, 1):
            log.info(copy_file(p, "D:/.temp/copy_tests"))
            _progress.emit({'pbar': idx})


if __name__ == '__main__':

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = Dummy(size=(1000, None))
    ui.show()

    sys.exit(app.exec_())
