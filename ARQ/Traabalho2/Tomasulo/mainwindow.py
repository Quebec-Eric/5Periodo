# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from window import Ui_MainWindow

def toSrintg():
        return "                     --------                -----------                                    ------                         --------------                           --------" 

def roderBuffer(self):
        self.ui.label.setText('1'+toSrintg())
        self.ui.label_4.setText('2'+toSrintg())
        self.ui.label_5.setText('3'+toSrintg())
        self.ui.label_6.setText('4'+toSrintg())
        self.ui.label_7.setText('5'+toSrintg())
        self.ui.label_8.setText('6'+toSrintg())
        self.ui.label_9.setText('7'+toSrintg())


def reservationStations(self):
    self.ui.label_14.setText('Load1'+toSrintg())
    self.ui.label_12.setText('Load2'+toSrintg())
    self.ui.label_11.setText('ADD1'+toSrintg())
    self.ui.label_13.setText('ADD2'+toSrintg())
    self.ui.label_24.setText('Mult1'+toSrintg())
    self.ui.label_25.setText('Mult2'+toSrintg())
    self.ui.label_26.setText('BNE'+toSrintg())


def fpRegisterStatus(self):
    self.ui.label_21.setText('Recoder'+toSrintg())
    self.ui.label_23.setText('Busy'+toSrintg())

class MainWindow(QMainWindow):

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tomasulo-Eric")
        roderBuffer(self)
        reservationStations(self)
        fpRegisterStatus(self)
      

   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
