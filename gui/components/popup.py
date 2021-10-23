# -*- coding: utf-8 -*-
from typing import Union

from PyQt5.QtWidgets import QMessageBox

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
               buttons: Union[str, list, tuple, None] = None) -> Union[str, None]:
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
        if isinstance(buttons, str):
            buttons = [buttons]
        for button in buttons:
            if button in pbutton:
                msg.addButton(pbutton[button])
    else:
        msg.addButton(pbutton['close'])

    user_action = msg.exec_()
    msg.destroy()

    for button_action in pbutton:
        if user_action == pbutton[button_action]:
            return button_action
    return None


class Popup:
    def __init__(self, appname: str = 'Dialog') -> None:
        self.appname = appname

    def info(self,
             primary: str = '',
             secondary: str = '',
             details: str = '',
             buttons: Union[str, list, tuple, None] = None) -> Union[str, None]:
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
            if isinstance(buttons, str):
                buttons = [buttons]
            for button in buttons:
                if button in pbutton:
                    msg.addButton(pbutton[button])
        else:
            msg.addButton(pbutton['close'])

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
                buttons: Union[str, list, tuple, None] = None) -> Union[str, None]:
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
            if isinstance(buttons, str):
                buttons = [buttons]
            for button in buttons:
                if button in pbutton:
                    msg.addButton(pbutton[button])
        else:
            msg.addButton(pbutton['close'])

        user_action = msg.exec_()
        msg.destroy()

        for button_action in pbutton:
            if user_action == pbutton[button_action]:
                return button_action
        return None

    def error(self, primary: str = '') -> Union[str, None]:
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
