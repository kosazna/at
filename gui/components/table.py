# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from typing import Optional
from pathlib import Path

import pandas as pd

from at.gui.components.atpyqt import (QApplication, QDoubleValidator, QFont,
                                      QHeaderView, QItemDelegate, QLineEdit,
                                      QPushButton, Qt, QTableWidget,
                                      QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget)
from at.gui.components.combo import ComboInput
from at.gui.components.progress import ProgressBar
from at.gui.components.status import StatusLabel
from at.gui.components.button import Button
from at.gui.utils import set_size

cssGuide = Path("D:/.temp/.dev/.aztool/at/gui/css/_style.css").read_text()


def drawDataFrame(widget: TableWidget):
    nRows, nColumns = widget.df.shape
    widget.columns = {idx: col_name for idx, col_name in
                      enumerate(['_index_'] + list(map(str, widget.df.columns)))}
    widget.index = list(map(str, widget.df.index))
    widget.setColumnCount(nColumns + 1)
    widget.setRowCount(nRows)
    widget.setHorizontalHeaderLabels(widget.columns.values())
    widget.setVerticalHeaderLabels(list(map(str, widget.index)))

    for i in range(nRows):
        for j in range(nColumns + 1):
            if j == 0:
                widget.setItem(i, j, QTableWidgetItem(str(widget.df.index[i])))
            else:
                widget.setItem(i, j, QTableWidgetItem(
                    str(widget.df.iloc[i, j-1])))


def shift(val, by: int = 1):
    return str(val+by)


def drawTable(widget: TableWidget):
    columns = widget.config['columns']
    obj = widget.config['object']
    ui = widget.config['ui']
    defaults = widget.config['defaults']

    nRows = len(widget.data)
    nColumns = len(columns)
    widget.columns = {idx: col_name for idx, col_name in enumerate(columns)}
    widget.index = list(range(nRows))
    widget.setColumnCount(nColumns)
    widget.setRowCount(nRows)
    widget.setHorizontalHeaderLabels(widget.columns.values())
    widget.setVerticalHeaderLabels(list(map(shift, widget.index)))

    for col in columns:
        col_idx = widget.getColIdx(col)
        _item = obj.get(col, QTableWidgetItem)
        if _item.__name__ == QTableWidgetItem.__name__:
            default = defaults.get(col, '')
            for i in range(nRows):
                if widget.data is not None:
                    try:
                        item_data = widget.data[i].get(col, default)
                    except IndexError:
                        item_data = default
                else:
                    item_data = default
                widget.setItem(i, col_idx, QTableWidgetItem(item_data))
        else:
            default = defaults.get(col, '')
            for i in range(nRows):
                item = obj[col](**ui.get(col, {}))
                if widget.data is not None:
                    try:
                        item_data = widget.data[i].get(col, default)
                    except IndexError:
                        item_data = default
                else:
                    item_data = default
                widget.setCellWidget(i, col_idx, item)
                if isinstance(item, ComboInput):
                    widget.cellWidget(i, col_idx).setCurrentText(item_data)
                elif isinstance(item, StatusLabel):
                    widget.cellWidget(i, col_idx).changeStatus(*item_data)


table_config = {
    "type": "custom",
    "columns": ["jobID", "parser", "status", "records", "URL"],
    "object": {
        "parser": ComboInput,
        "status": StatusLabel},
    "ui": {
        "parser": {"items": ["rellas", "skroutz", "kokkinoplitis"],
                   "combosize": (100, 24)}},
    "defaults": {
        "parser": 'skroutz',
        "status": ('', 'statusNeutral')}
}

table_data = [
    {
        "jobID": '',
        "parser": 'rellas',
        "URL": '',
        "status": ('OK', 'statusOk')
    },
    {
        "jobID": '',
        "URL": ''
    }
]


class TableWidget(QTableWidget):
    def __init__(self,
                 config: dict,
                 data: Optional[list[dict]] = None,
                 df: Optional[pd.DataFrame] = None,
                 sorting: bool = True,
                 parent: Optional[QWidget] = None,
                 size:tuple[int] = (400,300),
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.config = config
        self.data = data
        self.df = df
        self.columns: Optional[dict[int, str]] = None
        self.index: list = []
        self.initUi(sorting, size)

    def setupUi(self, sorting, size):
        set_size(widget=self, size=size)
        self.setStyleSheet(cssGuide)  # TODO delete this
        self.setSortingEnabled(sorting)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        if sorting:
            self.setAlternatingRowColors(True)
            self.horizontalHeader().setSortIndicatorClearable(True)
            self.horizontalHeader().setSortIndicatorShown(True)

    def initUi(self, sorting, size):
        self.setupUi(sorting, size)
        if self.config['type'] == 'pandas':
            drawDataFrame(self)
            self.cellChanged[int, int].connect(self.updateDataFrame)
        else:
            drawTable(self)

    def getColIdx(self, col_name: str) -> int:
        for k, v in self.columns.items():
            if col_name == v:
                return k
        raise ValueError(f"{col_name} not in columns")

    def updateDataFrame(self, row, column):
        idx = int(self.item(row, 0).text())
        text = self.item(row, column).text()
        self.df.iloc[idx, column - 1] = text


class Table(QWidget):
    def __init__(self,
                 config: dict,
                 data: Optional[list[dict]] = None,
                 df: Optional[pd.DataFrame] = None,
                 sorting: bool = True,
                 widgetsize :tuple[int] = (600, None),
                 tablesize:tuple[int] = (None, 400),
                 buttonsize: tuple[int] = (60,24),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.table: Optional[TableWidget] = None
        self.initUi(config, data, df, sorting, widgetsize, tablesize, buttonsize)

    def setupUi(self, config, data, df, sorting, widgetsize, tablesize, buttonsize):
        set_size(widget=self, size=widgetsize)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(4)
        

        self.table = TableWidget(config=config,
                                 data=data,
                                 df=df,
                                 size=tablesize,
                                 sorting=sorting,
                                 parent=self)

        self.addRowButton = Button(label='Add',
                                   color='blue',
                                   size=buttonsize,
                                   parent=self)

        buttonLayout.addWidget(
            self.addRowButton, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def initUi(self, config, data, df, sorting, widgetsize, tablesize, buttonsize):
        self.setupUi(config, data, df, sorting, widgetsize, tablesize, buttonsize)


if __name__ == '__main__':
    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    demo = Table(config=table_config,
                 data=table_data,
                 widgetsize=(800, None),
                 sorting=False)
    demo.show()

    sys.exit(app.exec())
