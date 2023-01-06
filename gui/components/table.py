import sys
from typing import Optional

import pandas as pd

from at.gui.components.atpyqt import (QApplication, QDoubleValidator,
                                      QHeaderView, QItemDelegate, QLineEdit,
                                      QPushButton, Qt, QTableWidget,
                                      QTableWidgetItem, QVBoxLayout, QWidget,
                                      QFont)


def drawDataFrame(widget: QTableWidget, df: pd.DataFrame):
    nRows, nColumns = df.shape
    columns = ['_index_'] + list(map(str, df.columns))
    index = list(map(str, df.index))
    widget.setColumnCount(nColumns + 1)
    widget.setRowCount(nRows)
    widget.setHorizontalHeaderLabels(columns)
    widget.setVerticalHeaderLabels(list(map(str, index)))

    for i in range(nRows):
        for j in range(nColumns + 1):
            if j == 0:
                widget.setItem(i, j, QTableWidgetItem(str(df.index[i])))
            else:
                widget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j-1])))


class TableWidget(QTableWidget):
    def __init__(self,
                 df: pd.DataFrame,
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.df = df
        self.setupUi()

    def setupUi(self):
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSortIndicatorClearable(True)
        self.horizontalHeader().setSortIndicatorShown(True)

        drawDataFrame(self, self.df)

        self.cellChanged[int, int].connect(self.updateDataFrame)

    def updateDataFrame(self, row, column):
        idx = int(self.item(row, 0).text())
        text = self.item(row, column).text()
        self.df.iloc[idx, column - 1] = text


class DFEditor(QWidget):
    data = {
        'Col X': list('ABCD'),
        'col Y': [10, 20, 30, 40]
    }

    # df = pd.read_excel("D:/Terpos/RA_FINAL.xlsx")
    df = pd.DataFrame(data)

    def __init__(self):
        super().__init__()
        self.resize(1200, 800)

        mainLayout = QVBoxLayout()

        self.table = TableWidget(DFEditor.df)
        mainLayout.addWidget(self.table)

        button_print = QPushButton('Display DF')
        # button_print.setStyleSheet('font-size: 30px')
        button_print.clicked.connect(self.print_DF_Values)
        mainLayout.addWidget(button_print)

        button_export = QPushButton('Export to CSV file')
        # button_export.setStyleSheet('font-size: 30px')
        button_export.clicked.connect(self.export_to_csv)
        mainLayout.addWidget(button_export)

        self.setLayout(mainLayout)

    def print_DF_Values(self):
        print(self.table.df)

    def export_to_csv(self):
        self.table.df.to_csv('Data export.csv', index=False)
        print('CSV file exported.')


if __name__ == '__main__':
    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    demo = DFEditor()
    demo.show()

    sys.exit(app.exec())
