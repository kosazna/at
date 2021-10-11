# -*- coding: utf-8 -*-

import sys
import traceback
from typing import Callable, Union

from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot


class WorkerSignalsStr(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    - finished: No data
    - error:`tuple` (exctype, value, traceback.format_exc() )
    - result: `object` data returned from processing, anything
    - progress: `str` indicating progress metadata
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(str)
    popup = pyqtSignal(str)


class WorkerSignalsTuple(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    - finished: No data
    - error:`tuple` (exctype, value, traceback.format_exc() )
    - result: `object` data returned from processing, anything
    - progress: `tuple` indicating progress metadata
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    # (progress_bar_current_value, progress_bar_max_value, status)
    progress = pyqtSignal(tuple)
    # (appname, primary, secondary, details, status, buttons)
    popup = pyqtSignal(tuple)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''

    def __init__(self, fn, worker, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = worker()

        # Add the callback to our kwargs
        self.kwargs['_progress'] = self.signals.progress
        self.kwargs['_popup'] = self.signals.popup

    @pyqtSlot()
    def run(self):

        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done


def run_thread(threadpool: QThreadPool,
               process: Callable,
               on_update: Union[Callable, None] = None,
               on_finish: Union[Callable, None] = None,
               on_popup: Union[Callable, None] = None):
    worker = Worker(process, WorkerSignalsTuple)
    if on_update is not None:
        worker.signals.progress.connect(on_update)
    if on_finish is not None:
        worker.signals.finished.connect(on_finish)
    if on_popup is not None:
        worker.signals.popup.connect(on_popup)

    threadpool.start(worker)
