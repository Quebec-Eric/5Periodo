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
class Tomasulo:
  def __init__(self, janelaEntrada, adder_num, multiplier_num, load_buffer_num, store_buffer_num, float_reg_num, int_reg_num, mem_size,p):
    global valor
    global fazerTudo

    global t
    fazerTudo=p
    i = 0
    t=0;
    for inst in janelaEntrada:  
      inst_ = ""
      p.ui.tableWidget.setItem(t-1,1,QTableWidgetItem(inst.lower()))
      t+=1
      for term in inst.split(" "):
        inst_ = inst_ + term.split(",")[0] + " "
      janelaEntrada[i] = inst_.split("\n")[0]
      i += 1
    self.instruction_status = [instruction_status(janelaEntrada[i], i) for i in range(len(janelaEntrada))]
    valor =0
    self.reservation_station = reservation_station(adder_num, multiplier_num)

    self.load_buffers = [load_buffer(i) for i in range(load_buffer_num)]
    self.store_buffers = [store_buffer(i) for i in range(store_buffer_num)]
    
    self.register_result_status = register_result_status(float_reg_num, int_reg_num)
    self.mem = [mem(i) for i in range(mem_size)]
    self.clock = 1

  def lbIsFull(self): 
    for lb in self.load_buffers: 
      if lb.busy == False: return lb.index 
    return "True" 


  def sbIsFull(self):
    for sb in self.store_buffers: 
      if sb.busy == False: return sb.index 
    return "True" 
  
  def print(self,p):
    global valor 
    valor =0 
   
    p.ui.tableWidget_5.setItem(valor-1,1,QTableWidgetItem(str(self.clock)))
    valor =0 
    for IS in self.instruction_status: IS.print(p)   
    valor =0 
    self.reservation_station.print(p)
    for lb in self.load_buffers: 
      lb.print(p, valor)
      valor+=1
    for sb in self.store_buffers:
       sb.print(p, valor)
       valor+=1
    self.register_result_status.print(p)
 

  def isFinished(self):
    for IS in self.instruction_status:
      if IS.write == -1: return False
    return True

  def writeResult(self):
    for RS in self.reservation_station.adders:            
      self.broadcast(RS)

    for RS in self.reservation_station.multipliers:      
      self.broadcast(RS)

    for RS in self.load_buffers:
      self.broadcast(RS)
    
    for RS in self.store_buffers:      
      if RS.busy == True and RS.time == 0:                
        if RS.qk != "null":                    
          if RS.qk.split("_")[0] == "Add": fus = self.reservation_station.adders
          elif RS.qk.split("_")[0] == "Mult": fus = self.reservation_station.multipliers
          for fu in fus: 
            if RS.qk == fu.name and self.clock == self.instruction_status[fu.inst_index].write + 1: 
              self.mem[RS.address].value = fu.result
              RS.last_time_write = self.clock 
              self.instruction_status[RS.inst_index].write = self.clock          
              fu.result = -1 
              RS.reset()              
                               
       
        elif RS.qk == "null": 
          self.mem[RS.address].value = RS.vk
          self.vk_broadcasted_cycle = self.clock
          RS.last_time_write = self.clock 
          self.instruction_status[RS.inst_index].write = self.clock          
          RS.reset()          

  def broadcast(self, RS):
    if RS.busy == True and RS.time == 0:
      RS.last_time_write = self.clock
      self.instruction_status[RS.inst_index].write = self.clock 

     
      for reg in self.register_result_status.float_regs:
        if reg.qi != "null" and reg.qi == RS.name:            
          reg.value = RS.result
          reg.qi = "null"

      for RSs in self.reservation_station.adders: 
        if RSs.busy == True and RSs.qj == RS.name:
          RSs.vj = RS.result
          RSs.vj_broadcasted_cycle = self.clock
          RSs.qj = "null"
        if RSs.busy == True and RSs.qk == RS.name:
          RSs.vk = RS.result
          RSs.vk_broadcasted_cycle = self.clock
          RSs.qk = "null"

      for RSs in self.reservation_station.multipliers:
        if RSs.busy == True and RSs.qj == RS.name:
          RSs.vj = RS.result
          RSs.vj_broadcasted_cycle = self.clock
          RSs.qj = "null"
        if RSs.busy == True and RSs.qk == RS.name:
          RSs.vk = RS.result
          RSs.vk_broadcasted_cycle = self.clock
          RSs.qk = "null"

      for RSs in self.load_buffers: 
        if RSs.busy == True and RSs.qj == RS.name:
          RSs.vj = RS.result
          RSs.vj_broadcasted_cycle = self.clock
          RSs.qj = "null"          

   
      RS.reset()
      
  def execute(self):
    for RS in self.reservation_station.adders:      
      if RS.busy == True and RS.vj != "null" and RS.vk != "null" and RS.qj == "null" and RS.qk == "null":
        if RS.vj_broadcasted_cycle == self.clock or RS.vk_broadcasted_cycle == self.clock: continue 
        else:
          RS.time = RS.time - 1        
          if RS.time == 0:
            if RS.op == ADDD: RS.result = RS.vj + RS.vk
            elif RS.op == SUBD: RS.result = RS.vj - RS.vk          
            self.instruction_status[RS.inst_index].complete = self.clock

    for RS in self.reservation_station.multipliers: 
      if RS.busy == True and RS.vj != "null" and RS.vk != "null" and RS.qj == "null" and RS.qk == "null":        
        if RS.vj_broadcasted_cycle == self.clock or RS.vk_broadcasted_cycle == self.clock: continue 
        else:
          RS.time = RS.time - 1
          if RS.time == 0:
            if RS.op == MULD: RS.result = RS.vj * RS.vk
            elif RS.op == DIVD: RS.result = RS.vj / RS.vk
            self.instruction_status[RS.inst_index].complete = self.clock

    for RS in self.load_buffers:
      if RS.busy == True and RS.vj != "null" and RS.qj == "null": 
       
        if RS.vj_broadcasted_cycle == self.clock: continue 
        else:
          RS.time = RS.time - 1
          if RS.time == 1:
            RS.address = RS.address + RS.vj
          elif RS.time == 0:
            RS.result = self.mem[RS.address].value
            self.instruction_status[RS.inst_index].complete = self.clock

    for RS in self.store_buffers:      
    
      if RS.busy == True:
      
        if RS.time != 0: 
          RS.time = RS.time - 1
          if RS.time == 0:
            RS.address = RS.address + RS.vj
            self.instruction_status[RS.inst_index].complete = self.clock
  
  def issue(self):
    for inst in self.instruction_status:      
      if inst.issue == -1: 
        if inst.name == LD:
          index = self.lbIsFull() 
          if index != "True" and self.load_buffers[index].last_time_write != self.clock:
            self.load_buffers[index].time = 2
            inst.issue = self.clock
            self.load_buffers[index].inst_index = inst.index 
            # load or store
            if self.register_result_status.int_regs[inst.rsIndex].qi != "null": 
              self.load_buffers[index].qj = self.register_result_status.int_regs[inst.rsIndex].qi
            else:              
              self.load_buffers[index].vj = self.register_result_status.int_regs[inst.rsIndex].value 
              self.load_buffers[index].qj = "null"
            self.load_buffers[index].address = inst.offset 
            self.load_buffers[index].busy = True

         
            self.register_result_status.float_regs[inst.rtIndex].qi = self.load_buffers[index].name 

        elif inst.name == SD:
          index = self.sbIsFull() 
          if index != "True" and self.store_buffers[index].last_time_write != self.clock:
            inst.issue = self.clock
            self.store_buffers[index].time = 1
            self.store_buffers[index].inst_index = inst.index            
           
            if self.register_result_status.int_regs[inst.rsIndex].qi != "null": 
              self.store_buffers[index].qj = self.register_result_status.int_regs[inst.rsIndex].qi              
            else:
              self.store_buffers[index].vj = self.register_result_status.int_regs[inst.rsIndex].value
              self.store_buffers[index].qj = "null"              
            self.store_buffers[index].address = inst.offset 
            self.store_buffers[index].busy = True

            
            if self.register_result_status.float_regs[inst.rtIndex].qi != "null":             
              self.store_buffers[index].qk = self.register_result_status.float_regs[inst.rtIndex].qi              
            else:
              self.store_buffers[index].vk = self.register_result_status.float_regs[inst.rtIndex].value             
              self.store_buffers[index].qk = "null"
            
        elif inst.name == ADDD or inst.name == SUBD or inst.name == MULD or inst.name == DIVD:        
          if inst.name == ADDD or inst.name == SUBD:             
            index = self.reservation_station.isFull(self.reservation_station.adders)
           
            if index != "True" and self.reservation_station.adders[index].last_time_write != self.clock:
              inst.issue = self.clock
              self.reservation_station.adders[index].inst_index = inst.index 
              if inst.name == ADDD: self.reservation_station.adders[index].op = ADDD
              elif inst.name == SUBD: self.reservation_station.adders[index].op = SUBD              
              self.reservation_station.adders[index].time = 2
              if self.register_result_status.float_regs[inst.rsIndex].qi != "null":
                self.reservation_station.adders[index].qj = self.register_result_status.float_regs[inst.rsIndex].qi
              else:            
              
                self.reservation_station.adders[index].vj = self.register_result_status.float_regs[inst.rsIndex].value 
                self.reservation_station.adders[index].qj = "null"

              if self.register_result_status.float_regs[inst.rtIndex].qi != "null":
                self.reservation_station.adders[index].qk = self.register_result_status.float_regs[inst.rtIndex].qi                
              else:
           
                self.reservation_station.adders[index].vk = self.register_result_status.float_regs[inst.rtIndex].value 
                self.reservation_station.adders[index].qk = "null"
              self.reservation_station.adders[index].busy = True
              self.register_result_status.float_regs[inst.rdIndex].qi = self.reservation_station.adders[index].name      

          elif inst.name == MULD or inst.name == DIVD: 
            index = self.reservation_station.isFull(self.reservation_station.multipliers)
           
            if index != "True" and self.reservation_station.multipliers[index].last_time_write != self.clock:
              inst.issue = self.clock
              self.reservation_station.multipliers[index].inst_index = inst.index 
              if inst.name == MULD:
                self.reservation_station.multipliers[index].time = 10
                self.reservation_station.multipliers[index].op = MULD
              elif inst.name == DIVD: 
                self.reservation_station.multipliers[index].time = 40
                self.reservation_station.multipliers[index].op = DIVD

              if self.register_result_status.float_regs[inst.rsIndex].qi != "null":
                self.reservation_station.multipliers[index].qj = self.register_result_status.float_regs[inst.rsIndex].qi
              else:
          
                self.reservation_station.multipliers[index].vj = self.register_result_status.float_regs[inst.rsIndex].value 
                self.reservation_station.multipliers[index].qj = "null"

              if self.register_result_status.float_regs[inst.rtIndex].qi != "null":
                self.reservation_station.multipliers[index].qk = self.register_result_status.float_regs[inst.rtIndex].qi                
              else:
                              
                self.reservation_station.multipliers[index].vk = self.register_result_status.float_regs[inst.rtIndex].value 
                self.reservation_station.multipliers[index].qk = "null"
              self.reservation_station.multipliers[index].busy = True
              self.register_result_status.float_regs[inst.rdIndex].qi = self.reservation_station.multipliers[index].name   
              
        break 


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

