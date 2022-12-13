import sys

from PyQt5 import QtWidgets,QtCore,QtGui,uic
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QTableWidget
from PyQt5.QtCore import pyqtSlot as Slot
import os.path
import re
import pandas as pd
import Arquivo as Aq



import sys

LD = "L.D"   
SD = "S.D"   
ADDD = "ADD.D"
SUBD = "SUB.D"
MULD = "MUL.D" 
DIVD = "DIV.D" 
t=0
valor =0;


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

  def print(self,p):
    global valor 
    valor +=1
    if self.issue == -1: issue = "--"
    else: issue = "x"
    if self.complete == -1: complete = "--"                                                                                                                                                                                 
    else: complete = "x"
    if self.write == -1: write = "--"
    else: write = "x"

    if self.name == LD or self.name == SD:     
     
      p.ui.tableWidget_3.setItem(valor-1,1,QTableWidgetItem(self.name))
      p.ui.tableWidget_3.setItem(valor-1,2,QTableWidgetItem(str(issue)))
      p.ui.tableWidget_3.setItem(valor-1,3,QTableWidgetItem(str(complete)))
      p.ui.tableWidget_3.setItem(valor-1,4,QTableWidgetItem(str(write)))
      p.ui.tableWidget_3.setItem(valor-1,5,QTableWidgetItem(str(self.rt)))
      novoO="Mem["+str(self.offset)+" + Regs[x]]"
      p.ui.tableWidget_3.setItem(valor-1,6,QTableWidgetItem(novoO))
    elif self.name==MULD:
      p.ui.tableWidget_3.setItem(valor-1,1,QTableWidgetItem(self.name))
      p.ui.tableWidget_3.setItem(valor-1,2,QTableWidgetItem(str(issue)))
      p.ui.tableWidget_3.setItem(valor-1,3,QTableWidgetItem(str(complete)))
      p.ui.tableWidget_3.setItem(valor-1,4,QTableWidgetItem(str(write)))
      p.ui.tableWidget_3.setItem(valor-1,5,QTableWidgetItem(str(self.rd)))
      novoO="#2 X Regs["+str(self.rs)+"]"
      p.ui.tableWidget_3.setItem(valor-1,6,QTableWidgetItem(novoO))
    
    elif self.name==ADDD:
      p.ui.tableWidget_3.setItem(valor-1,1,QTableWidgetItem(self.name))
      p.ui.tableWidget_3.setItem(valor-1,2,QTableWidgetItem(str(issue)))
      p.ui.tableWidget_3.setItem(valor-1,3,QTableWidgetItem(str(complete)))
      p.ui.tableWidget_3.setItem(valor-1,4,QTableWidgetItem(str(write)))
      p.ui.tableWidget_3.setItem(valor-1,5,QTableWidgetItem(str(self.rd)))
      novoO="#2 + #1"
      p.ui.tableWidget_3.setItem(valor-1,6,QTableWidgetItem(novoO))
    
    elif self.name==SUBD:
      p.ui.tableWidget_3.setItem(valor-1,1,QTableWidgetItem(self.name))
      p.ui.tableWidget_3.setItem(valor-1,2,QTableWidgetItem(str(issue)))
      p.ui.tableWidget_3.setItem(valor-1,3,QTableWidgetItem(str(complete)))
      p.ui.tableWidget_3.setItem(valor-1,4,QTableWidgetItem(str(write)))
      p.ui.tableWidget_3.setItem(valor-1,5,QTableWidgetItem(str(self.rd)))
      novoO="#2 - #1"
      p.ui.tableWidget_3.setItem(valor-1,6,QTableWidgetItem(novoO))
    else:
      p.ui.tableWidget_3.setItem(valor-1,1,QTableWidgetItem(self.name))
      p.ui.tableWidget_3.setItem(valor-1,2,QTableWidgetItem(str(issue)))
      p.ui.tableWidget_3.setItem(valor-1,3,QTableWidgetItem(str(complete)))
      p.ui.tableWidget_3.setItem(valor-1,4,QTableWidgetItem(str(write)))
      p.ui.tableWidget_3.setItem(valor-1,5,QTableWidgetItem(str(self.rd)))

     