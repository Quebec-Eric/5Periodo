import sys
class reservation_station:
  def __init__(self, adder_num, multiplier_num):
    self.adders = [adder(i) for i in range(adder_num)]
    self.multipliers = [multiplier(i) for i in range(multiplier_num)]
  
  def isFull(self, RS):
    for rs in RS:
      if rs.busy == False: return rs.index
    return "True"

  def print(self):
    print("-\n\nResevation Station:")
    print("\t\tTime\tName\tBusy\tOp\tVj\tVk\tQj\tQk")
    for adder in self.adders: self.print_RS(adder)
    for multiplier in self.multipliers: self.print_RS(multiplier)

  def print_RS(self, RS):
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
    print("\t\t%4s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (time, name, busy, op, vj, vk, qj, qk))
  
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
    self.inst_index = -1 # 紀錄該 reservation_station 處理的是哪一個 instruction
    self.vj_broadcasted_cycle = -1 # 為了不讓RS在broadcast的cycle就開始執行，因此必須在RS記錄得到broadcast的時間(cycle)
    self.vk_broadcasted_cycle = -1
    self.last_time_write = -1 # 為了禁止在write result之後的下個cycle解放station後，馬上被新的指令issue並放入該station中，
                   # 因此紀錄該 station 上個指令的 write result 時間，讓下個指令必須隔兩個cycle才能issue。
  
  def reset(self):    
    self.time = -1
    self.busy = False
    self.op = "null"
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
    #self.result = 0
    #self.inst_index = -1
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
    self.inst_index = -1 # 紀錄該 reservation_station 處理的是哪一個 instruction
    self.vj_broadcasted_cycle = -1 # 為了不讓RS在broadcast的cycle就開始執行，因此必須在RS記錄得到broadcast的時間(cycle)
    self.vk_broadcasted_cycle = -1
    self.last_time_write = -1 # 為了禁止在write result之後的下個cycle解放station後，馬上被新的指令issue並放入該station中，
                   # 因此紀錄該 station 上個指令的 write result 時間，讓下個指令必須隔兩個cycle才能issue。

  def reset(self):    
    self.time = -1
    self.busy = False
    self.op = "null"
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
    #self.result = 0
    #self.inst_index = -1
    self.vj_broadcasted_cycle = -1
    self.vk_broadcasted_cycle = -1

class load_buffer:
  def __init__(self, i):
    self.index = i  # index for register_result_status mapping
    self.name = "Load_" + str(i)
    self.time = -1
    self.busy = False
    self.vj = "null" # base address
    self.qj = "null" # the function unit which is processing base address
    self.address = 0 
    self.result = 0
    self.inst_index = -1 # 紀錄該 reservation_station 處理的是哪一個 instruction
    self.vj_broadcasted_cycle = -1  # 為了不讓RS在broadcast的cycle就開始執行，因此必須在RS記錄得到broadcast的時間(cycle)
    self.last_time_write = -1 # 為了禁止在write result之後的下個cycle解放station後，馬上被新的指令issue並放入該station中，
                   # 因此紀錄該 station 上個指令的 write result 時間，讓下個指令必須隔兩個cycle才能issue。

  def reset(self):    
    self.time = -1
    self.busy = False
    self.vj = "null"
    self.qj = "null"
    self.address = 0     
    #self.result = 0
    #self.inst_index = -1
    self.vj_broadcasted_cycle = -1 

  def print(self):
    if self.busy == False: busy = "No"
    else: busy = "Yes"
    if self.qj == "null": qj = ""
    else: qj = self.qj.split("_")[0] + "_" + str(int(self.qj.split("_")[-1]) + 1)          
    name = self.name.split("_")[0] + "_" + str(int(self.name.split("_")[-1]) + 1)
    print("\t\t%s\t%s\t%s\t\t%s" % (name, busy, self.address, qj))    

