# -*- coding: utf-8 -*-

import sys
import traceback
from typing import Callable, Optional

from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot


class WorkerSignals(QObject):
    error = pyqtSignal(tuple)  # (exctype, value, traceback.format_exc())
    progress = pyqtSignal(dict)
    result = pyqtSignal(object)
    finished = pyqtSignal()


class Worker(QRunnable):
    def __init__(self, fn, worker, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = worker()

        self.kwargs['_progress'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


def run_thread(threadpool: QThreadPool,
               function: Callable,
               on_update: Optional[Callable] = None,
               on_result: Optional[Callable] = None,
               on_finish: Optional[Callable] = None):
    worker = Worker(function, WorkerSignals)

    if on_update is not None:
        worker.signals.progress.connect(on_update)
    if on_result is not None:
        worker.signals.result.connect(on_result)
    if on_finish is not None:
        worker.signals.finished.connect(on_finish)

    threadpool.start(worker)
