# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import pyqtSlot as Slot


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("teste 1")
        print(self.text())

    @Slot()
    def botaoClicado(self):
        print("cheguei aq")