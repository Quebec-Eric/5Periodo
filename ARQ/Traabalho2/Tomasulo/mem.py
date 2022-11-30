import sys
class mem:  # 記憶體為8個雙精準(64-bit)的空間(64-Bytes)，初始值為1
  def __init__(self, i):
    self.name = "Mem_" + str(i)
    if i % 8 == 0: self.value = 1
    else: self.value = 0