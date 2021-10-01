# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QRunnable, pyqtSlot, pyqtSignal
import traceback
import sys


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
    progress = pyqtSignal(tuple)
    popup = pyqtSignal(str)

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
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['progress_popup'] = self.signals.popup

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