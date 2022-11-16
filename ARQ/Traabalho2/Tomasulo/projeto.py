import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot as Slot

import Arquivo as Aq


LD = "L.D"   
SD = "S.D"   
ADDD = "ADD.D" 
SUBD = "SUB.D" 
MULD = "MUL.D" 
DIVD = "DIV.D" 



class Tomasulo:

    def __init__(self, insts, adder_num, multiplier_num, load_buffer_num, store_buffer_num, float_reg_num, int_reg_num, mem_size,p):
        i = 0
        t=0;
        for inst in insts:  
            p.ui.tableWidget.setItem(t-1,1,QTableWidgetItem(inst))
            t+=1
            inst_ = ""
            for term in inst.split(" "):
                inst_ = inst_ + term.split(",")[0] + " "
        insts[i] = inst_.split("\n")[0]
        i += 1    










   
     





def inicio(self):
    f = open("test2.txt", 'r')  
    insts = f.readlines()
    adder_num = 3
    multiplier_num = load_buffer_num = store_buffer_num = 2  
    float_reg_num = 16  # 16 floating-point register, from F0, F2, F4, …, to F30, 初始值為1； 
    int_reg_num = 32   # 32 integer register, from R0, R1, …, to R31
    mem_size = 64     # 64-byte memory(8 double-precision space)
    tomasulo = Tomasulo(insts, adder_num, multiplier_num, load_buffer_num, store_buffer_num, 
						float_reg_num, int_reg_num, mem_size,self)