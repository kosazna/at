# -*- coding: utf-8 -*-
from typing import Tuple, Union
from pathlib import Path
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QApplication, QTextBrowser, QWidget

from at.logger import Logger


class TextBox(QTextBrowser):
    def __init__(self,
                 logger: Logger,
                 size: Union[Tuple[int], None] = None,
                 parent: Union[QWidget, None] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.logger = logger
        self.setupUi(size)

    def setupUi(self, size):
        self.setReadOnly(True)

        if size is not None:
            self.setFixedSize(*size)

    def addText(self):
        self.setText(self.logger.get_content())
        self.moveCursor(QTextCursor.End)


if __name__ == '__main__':
    import sys

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = TextBox(size=(600, 400))
    ui.show()

    sys.exit(app.exec_())
