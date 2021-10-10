# -*- coding: utf-8 -*-
from typing import Union

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMessageBox

popup_button_map = {
    'ok': QMessageBox.Ok,
    'open': QMessageBox.Open,
    'save': QMessageBox.Save,
    'cancel': QMessageBox.Cancel,
    'close': QMessageBox.Close,
    'yes': QMessageBox.Yes,
    'no': QMessageBox.No,
    'abort': QMessageBox.Abort,
    'retry': QMessageBox.Retry,
    'ignore': QMessageBox.Ignore}

popup_status_map = {
    'info': QMessageBox.Information,
    'question': QMessageBox.Question,
    'warning': QMessageBox.Warning,
    'error': QMessageBox.Critical}


def show_popup(appname: str = 'Dialog',
               primary: str = '',
               secondary: str = '',
               details: str = '',
               status: str = 'info',
               buttons: Union[list, tuple, None] = None):
    msg = QMessageBox()
    msg.setWindowTitle(f"{appname}")
    msg.setIcon(popup_status_map[status])

    if primary:
        msg.setText(primary)
    if secondary:
        msg.setInformativeText(secondary)
    if details:
        msg.setDetailedText(details)

    if buttons is not None:
        for button in buttons:
            if button in popup_button_map:
                msg.addButton(popup_button_map[button])

    return msg.exec_()


if __name__ == '__main__':
    import sys

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')
    result = show_popup(
        primary='Something went wrong with validating dataset', buttons=('ok', 'cancel', 'ignore'))

    if result == QMessageBox.Ok:
        print('kostas')
    else:
        print('azna')