class load_buffer:
  def __init__(self, i):
    self.index = i 
    self.name = "Load_" + str(i)
    self.time = -1
    self.busy = False
    self.vj = "null" 
    self.qj = "null" 
    self.address = 0 
    self.result = 0
    self.inst_index = -1 
    self.vj_broadcasted_cycle = -1  
    self.last_time_write = -1 
               

  def reset(self):    
    self.time = -1
    self.busy = False
    self.vj = "null"
    self.qj = "null"
    self.address = 0     
 
    self.vj_broadcasted_cycle = -1 

  def print(self,p,valor):
    if self.busy == False: busy = "No"
    else: busy = "Yes"
    if self.qj == "null": qj = ""
    else: qj = self.qj.split("_")[0] + "_" + str(int(self.qj.split("_")[-1]) + 1)          
    name = self.name.split("_")[0] + "_" + str(int(self.name.split("_")[-1]) + 1)   
    p.ui.tableWidget_2.setItem(valor-1,0,QTableWidgetItem(name))
    p.ui.tableWidget_2.setItem(valor-1,1,QTableWidgetItem(busy))
    p.ui.tableWidget_3.setItem(valor-1,0,QTableWidgetItem(busy))
    p.ui.tableWidget_2.setItem(valor-1,7,QTableWidgetItem(self.address))
    p.ui.tableWidget_2.setItem(valor-1,5,QTableWidgetItem(str(qj)))

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

