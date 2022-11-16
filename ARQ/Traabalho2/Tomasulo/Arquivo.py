import sys
from os.path import exists



def save_log_window_file(self):
    if  exists("LogJanelaTomasulo.txt"):
        self.ui.tableWidget.item(1,1).text()
