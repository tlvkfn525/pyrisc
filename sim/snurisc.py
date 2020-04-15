#!/usr/bin/python3

#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
#
#   The main program for the RISC-V ISA simulator.
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================

import sys
import os

from consts import *
from isa import *
from components import *
from program import *
from sim import *
from privReg import *
from vmem import *

#--------------------------------------------------------------------------
#   SNURISC: Target machine to simulate
#--------------------------------------------------------------------------

class SNURISC(object):


    def __init__(self, filename):

        self.filename       = filename
        self.pc             = Register()
        self.regs           = RegisterFile()
        self.imem           = Memory(IMEM_START, IMEM_SIZE, WORD_SIZE)
        self.dmem           = Memory(DMEM_START, DMEM_SIZE, WORD_SIZE)
        self.prv_regs       = PrivReg()
        self.prv            = PRV_M
        self.vmem           = VirtualMem()
        self.rstvec         = Memory(DEFAULT_RSTVEC, 0x1000, WORD_SIZE)
        self.set_rstvec()
        self.stat_info      = os.stat("./pk")
        self.heap_start     = HEAP_START
 
    def run(self, entry_point):
        Sim.run(self, entry_point)

    def set_rstvec(self):
        self.rstvec.access(True, DEFAULT_RSTVEC, 0x297, M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + WORD_SIZE, 0x28593 + (RESET_VEC_SIZE << 20), M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + 2 * WORD_SIZE, 0xf1402573, M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + 3 * WORD_SIZE, 0x0182a283, M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + 4 * WORD_SIZE, 0x28067, M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + 5 * WORD_SIZE, 0, M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + 6 * WORD_SIZE, IMEM_START, M_XWR)
        self.rstvec.access(True, DEFAULT_RSTVEC + 7 * WORD_SIZE, 0, M_XWR)
        
        try:
            dtb_file = open('devicetree.dtb', 'rb')

            for i in range(8, 0x400 // WORD_SIZE):
                b = dtb_file.read(1)
                s = int(ord(b))
                b = dtb_file.read(1)
                s = int(ord(b)) * 256 + s
                b = dtb_file.read(1)
                s = int(ord(b)) * 256 * 256 + s
                b = dtb_file.read(1)
                s = int(ord(b)) * 256 * 256 * 256 + s
                self.rstvec.access(True, DEFAULT_RSTVEC + i * WORD_SIZE, s, M_XWR)
            dtb_file.close()

        except IOError:
            print("File open Error: Check devicetree.dtb file")
        
        return
    
    var_num = -1
    def handle_syscall(self):
        a0                  = self.regs.read(10)
        a1                  = self.regs.read(11)
        a2                  = self.regs.read(12)
        a3                  = self.regs.read(13)
        a4                  = self.regs.read(14)
        a5                  = self.regs.read(15)
        a6                  = self.regs.read(16)
        n                   = self.regs.read(17)

        if n in sysconst_list:
            if n == 80:                                 # sys_fstat
                self.stat_info = os.stat(self.filename)
                return EXC_NONE
            elif n == 214:                              # sys_brk
                # var_num     = a6
                # if a0 == 0:
                #     self.vmem.var_set(var_num, self.heap_start)
                # elif var_num in self.vmem.var_list and self.vmem.var_get(var_num) == a0:
                #     self.regs.write(10, self.heap_start)
                #     self.regs.write(16, a6 - HEAP_SIZE)
                # else:
                #     self.vmem.var_set(var_num, self.heap_start)
                #     heap            = Memory(self.heap_start, HEAP_SIZE, WORD_SIZE)
                #     self.vmem.heap_list.append(heap)
                #     print('heap created:')
                #     print(hex(self.heap_start), hex(HEAP_SIZE + self.heap_start))
                #     self.heap_start = self.heap_start + var_num - HEAP_SIZE
                
                #value       = self.vmem.var_get(var_num)
                #self.regs.write(15, value)
                
                var_num     = a6
                value       = self.vmem.var_get(var_num)
                self.regs.write(15, value)
                if a0 != 0:
                    self.regs.write(10, self.heap_start)
                return EXC_NONE
            elif n == 64:                               # sys_write
                remainder   = a1 % 4
                address     = a1 - remainder
                i           = 0
                string      = ''
                while i < a2:
                    data    = self.vmem.access(True, address + i, 0, M_XRD)[0]
                    if i == 0:
                        data >>= (remainder * 8)
                    if data == 0xff:
                        data = self.vmem.access(True, 0x1333c, 0, M_XRD)[0]
                        data >>= (3 * 8)
                    while (data % 0x100 != 0):
                        letter = chr(data % 0x100)
                        string += letter
                        data //= 0x100
                    if data != 0:
                        break
                    i += 4
                print(string)
                return EXC_NONE
            elif n == 57:                               # sys_close
                return EXC_NONE
            elif n == 93:                               # sys_exit
                return EXC_FIN
            elif n == 63:                               # sys_read
                address             = a1
                all_input           = input("")
                
                remainder           = address % 4
                i                   = all_input[0]
                remain_string       = all_input[1:]
                data                = ord(i) << (remainder * 8)
                self.regs.write(10, data)
                self.vmem.access(True, address - remainder, data, M_XWR)

                imm                 = 1
                
                while imm < len(all_input) - 1:
                    i               = remain_string[0]
                    remain_string   = remain_string[1:]
                    remainder      += 1
                    if remainder == 4:
                        address    += 4
                        remainder   = 0
                    data            = ord(i) << (remainder * 8)
                    self.vmem.access(True, address - remainder, data, M_XWR)
                    imm            += 1
                # data        = 0
                # i           = 0
                # for c in string:
                #     i      += 1
                #     if i % 4   == 1:
                #         data += ord(c)
                #     elif i % 4 == 2:
                #         data += ord(c) * 256
                #     elif i % 4 == 3:
                #         data += ord(c) * 256 * 256
                #     else:
                #         data += ord(c) * 256 * 256 * 256
                #         heap.access(True, address, data, M_XWR)
                #         data = 0
                #         address += 4
                # if not (i % 4 == 0):
                #     heap.access(True, address, data, M_XWR)
                return EXC_NONE
            elif n == 62:
                return EXC_NONE
        else:
            return SYS_ERROR


#--------------------------------------------------------------------------
#   Utility functions for command line parsing
#--------------------------------------------------------------------------

def show_usage(name):
    print("SNURISC: A RISC-V Instruction Set Simulator in Python")
    print("Usage: %s [-l n] [-c m] [-v r] filename" % name)
    print("\tfilename: RISC-V executable file name")
    print("\t-l sets the desired log level n (default: 1)")
    print("\t   0: shows no output message")
    print("\t   1: dumps registers at the end of the execution")
    print("\t   2: dumps registers and data memory at the end of the execution")
    print("\t   3: 2 + shows instruction executed in each cycle")
    print("\t   4: 3 + shows full information for each instruction")
    print("\t   5: 4 + dumps registers for each cycle")
    print("\t   6: 5 + dumps data memory for each cycle")
    print("\t-c shows logs after cycle m (default: 0, only effective for log level 3 or higher)")
    print("\t-v activates virtual memory, to run regular elf file (default: 0, activate for non-zero integer)")


def parse_args(args):

    if (not len(args) in [ 2, 4, 6, 8 ]):
        return None

    index = 1
    while True:
        if args[index].startswith('-'):
            if args[index] == '-l':
                try:
                    level = int(args[index + 1])
                except ValueError:
                    level = 999
                if level > Log.MAX_LOG_LEVEL:
                    print("Invalid log level '%s'" % args[index + 1])
                    return None
                index += 2
                Log.level = level
            elif args[index] == '-c':
                try:
                    cycle = int(args[index + 1])
                except ValueError:
                    print("Invalid cycle number '%s'" % args[index + 1])
                    return None
                index += 2
                Log.start_cycle = cycle
            elif args[index] == '-v':
                try:
                    vmem_activate = int(args[index + 1])
                except ValueError:
                    vmem_activate = 0
                index += 2
                Log.vmem_activate = (vmem_activate != 0)
            else:
                print("Invalid option '%s'" % args[index])
                return None
        else:
            break

    if len(args) != index + 1:
        print("Invalid argument '%s'" % args[index + 1:])
        return None

    return args[index]      # executable file name


#--------------------------------------------------------------------------
#   Simulator main
#--------------------------------------------------------------------------

def main():
    filename = parse_args(sys.argv)
    if not filename:
        show_usage(sys.argv[0])
        sys.exit()

    cpu = SNURISC(filename)
    prog = Program()
    
    if Log.vmem_activate:
        Log.vmem_activate = False
        entry_point = prog.load(cpu, "./pk")
        cpu.run(DEFAULT_RSTVEC)
        Log.vmem_activate = True
    entry_point = prog.load(cpu, filename)
    
    if not entry_point:
        sys.exit()
    cpu.run(entry_point)
    Stat.show()


if __name__ == '__main__':
    main()


