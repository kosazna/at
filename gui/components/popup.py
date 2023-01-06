# -*- coding: utf-8 -*-
from typing import Union

from at.gui.components.atpyqt import QMessageBox

pbutton = {
    'ok': QMessageBox.StandardButton.Ok,
    'open': QMessageBox.StandardButton.Open,
    'save': QMessageBox.StandardButton.Save,
    'cancel': QMessageBox.StandardButton.Cancel,
    'close': QMessageBox.StandardButton.Close,
    'yes': QMessageBox.StandardButton.Yes,
    'no': QMessageBox.StandardButton.No,
    'abort': QMessageBox.StandardButton.Abort,
    'retry': QMessageBox.StandardButton.Retry,
    'ignore': QMessageBox.StandardButton.Ignore}

pstatus = {
    'info': QMessageBox.Icon.Information,
    'question': QMessageBox.Icon.Question,
    'warning': QMessageBox.Icon.Warning,
    'error': QMessageBox.Icon.Critical}


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
    appname: str = 'Dialog'

    @classmethod
    def set_appname(cls, appname: str):
        cls.appname = appname

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

    def error(self,
              primary: str = '',
              secondary: str = '',
              details: str = '',) -> Union[str, None]:
        msg = QMessageBox()
        msg.setWindowTitle(f"{self.appname}")
        msg.setIcon(pstatus['error'])
        msg.setText(primary)

        if primary:
            msg.setText(primary)
        if secondary:
            msg.setInformativeText(secondary)
        if details:
            msg.setDetailedText(details)

        msg.addButton(pbutton['close'])

        user_action = msg.exec_()
        msg.destroy()

        for button_action in pbutton:
            if user_action == pbutton[button_action]:
                return button_action
        return None
