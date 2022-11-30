import sys
class store_buffer:
  # mem[rs + immd.(offset)] = rt
  def __init__(self, i):
    self.index = i  # index for register_result_status mapping    
    self.name = "Store_" + str(i)
    self.time = -1
    self.busy = False
    self.vj = "null" # base address register(rs)
    self.vk = "null" # source register (rt)
    self.qj = "null" 
    self.qk = "null" # the function unit which is processing base address
    self.address = 0
    self.result = 0
    self.inst_index = -1 # 紀錄該 reservation_station 處理的是哪一個 instruction
    self.vk_broadcasted_cycle = -1 # 為了不讓RS在broadcast的cycle就開始執行，因此必須在RS記錄得到broadcast的時間(cycle)
    self.last_time_write = -1 # 為了禁止在write result之後的下個cycle解放station後，馬上被新的指令issue並放入該station中，
                   # 因此紀錄該 station 上個指令的 write result 時間，讓下個指令必須隔兩個cycle才能issue。    

  def reset(self):    
    self.time = -1
    self.busy = False
    self.vj = "null"
    self.vk = "null"
    self.qj = "null"
    self.qk = "null"
    self.address = 0     
    #self.result = 0
    #self.inst_index = -1
    self.vk_broadcasted_cycle = -1

  def print(self):
    if self.busy == False: busy = "No"
    else: busy = "Yes"
    if self.qk == "null": qk = ""
    else: qk = self.qk.split("_")[0] + "_" + str(int(self.qk.split("_")[-1]) + 1)          
    name = self.name.split("_")[0] + "_" + str(int(self.name.split("_")[-1]) + 1)    
    print("\t\t%s\t%s\t%s\t\t%s" % (name, busy, self.address, qk))    