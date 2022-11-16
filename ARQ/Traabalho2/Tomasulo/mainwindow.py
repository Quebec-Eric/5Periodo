# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot as Slot

import projeto


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from window import Ui_MainWindow


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tomasulo-Eric")
        
    
       

    @Slot()   
    def rodar(self):
        projeto.inicio(self)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())




