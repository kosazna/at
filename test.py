import time
import tqdm
import pandas as pd
import atexit
import dtale

@atexit.register
def terminate():
    print('Finished')

# for x in tqdm.tqdm(range(0,20), "COPYING FILES", ncols=50, colour='blue', leave=True, bar_format="{l_bar}{bar}|"):  
#     b = "[" + "#" * x + ' ' * (100-x) + "]"
#     # print (b, end="/r")
#     time.sleep(0.1)
#     a = 10/0

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