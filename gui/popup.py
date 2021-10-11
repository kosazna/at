# -*- coding: utf-8 -*-
from typing import Union

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMessageBox

pbutton = {
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

pstatus = {
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

    msg.setIcon(pstatus[status])

    if primary:
        msg.setText(primary)
    if secondary:
        msg.setInformativeText(secondary)
    if details:
        msg.setDetailedText(details)

    if buttons is not None:
        for button in buttons:
            if button in pbutton:
                msg.addButton(pbutton[button])

    user_action = msg.exec_()
    msg.destroy()

    for button_action in pbutton:
        if user_action == pbutton[button_action]:
            return button_action
    return None


class Popup(QMessageBox):
    def __init__(self, appname: str = 'Dialog') -> None:
        self.appname = appname

    def info(self,
             primary: str = '',
             secondary: str = '',
             details: str = '',
             buttons: Union[list, tuple, None] = None):
        msg = QMessageBox()
        msg.setWindowTitle(f"{self.appname}")
        msg.setIcon(pstatus['info'])

        if primary:
            msg.setText(primary)
        if secondary:
            msg.setInformativeText(secondary)
        if details:
            msg.setDetailedText(details)

        if buttons is not None:
            for button in buttons:
                if button in pbutton:
                    msg.addButton(pbutton[button])

        user_action = msg.exec_()
        msg.destroy()

        for button_action in pbutton:
            if user_action == pbutton[button_action]:
                return button_action
        return None

    def warning(self,
                primary: str = '',
                secondary: str = '',
                details: str = '',
                buttons: Union[list, tuple, None] = None):
        msg = QMessageBox()
        msg.setWindowTitle(f"{self.appname}")
        msg.setIcon(pstatus['warning'])

        if primary:
            msg.setText(primary)
        if secondary:
            msg.setInformativeText(secondary)
        if details:
            msg.setDetailedText(details)

        if buttons is not None:
            for button in buttons:
                if button in pbutton:
                    msg.addButton(pbutton[button])

        user_action = msg.exec_()
        msg.destroy()

        for button_action in pbutton:
            if user_action == pbutton[button_action]:
                return button_action
        return None

    def error(self, primary: str = ''):
        msg = QMessageBox()
        msg.setWindowTitle(f"{self.appname}")
        msg.setIcon(pstatus['error'])
        msg.setText(primary)
        msg.addButton(pbutton['close'])

        user_action = msg.exec_()
        msg.destroy()

        for button_action in pbutton:
            if user_action == pbutton[button_action]:
                return button_action
        return None


if __name__ == '__main__':
    import sys

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    print(Popup('atcrawl').error("You are not licensed to use this process"))
