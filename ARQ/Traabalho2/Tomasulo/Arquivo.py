import sys
from os.path import exists


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot as Slot


class janelaInstrucao:

    def ColocarNaLista(instrucao, self):
        t=0;
        for i in instrucao:
            self.ui.tableWidget.setItem(t-1,1,QTableWidgetItem(i))
            t+=1    
        return 0        