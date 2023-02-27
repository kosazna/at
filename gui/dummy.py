# -*- coding: utf-8 -*-
import atexit
import sys
from pathlib import Path
from time import sleep
from typing import Any, Tuple, Union

from at.auth.client import Authorize, AuthStatus, licensed
from at.gui.atwidget import AtWidget
from at.gui.components import *
from at.gui.utils import *
from at.gui.utils import validateParams
from at.gui.worker import run_thread
from at.io.copyfuncs import batch_copy_file, copy_file
from at.io.utils import write_json
from at.logger import log
from at.path import PathEngine

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignmentFlag.AlignLeft when adding widget to layout

cssGuide = Path().cwd().joinpath("gui/css/_style.css").read_text()

log.set_mode("GUI")
APPNAME = 'ktima'
paths = PathEngine(APPNAME)
# authenticator = Authorize(APPNAME, paths.get_authfolder())


class Dummy(AtWidget):
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

        self.folderInput = FolderInput(label="Folder",
                                       placeholder=PATH_PLACEHOLDER,
                                       orientation=VERTICAL,
                                       labelsize=(70, 24),
                                       editsize=(None, 24),
                                       parent=self)
        self.fileInput = FileInput(label="File In",
                                   placeholder=PATH_PLACEHOLDER,
                                   orientation=HORIZONTAL,
                                   labelsize=(70, 24),
                                   editsize=(None, 24),
                                   parent=self)
        self.fileOutput = FileOutput(label="File Out",
                                     placeholder=PATH_PLACEHOLDER,
                                     orientation=HORIZONTAL,
                                     labelsize=(70, 24),
                                     editsize=(None, 24),
                                     parent=self)
        self.filename = FileNameInput(label="Filename",
                                      placeholder='',
                                      labelsize=(70, 24),
                                      editsize=(None, 24),
                                      parent=self)
        self.input = StrInput(label="Input",
                              orientation=HORIZONTAL,
                              completer=['Astota', 'Asttom'],
                              hidden=False,
                              labelsize=(70, 24),
                              editsize=(None, 24),
                              parent=self)
        self.inputInt = IntInput(label="Int",
                                 orientation=HORIZONTAL,
                                 value_range=None,
                                 labelsize=(70, 24),
                                 editsize=(None, 24),
                                 parent=self)
        self.combo = ComboInput(label="Combo",
                                items=["1", "2", "3"],
                                labelsize=(70, 24),
                                combosize=(150, 24),
                                parent=self)
        self.check = CheckInput(label="Check",
                                checked=True,
                                height=24,
                                parent=self)
        self.status = StatusButton(status='',
                                   size=(None, 24),
                                   parent=self)
        self.statusSmall = StatusLabel(label='Status',
                                       status='offline',
                                       labelsize=(70, 24),
                                       statussize=(100, 24),
                                       parent=self)
        self.button1 = Button(label="accept",
                              color=None,
                              icon='x',
                              size=(70, 24),
                              parent=self)
        self.button2 = Button(label="decline",
                              color=None,
                              size=(70, 24),
                              parent=self)
        self.button3 = Button(label="process",
                              color=None,
                              size=(70, 24),
                              parent=self)
        self.progress = ProgressBar(size=(None, 24),
                                    parent=self)
        self.listWidget = ListWidget(label='Select Shapefiles',
                                     labelsize=(200, 24),
                                     widgetsize=(None, 240),
                                     parent=self)
        self.console = Console(size=(400, None),
                               parent=self)
        self.customLabel1 = Label(icon='people-fill',
                                  label='aznavouridis.k',
                                  parent=self)
        self.customLabel2 = Label(icon='calendar-range-fill',
                                  label='2021-10-13',
                                  parent=self)
        self.customLabel3 = Label(icon='bar-chart-fill',
                                  label='2829',
                                  parent=self)
        self.filter = FilterFileSelector('Φιλτρα', parent=self)

        self.listWidget.assignLoadFunc(self.load_content)

        self.layoutComboCheck.addWidget(self.combo)
        self.layoutComboCheck.addWidget(self.check, 1)

        self.layoutGeneral.addWidget(self.folderInput)
        self.layoutGeneral.addWidget(self.fileInput)
        self.layoutGeneral.addWidget(self.fileOutput)
        self.layoutGeneral.addWidget(self.filename)
        self.layoutGeneral.addWidget(self.input)
        self.layoutGeneral.addWidget(self.inputInt)
        self.layoutGeneral.addWidget(self.customLabel1)
        self.layoutGeneral.addWidget(self.customLabel2)
        self.layoutGeneral.addWidget(self.customLabel3)
        self.layoutGeneral.addLayout(self.layoutComboCheck)
        self.layoutGeneral.addWidget(self.statusSmall)
        self.layoutGeneral.addWidget(self.listWidget)
        self.layoutGeneral.addWidget(self.filter)

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

    def getParams(self):
        _params = {
            'inputStr': self.input.getText(),
            'inputInt': self.inputInt.getText()
        }

        return _params

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

    @validateParams
    def execute(self, _progress):
        log.info("Starting Process")
        log.warning("Warning")
        log.error("Error")
        _progress.emit({'progress': (20,100), 'statusSmall': ('azna', 'statusError')})
        sleep(1)
        log.info("Processing...\n")
        _progress.emit({'progress': (60,100), 'statusSmall': ('azna', 'statusWarning')})
        sleep(2)
        log.success("Finished")
        _progress.emit({'progress': (100,100), 'statusSmall': ('azna', 'statusOk')})

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

    # @atexit.register
    # def terminate():
    #     print("finished")

    def appExec():
        SEGOE = QFont("Segoe UI", 9)

        app = QApplication(sys.argv)
        app.setFont(SEGOE)
        app.setStyle('Fusion')

        ui = Dummy(size=(1000, None))
        ui.show()
        app.exec()
        # log.set_mode("CLI")
        # write_json("D:/test.json", {"name": "kostas"})

        

    sys.exit(appExec())
