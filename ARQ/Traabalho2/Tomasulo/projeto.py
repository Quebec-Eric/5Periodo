import sys

from PyQt5 import QtWidgets,QtCore,QtGui,uic
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QTableWidget
from PyQt5.QtCore import pyqtSlot as Slot
import os.path
import Arquivo as Aq
import instruction_status as Estado
import reservation_station as Reservado
import load_buffer as load
import store_buffer as store
import register_result_status as Resister_status
import mem as memoria

LD = "L.D"   
SD = "S.D"   
ADDD = "ADD.D" 
SUBD = "SUB.D" 
MULD = "MUL.D" 
DIVD = "DIV.D" 
BNE="BNE.D"

class Tomasulo:

  def __init__(self, insts, adder_num, multiplier_num, load_buffer_num, store_buffer_num, float_reg_num, int_reg_num, mem_size,p):
    # 去除指令的逗號，並 initialize instruction status
    i = 0
    t=0;
    for inst in insts:  
      inst_ = ""
      p.ui.tableWidget.setItem(t-1,1,QTableWidgetItem(inst.lower()))
      t+=1
      for term in inst.split(" "):
        inst_ = inst_ + term.split(",")[0] + " "
      insts[i] = inst_.split("\n")[0]
      i += 1
    self.instruction_status = [Estado.instruction_status(insts[i], i) for i in range(len(insts))]
    self.reservation_station = Reservado.reservation_station(adder_num, multiplier_num)
    #print("aki")
    self.load_buffers = [load.load_buffer(i) for i in range(load_buffer_num)]
    self.store_buffers = [store.store_buffer(i) for i in range(store_buffer_num)]
    #print("aki")
    self.register_result_status = Resister_status.register_result_status(float_reg_num, int_reg_num)
    self.mem = [memoria.mem(i) for i in range(mem_size)]
    self.clock = 1
    print("aki")







   
     





def inicio(self):
  # read argument from command lind
  
  f = open("test2.txt", 'r')
  insts = f.readlines()   # read instructions from text file

  # read input from pwd
  #f = open("sample4.txt", 'r')
  #insts = f.readlines()   # read instructions from text file
  #f.close()

  adder_num = 3
  multiplier_num = load_buffer_num = store_buffer_num = 2  
  float_reg_num = 16  # 16 floating-point register, from F0, F2, F4, …, to F30, 初始值為1； 
  int_reg_num = 32   # 32 integer register, from R0, R1, …, to R31
  mem_size = 64     # 64-byte memory(8 double-precision space)
  tomasulo = Tomasulo(insts, adder_num, multiplier_num, load_buffer_num, store_buffer_num, 
						float_reg_num, int_reg_num, mem_size,self)
  