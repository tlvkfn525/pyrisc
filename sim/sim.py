#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
#
#   Class for instruction-level simulation.
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


import sys

from consts import *
from isa import *
from components import *
from program import *

#--------------------------------------------------------------------------
#   Sim: simulates the CPU execution
#--------------------------------------------------------------------------

class Sim(object):

    @staticmethod
    def run(cpu, entry_point):

        Sim.cpu = cpu
        Sim.cpu.pc.write(entry_point)
        status = EXC_NONE

        while True:
            # Execute a single instruction
            status = Sim.single_step()
            
            # Update stats
            Stat.cycle      += 1
            Stat.icount     += 1

            # Show logs after executing a single instruction
            if Log.level >= 5:
                Sim.cpu.regs.dump()
            if Log.level >= 6:
                Sim.cpu.dmem.dump(skipzero = True)
            if not status == EXC_NONE:
                break
      
        # Handle exceptions, if any
        if (status & EXC_DMEM_ERROR):
            print("Exception '%s' occurred at 0x%08x -- Program terminated" % (EXC_MSG[EXC_DMEM_ERROR], Sim.cpu.pc.read()))
        elif (status & EXC_FIN):
            print("Execution completed")
        elif (status & EXC_ILLEGAL_INST):
            print("Exception '%s' occurred at 0x%08x -- Program terminated" % (EXC_MSG[EXC_ILLEGAL_INST], Sim.cpu.pc.read()))
        elif (status & EXC_IMEM_ERROR):
            print("Exception '%s' occurred at 0x%08x -- Program terminated" % (EXC_MSG[EXC_IMEM_ERROR], Sim.cpu.pc.read()))
        elif (status & EXC_FENCE):
            print("***** pk: Ready to start C program *****")
        elif (status & EXC_OS_ERROR):
            print("Invalid ECALL. Pyrisc simulater cannot process.")

        # Show logs after finishing the program execution
        if Log.level > 0:
            if Log.level < 5:
                Sim.cpu.regs.dump()
            if Log.level > 1 and Log.level < 6:
                Sim.cpu.dmem.dump(skipzero = True)
            

    @staticmethod
    def log(pc, inst, rd, wbdata, pc_next):

        if Stat.cycle < Log.start_cycle:
            return
        if Log.level >= 4:
            info = "# R[%d] <- 0x%08x, pc_next=0x%08x" % (rd, wbdata, pc_next) if rd else \
                   "# pc_next=0x%08x" % pc_next
        else:
            info = ''
        if Log.level >= 3:
            print("%d 0x%08x: %-30s%-s" % (Stat.cycle, pc, Program.disasm(pc, inst), info))
        else:
            return
    
    def run_alu(pc, inst, opcode, cs):
        np.seterr(all='ignore')
        Stat.inst_alu += 1

        rs1         = RISCV.rs1(inst)
        rs2         = RISCV.rs2(inst)
        rd          = RISCV.rd(inst)

        imm_i       = RISCV.imm_i(inst)
        imm_u       = RISCV.imm_u(inst)

        rs1_data    = Sim.cpu.regs.read(rs1)
        rs2_data    = Sim.cpu.regs.read(rs2)

        alu1        = rs1_data      if cs[IN_ALU1] == OP1_RS1    else \
                      pc            if cs[IN_ALU1] == OP1_PC     else \
                      WORD(0)       

        alu2        = rs2_data      if cs[IN_ALU2] == OP2_RS2    else \
                      imm_i         if cs[IN_ALU2] == OP2_IMI    else \
                      imm_u         if cs[IN_ALU2] == OP2_IMU    else \
                      WORD(0)

        
        alu_out     = WORD(alu1 + alu2)                     if (cs[IN_OP] == ALU_ADD)    else \
                      WORD(alu1 - alu2)                     if (cs[IN_OP] == ALU_SUB)    else \
                      WORD(alu1 & alu2)                     if (cs[IN_OP] == ALU_AND)    else \
                      WORD(alu1 | alu2)                     if (cs[IN_OP] == ALU_OR)     else \
                      WORD(alu1 ^ alu2)                     if (cs[IN_OP] == ALU_XOR)    else \
                      SWORD(alu1) < SWORD(alu2)             if (cs[IN_OP] == ALU_SLT)    else \
                      WORD(alu1) < WORD(alu2)               if (cs[IN_OP] == ALU_SLTU)   else \
                      WORD(alu1 << (alu2 & 0x1f))           if (cs[IN_OP] == ALU_SLL)    else \
                      WORD(SWORD(alu1) >> (alu2 & 0x1f))    if (cs[IN_OP] == ALU_SRA)    else \
                      WORD(alu1 >> (alu2 & 0x1f))           if (cs[IN_OP] == ALU_SRL)    else \
                      WORD(0)

        pc_next     = pc + 4

        Sim.cpu.regs.write(rd, alu_out)
        Sim.cpu.pc.write(pc_next)
        Sim.log(pc, inst, rd, alu_out, pc_next)
        return EXC_NONE

    def run_mem(pc, inst, opcode, cs):
        Stat.inst_mem += 1
       
        rs1         = RISCV.rs1(inst)
        rs1_data    = Sim.cpu.regs.read(rs1)

        if (cs[IN_OP] == MEM_LD):
            rd          = RISCV.rd(inst)
            imm_i       = RISCV.imm_i(inst)
            mem_addr    = rs1_data + SWORD(imm_i)
            funct3      = (inst & FUNCT3_MASK) >> FUNCT3_SHIFT
            remainder   = mem_addr % WORD_SIZE
            if (remainder != 0 and funct3 != 2):
                mem_addr -= remainder
            mem_data, dmem_ok = Sim.cpu.dmem.access(True, mem_addr, 0, M_XRD)
            
            if dmem_ok:
                if (funct3 == 0):                           # LB
                    mem_data = (mem_data >> (remainder * 8)) & 0xFF
                    sign = mem_data >> 7
                    mem_data += ((0 - sign) << 8)
                elif (funct3 == 4):                         # LBU
                    mem_data = (mem_data >> (remainder * 8)) & 0xFF
                elif (funct3 == 1):                         # LH
                    mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                    sign = mem_data >> 15
                    mem_data += ((0 - sign) << 8)
                elif (funct3 == 5):                         # LHU
                    mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                elif (funct3 != 2):
                    return EXC_ILLEGAL_INST
                Sim.cpu.regs.write(rd, mem_data)
            else:
                mem_data, vdmem_ok = Sim.cpu.vmem.access(True, mem_addr, 0, M_XRD)
                if vdmem_ok:
                    if (funct3 == 0):                           # LB
                        mem_data = (mem_data >> (remainder * 8)) & 0xFF
                        sign = mem_data >> 7
                        mem_data += ((0 - sign) << 8)
                    elif (funct3 == 4):                         # LBU
                        mem_data = (mem_data >> (remainder * 8)) & 0xFF
                    elif (funct3 == 1):                         # LH
                        mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                        sign = mem_data >> 15
                        mem_data += ((0 - sign) << 8)
                    elif (funct3 == 5):                         # LHU
                        mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                    elif (funct3 != 2):
                        return EXC_ILLEGAL_INST
                    Sim.cpu.regs.write(rd, mem_data)
                else:
                    mem_data, rstvec_ok = Sim.cpu.rstvec.access(True, mem_addr, 0, M_XRD)        # TODO: Combine memories
                    if rstvec_ok:
                        if (funct3 == 0):                           # LB
                            mem_data = (mem_data >> (remainder * 8)) & 0xFF
                            sign = mem_data >> 7
                            mem_data += ((0 - sign) << 8)
                        elif (funct3 == 4):                         # LBU
                            mem_data = (mem_data >> (remainder * 8)) & 0xFF
                        elif (funct3 == 1):                         # LH
                            mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                            sign = mem_data >> 15
                            mem_data += ((0 - sign) << 8)
                        elif (funct3 == 5):                         # LHU
                            mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                        elif (funct3 != 2):
                            return EXC_ILLEGAL_INST
                        Sim.cpu.regs.write(rd, mem_data)
                    else:
                        mem_data, imem_ok = Sim.cpu.imem.access(True, mem_addr, 0, M_XRD)
                        if imem_ok:
                            if (funct3 == 0):                           # LB
                                mem_data = (mem_data >> (remainder * 8)) & 0xFF
                                sign = mem_data >> 7
                                mem_data += ((0 - sign) << 8)
                            elif (funct3 == 4):                         # LBU
                                mem_data = (mem_data >> (remainder * 8)) & 0xFF
                            elif (funct3 == 1):                         # LH
                                mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                                sign = mem_data >> 15
                                mem_data += ((0 - sign) << 8)
                            elif (funct3 == 5):                         # LHU
                                mem_data = (mem_data >> (remainder * 8)) & 0xFFFF
                            elif (funct3 != 2):
                                return EXC_ILLEGAL_INST
                            Sim.cpu.regs.write(rd, mem_data)
                        else:
                            return EXC_DMEM_ERROR
            
        else:
            rd          = 0                     
            rs2         = RISCV.rs2(inst)
            rs2_data    = Sim.cpu.regs.read(rs2)

            imm_s       = RISCV.imm_s(inst)
            mem_addr    = rs1_data + SWORD(imm_s)
            funct3      = (inst & FUNCT3_MASK) >> FUNCT3_SHIFT
            remainder   = mem_addr % WORD_SIZE
            if (remainder != 0 and funct3 != 2):
                mem_addr -= remainder
            if (funct3 == 0):                               # SB
                rs2_data = rs2_data & 0xFF
            # elif (funct3 == 1):                           # SH
            #     rs2_data = rs2_data & 0xFFFF
            rs2_data = rs2_data << (remainder * 8)
            save_data, dmem_ok = Sim.cpu.dmem.access(True, mem_addr, 0, M_XRD)
            if dmem_ok:
                save_data = save_data & ((1 << (remainder * 8)) - 1)
                rs2_data += save_data
                mem_data = Sim.cpu.dmem.access(True, mem_addr, rs2_data, M_XWR)
            else:
                save_data, vdmem_ok = Sim.cpu.vmem.access(True, mem_addr, 0, M_XRD)
                if vdmem_ok:
                    save_data = save_data & ((1 << (remainder * 8)) - 1)
                    rs2_data += save_data
                    mem_data = Sim.cpu.vmem.access(True, mem_addr, rs2_data, M_XWR)
                else:
                    save_data, imem_ok = Sim.cpu.imem.access(True, mem_addr, 0, M_XRD)
                    if imem_ok:
                        save_data = save_data & ((1 << (remainder * 8)) - 1)
                        rs2_data += save_data
                        mem_data = Sim.cpu.imem.access(True, mem_addr, rs2_data, M_XWR)
                    else:
                        return EXC_DMEM_ERROR

        pc_next         = pc + 4
        Sim.cpu.pc.write(pc_next)
        Sim.log(pc, inst, rd, mem_data, pc_next)
        return EXC_NONE

    def run_ctrl(pc, inst, opcode, cs):

        Stat.inst_ctrl += 1

        rs1             = RISCV.rs1(inst)
        rs2             = RISCV.rs2(inst)
        rd              = RISCV.rd(inst)
        rs1_data        = Sim.cpu.regs.read(rs1)
        rs2_data        = Sim.cpu.regs.read(rs2)

        imm_i           = RISCV.imm_i(inst)
        imm_j           = RISCV.imm_j(inst)
        imm_b           = RISCV.imm_b(inst)
        pc_plus4        = pc + 4

        pc_next         = pc + imm_j        if opcode == JAL    else                                             \
                          pc + imm_b        if (opcode == BEQ and rs1_data == rs2_data) or                       \
                                                (opcode == BNE and not (rs1_data == rs2_data)) or                \
                                                (opcode == BLT and SWORD(rs1_data) < SWORD(rs2_data)) or         \
                                                (opcode == BGE and not (SWORD(rs1_data) < SWORD(rs2_data))) or   \
                                                (opcode == BLTU and WORD(rs1_data) < WORD(rs2_data)) or          \
                                                (opcode == BGEU and not (WORD(rs1_data) < WORD(rs2_data)))  else \
                          (rs1_data + imm_i) & WORD(0xfffffffe)     if opcode == JALR   else                     \
                          pc_plus4

        if (opcode in [ JAL, JALR ]):
            Sim.cpu.regs.write(rd, pc_plus4)
        Sim.cpu.pc.write(WORD(pc_next))
        Sim.log(pc, inst, rd, pc_plus4, WORD(pc_next))
        if pc == pc_next:
            return EXC_FIN
        return EXC_NONE

    def run_csr(pc, inst, opcode, cs):
        
        Stat.inst_ctrl += 1
        if (inst & FENCE_MASK) == FENCE:
            pc_next = pc + 4
            Sim.cpu.pc.write(pc_next)
            Sim.log(pc, inst, 0, 0, pc_next)
            return EXC_FENCE

        elif inst == ECALL:
            pc_next = pc + 4
            Sim.cpu.pc.write(pc_next)
            Sim.log(pc, inst, 0, 0, pc_next) 
            r = Sim.cpu.handle_syscall()
            if r == SYS_ERROR:
                return EXC_OS_ERROR
            else:
                return EXC_NONE

        elif inst == EBREAK:
            pc_next = pc + 4
            Sim.cpu.pc.write(pc_next)
            Sim.log(pc, inst, 0, 0, pc_next)
            return EXC_OS_ERROR



        rs1             = RISCV.rs1(inst)
        csr_addr        = inst >> 20
        rd              = RISCV.rd(inst)
        rs1_data        = Sim.cpu.regs.read(rs1)
        if ((inst & FUNCT3_MASK) >> FUNCT3_SHIFT) > 4:
            rs1_data = rs1
        prv_name        = csr_name(csr_addr)
        prv_reg         = Sim.cpu.prv_regs.find(prv_name)
        if (prv_reg != None):
            exc_imm = Sim.csr_handler(prv_reg, opcode, rs1_data, rd)
            if (exc_imm != EXC_NONE):
                return exc_imm

        else:
            return EXC_ILLEGAL_INST                 
        
        pc_next         = pc + 4
        Sim.cpu.pc.write(pc_next)
        Sim.log(pc, inst, rd, rs1_data, pc_next)
        return EXC_NONE

    @staticmethod
    def csr_handler(prv_reg, opcode, rs1_data, rd):
        csr_data    = prv_reg.read()
        Sim.cpu.regs.write(rd, csr_data)

        if   (opcode == CSRRW or opcode == CSRRWI):
            prv_reg.write(rs1_data)
            
        elif (opcode == CSRRS or opcode == CSRRSI):
            rs1_data = csr_data | rs1_data
            prv_reg.write(rs1_data)

        else:
            return EXC_ILLEGAL_INST
        
        return EXC_NONE

    func = [ run_alu, run_mem, run_ctrl, run_csr ]

    @staticmethod
    def single_step():

        pc         = Sim.cpu.pc.read()
        # Instruction fetch

        if Log.vmem_activate:
            inst, imem_status = Sim.cpu.vmem.access(True, pc, 0, M_XRD)
    
        else:
            inst, imem_status = Sim.cpu.imem.access(True, pc, 0, M_XRD)
            if not imem_status:
                inst, imem_status = Sim.cpu.rstvec.access(True, pc, 0, M_XRD)

                if not imem_status:
                    return EXC_IMEM_ERROR
       
        # Instruction decode 
        opcode  = RISCV.opcode(inst)
        if opcode == ILLEGAL:
            return EXC_ILLEGAL_INST
        cs = isa[opcode]
        return Sim.func[cs[IN_CLASS]](pc, inst, opcode, cs)