class register_result_status:
  def __init__(self, float_reg_num, int_reg_num):
    
    self.float_regs = [float_reg(i) for i in range(float_reg_num)] 
    self.int_regs = [int_reg(i) for i in range(int_reg_num)]    
    self.int_regs[1].value = 16    

  def print(self,p):   
    global valor
    valor=1 
    
    p.ui.tableWidget_4.setItem(1,0,QTableWidgetItem("Busy"))
    a = ""
    for fr in self.float_regs: a += fr.name + "\t"
    

    a = ""
    p.ui.tableWidget_4.setItem(1,1,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,2,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,3,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,4,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,5,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,6,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,7,QTableWidgetItem("No"))
    p.ui.tableWidget_4.setItem(1,8,QTableWidgetItem("No"))
    for fr in self.float_regs: 
      if fr.qi == "null":
         qi = ""
         saber="No"
      else: 
        qi = fr.qi.split("_")[0] + "_" + str(int(fr.qi.split("_")[-1]) + 1)      
        saber="Yes"
     
      p.ui.tableWidget_4.setItem(0,valor,QTableWidgetItem(str(qi)))
      #p.ui.tableWidget_4.setItem(1,valor,QTableWidgetItem(saber))
      valor+=1
    
    valor =1
    a = ""
    for fr in self.float_regs:
       a += str(fr.value) + "\t"
       #p.ui.tableWidget_4.setItem(1,valor,QTableWidgetItem(saber))
       valor+=1
    
    
  
    

