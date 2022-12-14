import sys

from PyQt5 import QtWidgets,QtCore,QtGui,uic
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QTableWidget
from PyQt5.QtCore import pyqtSlot as Slot
import os.path
import re
import pandas as pd
import Arquivo as Aq




class reservation_station:
  def __init__(self, adder_num, multiplier_num):
    self.adders = [adder(i) for i in range(adder_num)]
    self.multipliers = [multiplier(i) for i in range(multiplier_num)]
  
  def isFull(self, RS):
    for rs in RS:
      if rs.busy == False: return rs.index
    return "True"

  def print(self,p):
    global valor
   
    for adder in self.adders: 
      self.print_RS(adder,p,valor)
      valor+=1
    
    for multiplier in self.multipliers: 
      self.print_RS(multiplier,p,valor)
      valor+=1
  
  def print_RS(self, RS,p,valor):
    
    if RS.time == -1: time = ""
    else: time = RS.time
    if RS.busy == False: busy = "No"
    else: busy = "Yes"
    if RS.op == "null": op = ""
    else: op = RS.op
    if RS.vj == "null": vj = ""
    #prit("to aki")
    else: vj = RS.vj
    if RS.vk == "null": vk = ""
    else: vk = RS.vk
    if RS.qj == "null": qj = ""
    else: qj = qj = RS.qj.split("_")[0] + "_" + str(int(RS.qj.split("_")[-1]) + 1)      
    if RS.qk == "null": qk = ""
    else: qk = RS.qk.split("_")[0] + "_" + str(int(RS.qk.split("_")[-1]) + 1)
    name = RS.name.split("_")[0] + "_" + str(int(RS.name.split("_")[-1]) + 1)    
    p.ui.tableWidget_2.setItem(valor-1,0,QTableWidgetItem(name))
    p.ui.tableWidget_2.setItem(valor-1,1,QTableWidgetItem(busy))
    p.ui.tableWidget_3.setItem(valor-1,0,QTableWidgetItem(busy))
    p.ui.tableWidget_2.setItem(valor-1,2,QTableWidgetItem(str(op)))
    p.ui.tableWidget_2.setItem(valor-1,3,QTableWidgetItem(str(vj)))
    p.ui.tableWidget_2.setItem(valor-1,4,QTableWidgetItem(str(vk)))
    p.ui.tableWidget_2.setItem(valor-1,5,QTableWidgetItem(str(qj)))
    p.ui.tableWidget_2.setItem(valor-1,6,QTableWidgetItem(str(qk)))
    
  def adderIsFull(self, RS):
    for adder in self.adders:
      if adder.busy == False: return False
    return True

  def multiplierIsFull(self, RS):
    for multiplier in self.multipliers:
      if multiplier.busy == False: return False
    return True

class adder:
  def __init__(self, i):
    self.index = i
    self.name = "Add_" + str(i)
    self.time = -1
    self.busy = False
    self.op = "null"
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
    self.result = 0
    self.inst_index = -1 
    self.vj_broadcasted_cycle = -1
    self.vk_broadcasted_cycle = -1
    self.last_time_write = -1
  
  def reset(self):    
    self.time = -1
    self.busy = False
    self.op = "null"
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
  
    self.vj_broadcasted_cycle = -1
    self.vk_broadcasted_cycle = -1

class multiplier:
  def __init__(self, i):
    self.index = i
    self.name = "Mult_" + str(i)
    self.time = -1
    self.busy = False
    self.op = "null"
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
    self.result = 0
    self.inst_index = -1 
    self.vj_broadcasted_cycle = -1 
    self.vk_broadcasted_cycle = -1
    self.last_time_write = -1 

  def reset(self):    
    self.time = -1
    self.busy = False
    self.op = "null"
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
  
    self.vj_broadcasted_cycle = -1
    self.vk_broadcasted_cycle = -1

