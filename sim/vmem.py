#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
#
#   Classes for hardware components: RegisterFile, Register, and Memory. 
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================

from consts import *
from components import *

class VirtualMem(object):

    mem1      = Memory(0, 0, WORD_SIZE)
    mem2      = Memory(0, 0, WORD_SIZE)
    var_list = {}
    def mem1_init(self, mem_addr, mem_size, word_size):
        self.mem1 = Memory(mem_addr, mem_size, word_size)

    def mem2_init(self, mem_addr, mem_size, word_size):
        self.mem2 = Memory(mem_addr, mem_size, word_size)

    def access(self, valid, addr, data, fcn):
        
        res = self.mem1.access(valid, addr, data, fcn)
        if not res[1]:
            res = self.mem2.access(valid, addr, data, fcn)
        return res

    def var_get(self, var_num):
        if not var_num in self.var_list:
            self.var_list[var_num] = 0
        return self.var_list[var_num]

    def var_set(self, var_num, var_value):
        self.var_list[var_num] = var_value