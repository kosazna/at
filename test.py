# import subprocess

# a = subprocess.check_output("D:/.temp/.dev/.aztool/atauth/dist/auth.exe --appname atcrawl")

# print(eval(a))

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout,
                             QWidget, QTextBrowser, QPushButton)
from time import sleep
import logging


class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s\n' % record)
        # originally: XStream.stdout().write("{}\n".format(record))


logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if (not self.signalsBlocked()):
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if (not XStream._stdout):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if (not XStream._stderr):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class MyDialog(QWidget):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self._console = QTextBrowser(self)
        self._button = QPushButton(self)
        self._button.setText('Test Me')

        layout = QVBoxLayout()
        layout.addWidget(self._console)
        layout.addWidget(self._button)
        self.setLayout(layout)

        XStream.stdout().messageWritten.connect(self._console.insertPlainText)
        XStream.stderr().messageWritten.connect(self._console.insertPlainText)

        self._button.clicked.connect(self.test)

    def test(self):
        logger.debug('debug message')
        sleep(1)
        logger.info('info message')
        logger.warning('warning message')
        sleep(2)
        logger.error('error message')
        print('Old school hand made print message')


if (__name__ == '__main__'):
    app = None
    if (not QApplication.instance()):
        app = QApplication([])
    dlg = MyDialog()
    dlg.show()
    if (app):
        app.exec_()
