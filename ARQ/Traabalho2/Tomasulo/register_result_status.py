import sys



class register_result_status:
  def __init__(self, float_reg_num, int_reg_num):
    self.float_regs = [float_reg(i) for i in range(float_reg_num)] # 浮點數暫存器有16個，編號為F0、F2、F4、…、F30，初始值為1；
    self.int_regs = [int_reg(i) for i in range(int_reg_num)]    # 整數暫存器有32個，編號為R0、R1、…、R31
    self.int_regs[1].value = 16    

  def print(self):    
    print("Register result status:")
    a = ""
    for fr in self.float_regs: a += fr.name + "\t"
    print("\t\t\t" + a)

    a = ""
    for fr in self.float_regs: 
      if fr.qi == "null": qi = ""
      else: qi = fr.qi.split("_")[0] + "_" + str(int(fr.qi.split("_")[-1]) + 1)      
      a += str(qi) + "\t"
    print("\t\tQi:\t" + a)

    a = ""
    for fr in self.float_regs: a += str(fr.value) + "\t"
    print("\t\tvalue:\t" + a)
    print("\n")
    
    a = ""
    for ir in self.int_regs:  a += ir.name + "\t"
    print("\t\t\t" + a)

    a = ""
    for ir in self.int_regs:
      if ir.qi == "null": qi = ""
      else: qi = ir.qi.split("_")[0] + "_" + str(int(ir.qi.split("_")[-1]) + 1)
      a += str(qi) + "\t"
    print("\t\tQi:\t" + a)

    a = ""
    for ir in self.int_regs: a += str(ir.value) + "\t"
    print("\t\tvalue:\t" + a)
    print("-\n")    


class float_reg:
  def __init__(self, i):
    self.name = "F" + str(i * 2)
    self.value = 1
    self.qi = "null" # 正在等待的 function unit
  
  def print(self):
    print("reg %s, value: %d" % (self.name, self.value))


class int_reg:
  def __init__(self, i):
    self.name = "R" + str(i)
    self.value = 0
    self.qi = "null" # 正在等待的 function unit

  def print(self):
    print("reg %s, value: %d" % (self.name, self.value))