class float_reg:
  def __init__(self, i):
    self.name = "F" + str(i * 2)
    self.value = 1
    self.qi = "null" 

class int_reg:
  def __init__(self, i):
    self.name = "R" + str(i)
    self.value = 0
    self.qi = "null" 





def PassarClock(self):

  global tomasulo
  tomasulo.writeResult()  
  tomasulo.execute()   
  tomasulo.issue()     
  tomasulo.print(self)   
  tomasulo.clock += 1 
  if tomasulo.isFinished(): escreverFim(self)
  return 0


def escreverFim(p):
  global t
  for i in range(t):
    p.ui.tableWidget_2.setItem(i-1,0,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,1,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,2,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,3,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,4,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,5,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,6,QTableWidgetItem("---------"))
    p.ui.tableWidget_2.setItem(i-1,7,QTableWidgetItem("---------"))
  
    for i in range(t):
      p.ui.tableWidget_3.setItem(i-1,0,QTableWidgetItem("---------"))
      p.ui.tableWidget_3.setItem(i-1,1,QTableWidgetItem("---------"))
      p.ui.tableWidget_3.setItem(i-1,2,QTableWidgetItem("---------"))
      p.ui.tableWidget_3.setItem(i-1,3,QTableWidgetItem("---------"))
      p.ui.tableWidget_3.setItem(i-1,4,QTableWidgetItem("---------"))
      p.ui.tableWidget_3.setItem(i-1,5,QTableWidgetItem("---------"))
      p.ui.tableWidget_3.setItem(i-1,6,QTableWidgetItem("---------"))

    for i in range(t):
       p.ui.tableWidget.setItem(i-1,0,QTableWidgetItem("---------"))
    
    for i in range(9):
       p.ui.tableWidget_4.setItem(0,i,QTableWidgetItem("---------"))
       p.ui.tableWidget_4.setItem(1,i,QTableWidgetItem("---------"))
      
     
def existe(palava):
  
  return 1

def inicio(self):
  
  global tomasulo
  
  f = open('test2.txt', 'r')
  insts = f.readlines()
  adder_num = 3
  multiplier_num = load_buffer_num = store_buffer_num = 2  
  float_reg_num = 16  
  int_reg_num = 32  
  mem_size = 64     
  tomasulo = Tomasulo(insts, adder_num, multiplier_num, load_buffer_num, store_buffer_num, 
			float_reg_num, int_reg_num, mem_size,self)
      
  

















