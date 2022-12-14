import sys

from PyQt5 import QtWidgets,QtCore,QtGui,uic
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QTableWidget
from PyQt5.QtCore import pyqtSlot as Slot
import os.path
import re
import pandas as pd
import Arquivo as Aq


class store_buffer:

  def __init__(self, i):
    self.index = i 
    self.name = "Store_" + str(i)
    self.time = -1
    self.busy = False
    self.vj = "null" 
    self.vk = "null" 
    self.qj = "null" 
    self.qk = "null" 
    self.address = 0
    self.result = 0
    self.inst_index = -1 
    self.vk_broadcasted_cycle = -1
    self.last_time_write = -1 
                   #

  def reset(self):    
    self.time = -1
    self.busy = False
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
    self.address = 0     
    self.vk_broadcasted_cycle = -1

  def print(self,p,valor):
    if self.busy == False: busy = "No"
    else: busy = "Yes"
    if self.qk == "null": qk = ""
    else: qk = self.qk.split("_")[0] + "_" + str(int(self.qk.split("_")[-1]) + 1)          
    name = self.name.split("_")[0] + "_" + str(int(self.name.split("_")[-1]) + 1)    
    p.ui.tableWidget_2.setItem(valor-1,0,QTableWidgetItem(name))
    p.ui.tableWidget_2.setItem(valor-1,1,QTableWidgetItem(busy))
    p.ui.tableWidget_2.setItem(valor-1,7,QTableWidgetItem(self.address))
    p.ui.tableWidget_2.setItem(valor-1,5,QTableWidgetItem(str(qk)))
 


class mem:  
  def __init__(self, i):
    self.name = "Mem_" + str(i)
    if i % 8 == 0: self.value = 1
    else: self.value = 0
