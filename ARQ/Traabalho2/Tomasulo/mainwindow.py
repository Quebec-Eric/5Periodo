# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot as Slot

import projeto
import Arquivo


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from window import Ui_MainWindow

instrucoes=[]
clock =0
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
       
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit_5.setText("0")
        self.setWindowTitle("Tomasulo-Eric")
        self.ui.tableWidget.setColumnWidth(0,200)
        t=0
        for inst in range(7):  
            self.ui.tableWidget.setItem(t-1,1,QTableWidgetItem("---------------------"))
            
            instrucoes.append("------------------")    
            t+=1
           # eric=self.ui.tableWidget.item(t-1,1).read()
           # print(eric)
    @Slot()   
    def rodar(self):
        global clock
        if clock == 0:
            self.ui.textEdit_5.setText(clock)
            clock+=1
            projeto.inicio(self)
        return

    @Slot()
    def voltar(self):
        Arquivo.janelaInstrucao.ColocarNaLista(instrucoes,self)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())




