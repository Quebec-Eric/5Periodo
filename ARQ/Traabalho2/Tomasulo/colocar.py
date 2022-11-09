import sys

from PyQt5.QtWidgets import QApplication, QMainWindow



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


def salvarArquivo(self):
    arquivo = open('logOperacoes.txt', 'w')
    #Roder buffer
    arquivo.write("Roder Buffer\n")
    arquivo.write(self.ui.label.text()+"\n")
    arquivo.write(self.ui.label_4.text()+"\n")
    arquivo.write(self.ui.label_5.text()+"\n")
    arquivo.write(self.ui.label_6.text()+"\n")
    arquivo.write(self.ui.label_7.text()+"\n")
    arquivo.write(self.ui.label_8.text()+"\n")
    arquivo.write(self.ui.label_9.text()+"\n")
    #Reservation stations
    arquivo.write("Reservation Stations\n")
    arquivo.write(self.ui.label_14.text()+"\n")
    arquivo.write(self.ui.label_12.text()+"\n")
    arquivo.write(self.ui.label_11.text()+"\n")
    arquivo.write(self.ui.label_13.text()+"\n")
    arquivo.write(self.ui.label_24.text()+"\n")
    arquivo.write(self.ui.label_25.text()+"\n")
    arquivo.write(self.ui.label_26.text()+"\n")
    #Fp Register Status
    arquivo.write("Fp Regisster Status\n")
    arquivo.write(self.ui.label_21.text()+"\n")
    arquivo.write(self.ui.label_23.text()+"\n")
    arquivo.close()


def lerLOG(self):
    arquivo = open('logOperacoes.txt', 'r')
    linhas=arquivo.readline()
    #self.ui.label_21.setText(linhas )
    return 0



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
    