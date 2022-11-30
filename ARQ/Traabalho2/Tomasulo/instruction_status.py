import sys

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import pyqtSlot as Slot
import os.path
import Arquivo as Aq

LD = "L.D"
SD = "S.D"
ADDD = "ADD.D"
SUBD = "SUB.D"
MULD = "MUL.D"
DIVD = "DIV.D"
BNE = "BNE.D"


class instruction_status:
    def __init__(self, inst, i):
        inst = inst.split()
        self.name = inst[0]
        self.issue = self.complete = self.write = self.rs = self.rt = self.rd = self.offset = -1
        self.index = i

        if self.name == LD or self.name == SD:
            self.offset = int(inst[-1].split("(")[0])

            self.rs = inst[-1].split("(")[-1].split(")")[0]

            self.rsIndex = int(self.rs.split('R')[-1])

            self.rt = inst[1]
            self.rtIndex = int(int(self.rt.split('F')[-1]) / 2)
        else:
            self.rd = inst[1]
            self.rdIndex = int(int(self.rd.split('F')[-1]) / 2)

            self.rs = inst[2]
            self.rsIndex = int(int(self.rs.split('F')[-1]) / 2)

            self.rt = inst[3]
            self.rtIndex = int(int(self.rt.split('F')[-1]) / 2)


def print(self):
    if self.issue == -1:
        issue = ""
    else:
        issue = self.issue
    if self.complete == -1:
        complete = ""
    else:
        complete = self.complete
    if self.write == -1:
        write = ""
    else:
        write = self.write

    if self.name == LD or self.name == SD:
        print("\t\t%s\t%s\t%s\t%s\t  %s\t    %s\t\t %s" %
              (self.name, self.rt, self.offset, self.rs, issue, complete, write))
    else:
        print("\t\t%s\t%s\t%s\t%s\t  %s\t    %s\t\t %s" %
              (self.name, self.rd, self.rs, self.rt, issue, complete, write))
