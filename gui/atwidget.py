# -*- coding: utf-8 -*-

from typing import Any, Callable, Iterable, Optional

from at.auth import AuthStatus
from at.gui.components import Popup, Qt, QThreadPool, QWidget, pyqtSignal
from at.gui.worker import run_thread
from at.result import Result


class AtWidget(QWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.threadpool = QThreadPool(parent=self)
        self.popup = Popup()

        self.no_validate = []

    def updateProgress(self, metadata: dict):
        for update_item, update_value in metadata.items():
            if update_item.startswith('progress'):
                gui_object = getattr(self, update_item, None)
                if gui_object is not None:
                    gui_object.setValueMaximum(*update_value)
            elif update_item.startswith('status'):
                if isinstance(update_value, str):
                    status_text = update_value
                    status_name = 'statusNeutral'
                elif isinstance(update_value, (list, tuple)):
                    status_text = update_value[0]
                    status_name = update_value[1]
                else:
                    status_text = ''
                    status_name = 'statusNeutral'
                gui_object = getattr(self, update_item, None)
                if gui_object is not None:
                    gui_object.changeStatus(status_text, status_name)
            elif update_item.startswith('signal'):
                signal_object = getattr(self, update_item, None)
                if signal_object is not None:
                    signal_object.emit(update_value)
            else:
                gui_object = getattr(self, update_item, None)
                if gui_object is not None and hasattr(gui_object, 'setText'):
                    gui_object.setText(update_value)

    def updateResult(self, status: Any):
        if status is not None:
            if isinstance(status, AuthStatus):
                if not status.authorised:
                    self.popup.error(status.msg)
            elif isinstance(status, Result):
                if status.result == Result.ERROR:
                    self.popup.error(status.msg, **status.details)
                elif status.result == Result.WARNING:
                    self.popup.warning(status.msg, **status.details)
                else:
                    self.popup.info(status.msg, **status.details)

                if status.metadata is not None:
                    self.updateProgress(status.metadata)
            else:
                self.popup.info(status)

    def updateFinish(self):
        pass

    def runThread(self, function: Callable):
        run_thread(threadpool=self.threadpool,
                   function=function,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def getParams(self):
        return dict()

    def validateParams(self, needed: Optional[Iterable] = None):
        params = self.getParams()

        if params:
            bools = []
            validated = False

            for key, value in params.items():
                if key in self.no_validate:
                    continue

                if needed is not None:
                    if key in needed:
                        if value:
                            bools.append(True)
                        else:
                            bools.append(False)
                else:
                    if value:
                        bools.append(True)
                    else:
                        bools.append(False)

            validated = all(bools)

        return validated, params
