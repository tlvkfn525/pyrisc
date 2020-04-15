#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
#
#   Constant definitions
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


import numpy as np


#--------------------------------------------------------------------------
#   Data types
#--------------------------------------------------------------------------

WORD                = np.uint32
SWORD               = np.int32


#--------------------------------------------------------------------------
#   RISC-V constants
#--------------------------------------------------------------------------

WORD_SIZE           = 4
NUM_REGS            = 32

BUBBLE              = WORD(0x00004033)      # Machine-generated NOP:  xor x0, x0, x0
NOP                 = WORD(0x00000013)      # Software-generated NOP: addi zero, zero, 0
ILLEGAL             = WORD(0xffffffff)

OP_MASK             = WORD(0x0000007f)
OP_SHIFT            = 0
RD_MASK             = WORD(0x00000f80)
RD_SHIFT            = 7
FUNCT3_MASK         = WORD(0x00007000)
FUNCT3_SHIFT        = 12
RS1_MASK            = WORD(0x000f8000)
RS1_SHIFT           = 15
RS2_MASK            = WORD(0x01f00000)
RS2_SHIFT           = 20
FUNCT7_MASK         = WORD(0xfe000000)
FUNCT7_SHIFT        = 25


#--------------------------------------------------------------------------
#   Memory control signals
#--------------------------------------------------------------------------

M_XRD               = 0
M_XWR               = 1


#--------------------------------------------------------------------------
#   ISA table index
#--------------------------------------------------------------------------

IN_NAME             = 0
IN_MASK             = 1
IN_TYPE             = 2
IN_CLASS            = 3
IN_ALU1             = 4
IN_ALU2             = 5
IN_OP               = 6
IN_MT               = 7


#--------------------------------------------------------------------------
#   ISA table[IN_TYPE]: Instruction types for disassembling
#--------------------------------------------------------------------------

R_TYPE              = 0
I_TYPE              = 1
IL_TYPE             = 2     # I_TYPE, but load instruction
IJ_TYPE             = 3     # I_TYPE, but jalr instruction
U_TYPE              = 4
S_TYPE              = 5
B_TYPE              = 6
J_TYPE              = 7
X_TYPE              = 8
P_TYPE              = 9     # Privileged instructions
PI_TYPE             = 10    # Privileged instruction with zero-extended immediate


#--------------------------------------------------------------------------
#   ISA table[IN_CLASS]: Instruction classes for collecting stats
#--------------------------------------------------------------------------

CL_ALU              = 0
CL_MEM              = 1
CL_CTRL             = 2
CL_CSR              = 3     # Accessing CSR


#--------------------------------------------------------------------------
#   ISA table[IN_ALU1]: ALU operand select 1
#--------------------------------------------------------------------------

OP1_X               = 0
OP1_RS1             = 1         
OP1_PC              = 2
OP1_IMM             = 3     # zero-extended immediate(zimm) for privileged instructions


#--------------------------------------------------------------------------
#   ISA table[IN_ALU2]: ALU operand select 2
#--------------------------------------------------------------------------

OP2_X               = 0
OP2_RS2             = 1         
OP2_IMI             = 2         
OP2_IMS             = 3         
OP2_IMU             = 4
OP2_IMJ             = 5
OP2_IMB             = 6
OP2_CSR             = 7


#--------------------------------------------------------------------------
#   ISA table[IN_OP]: ALU and memory operation control
#--------------------------------------------------------------------------

ALU_X               = 0
ALU_ADD             = 1
ALU_SUB             = 2
ALU_SLL             = 3
ALU_SRL             = 4
ALU_SRA             = 5
ALU_AND             = 6
ALU_OR              = 7
ALU_XOR             = 8
ALU_SLT             = 9
ALU_SLTU            = 10
MEM_LD              = 11
MEM_ST              = 12


#--------------------------------------------------------------------------
#   ISA table[IN_MT]: Memory operation type
#--------------------------------------------------------------------------

MT_X                = 0
MT_B                = 1
MT_H                = 2
MT_W                = 3
MT_D                = 4
MT_BU               = 5
MT_HU               = 6
MT_WU               = 7


#--------------------------------------------------------------------------
#   Exceptions
#--------------------------------------------------------------------------

EXC_NONE            = 0         # EXC_NONE should be zero
EXC_IMEM_ERROR      = 1
EXC_DMEM_ERROR      = 2
EXC_ILLEGAL_INST    = 4
EXC_FIN             = 8
EXC_FENCE           = 16
EXC_OS_ERROR        = 32

EXC_MSG = {         EXC_IMEM_ERROR:     "imem access error", 
                    EXC_DMEM_ERROR:     "dmem access error",
                    EXC_ILLEGAL_INST:   "illegal instruction",
}

#--------------------------------------------------------------------------
#   Privilege level
#--------------------------------------------------------------------------

PRV_U               = 0
PRV_S               = 1
PRV_H               = 2
PRV_M               = 3

#--------------------------------------------------------------------------
#   Configurations
#--------------------------------------------------------------------------

# Memory configurations
#   IMEM: 0x80000000 - 0x8000ffff (1024KB)
#   DMEM: 0x80010000 - 0x8002ffff (2048KB)

IMEM_START          = WORD(0x80000000)      # IMEM: 0x80000000 - 0x8000ffff (1024KB)
IMEM_SIZE           = WORD(64 * 1024)       
DMEM_START          = WORD(0x80010000)      # DMEM: 0x80010000 - 0x8002ffff (2048KB)
DMEM_SIZE           = WORD(128 * 1024)
HEAP_START          = WORD(0x14cc4)      # Heap grows from here
HEAP_SIZE           = WORD(440)

DEFAULT_RSTVEC      = WORD(0x1000)          # default reset vector: beginning address
RESET_VEC_SIZE      = 32

#--------------------------------------------------------------------------
#   Privilege level register number encoding
#--------------------------------------------------------------------------

CSR_FFLAGS          = 0x1
CSR_FRM             = 0x2
CSR_FCSR            = 0x3
CSR_USTATUS         = 0x0
CSR_UIE             = 0x4
CSR_UTVEC           = 0x5
CSR_VSTART          = 0x8
CSR_VXSAT           = 0x9
CSR_VXRM            = 0xa
CSR_USCRATCH        = 0x40
CSR_UEPC            = 0x41
CSR_UCAUSE          = 0x42
CSR_UTVAL           = 0x43
CSR_UIP             = 0x44
CSR_CYCLE           = 0xc00
CSR_TIME            = 0xc01
CSR_INSTRET         = 0xc02
CSR_HPMCOUNTER3     = 0xc03
CSR_HPMCOUNTER4     = 0xc04
CSR_HPMCOUNTER5     = 0xc05
CSR_HPMCOUNTER6     = 0xc06
CSR_HPMCOUNTER7     = 0xc07
CSR_HPMCOUNTER8     = 0xc08
CSR_HPMCOUNTER9     = 0xc09
CSR_HPMCOUNTER10    = 0xc0a
CSR_HPMCOUNTER11    = 0xc0b
CSR_HPMCOUNTER12    = 0xc0c
CSR_HPMCOUNTER13    = 0xc0d
CSR_HPMCOUNTER14    = 0xc0e
CSR_HPMCOUNTER15    = 0xc0f
CSR_HPMCOUNTER16    = 0xc10
CSR_HPMCOUNTER17    = 0xc11
CSR_HPMCOUNTER18    = 0xc12
CSR_HPMCOUNTER19    = 0xc13
CSR_HPMCOUNTER20    = 0xc14
CSR_HPMCOUNTER21    = 0xc15
CSR_HPMCOUNTER22    = 0xc16
CSR_HPMCOUNTER23    = 0xc17
CSR_HPMCOUNTER24    = 0xc18
CSR_HPMCOUNTER25    = 0xc19
CSR_HPMCOUNTER26    = 0xc1a
CSR_HPMCOUNTER27    = 0xc1b
CSR_HPMCOUNTER28    = 0xc1c
CSR_HPMCOUNTER29    = 0xc1d
CSR_HPMCOUNTER30    = 0xc1e
CSR_HPMCOUNTER31    = 0xc1f

CSR_VL              = 0xc20
CSR_VTYPE           = 0xc21
CSR_VLENB           = 0xc22
CSR_SSTATUS         = 0x100
CSR_SIE             = 0x104
CSR_STVEC           = 0x105
CSR_SCOUNTEREN      = 0x106
CSR_SSCRATCH        = 0x140
CSR_SEPC            = 0x141
CSR_SCAUSE          = 0x142
CSR_STVAL           = 0x143
CSR_SIP             = 0x144
CSR_SATP            = 0x180
CSR_VSSTATUS        = 0x200
CSR_VSIE            = 0x204
CSR_VSTVEC          = 0x205
CSR_VSSCRATCH       = 0x250
CSR_VSEPC           = 0x241
CSR_VSCAUSE         = 0x242
CSR_VSTVAL          = 0x243
CSR_VSIP            = 0x244
CSR_VSATP           = 0x280
CSR_HSTATUS         = 0x600
CSR_HEDELEG         = 0x602
CSR_HIDELEG         = 0x603
CSR_HCOUNTEREN      = 0x606
CSR_HGATP           = 0x680
CSR_UTVT            = 0x7
CSR_UNXTI           = 0x45
CSR_UINTSTATUS      = 0x46
CSR_USCRATCHCSW     = 0x48
CSR_USCRATCHCSWL    = 0x49
CSR_STVT            = 0x107
CSR_SNXTI           = 0x145
CSR_SINTSTATUS      = 0x146
CSR_SSCRATCHCSW     = 0x148
CSR_SSCRATCHCSWL    = 0x149
CSR_MTVT            = 0x307
CSR_MNXTI           = 0x345
CSR_MINTSTATUS      = 0x346
CSR_MSCRATCHCSW     = 0x348
CSR_MSCRATCHCSWL    = 0x349

# Machine Trap Setup

CSR_MSTATUS         = 0x300
CSR_MISA            = 0x301
CSR_MEDELEG         = 0x302
CSR_MIDELEG         = 0x303
CSR_MIE             = 0x304
CSR_MTVEC           = 0x305
CSR_MCOUNTEREN      = 0x306

# Machine Trap Handling

CSR_MSCRATCH        = 0x340
CSR_MEPC            = 0x341
CSR_MCAUSE          = 0x342
CSR_MTVAL           = 0x343
CSR_MIP             = 0x344

# Machine Memory Protection

CSR_PMPCFG0         = 0x3a0
CSR_PMPCFG1         = 0x3a1
CSR_PMPCFG2         = 0x3a2
CSR_PMPCFG3         = 0x3a3
CSR_PMPADDR0        = 0x3b0
CSR_PMPADDR1        = 0x3b1
CSR_PMPADDR2        = 0x3b2
CSR_PMPADDR3        = 0x3b3
CSR_PMPADDR4        = 0x3b4
CSR_PMPADDR5        = 0x3b5
CSR_PMPADDR6        = 0x3b6
CSR_PMPADDR7        = 0x3b7
CSR_PMPADDR8        = 0x3b8
CSR_PMPADDR9        = 0x3b9
CSR_PMPADDR10       = 0x3ba
CSR_PMPADDR11       = 0x3bb
CSR_PMPADDR12       = 0x3bc
CSR_PMPADDR13       = 0x3bd
CSR_PMPADDR14       = 0x3be
CSR_PMPADDR15       = 0x3bf

CSR_TSELECT         = 0x7a0
CSR_TDATA1          = 0x7a1
CSR_TDATA2          = 0x7a2
CSR_TDATA3          = 0x7a3
CSR_DCSR            = 0x7b0
CSR_DPC             = 0x7b1
CSR_DSCRATCH        = 0x7b2

# Machine Counter/Timers

CSR_MCYCLE          = 0xb00
CSR_MINSTRET        = 0xb02
CSR_MHPMCOUNTER3    = 0xb03
CSR_MHPMCOUNTER4    = 0xb04
CSR_MHPMCOUNTER5    = 0xb05
CSR_MHPMCOUNTER6    = 0xb06
CSR_MHPMCOUNTER7    = 0xb07
CSR_MHPMCOUNTER8    = 0xb08
CSR_MHPMCOUNTER9    = 0xb09
CSR_MHPMCOUNTER10   = 0xb0a
CSR_MHPMCOUNTER11   = 0xb0b
CSR_MHPMCOUNTER12   = 0xb0c
CSR_MHPMCOUNTER13   = 0xb0d
CSR_MHPMCOUNTER14   = 0xb0e
CSR_MHPMCOUNTER15   = 0xb0f
CSR_MHPMCOUNTER16   = 0xb10
CSR_MHPMCOUNTER17   = 0xb11
CSR_MHPMCOUNTER18   = 0xb12
CSR_MHPMCOUNTER19   = 0xb13
CSR_MHPMCOUNTER20   = 0xb14
CSR_MHPMCOUNTER21   = 0xb15
CSR_MHPMCOUNTER22   = 0xb16
CSR_MHPMCOUNTER23   = 0xb17
CSR_MHPMCOUNTER24   = 0xb18
CSR_MHPMCOUNTER25   = 0xb19
CSR_MHPMCOUNTER26   = 0xb1a
CSR_MHPMCOUNTER27   = 0xb1b
CSR_MHPMCOUNTER28   = 0xb1c
CSR_MHPMCOUNTER29   = 0xb1d
CSR_MHPMCOUNTER30   = 0xb1e
CSR_MHPMCOUNTER31   = 0xb1f

# Machine Counter Setup

# CSR_MCOUNTINHIBIT   = 0x320     # not included in spike encoding
CSR_MHPEVENT3       = 0x323
CSR_MHPEVENT4       = 0x324
CSR_MHPEVENT5       = 0x325
CSR_MHPEVENT6       = 0x326
CSR_MHPEVENT7       = 0x327
CSR_MHPEVENT8       = 0x328
CSR_MHPEVENT9       = 0x329
CSR_MHPEVENT10      = 0x32a
CSR_MHPEVENT11      = 0x32b
CSR_MHPEVENT12      = 0x32c
CSR_MHPEVENT13      = 0x32d
CSR_MHPEVENT14      = 0x32e
CSR_MHPEVENT15      = 0x32f
CSR_MHPEVENT16      = 0x330
CSR_MHPEVENT17      = 0x331
CSR_MHPEVENT18      = 0x332
CSR_MHPEVENT19      = 0x333
CSR_MHPEVENT20      = 0x334
CSR_MHPEVENT21      = 0x335
CSR_MHPEVENT22      = 0x336
CSR_MHPEVENT23      = 0x337
CSR_MHPEVENT24      = 0x338
CSR_MHPEVENT25      = 0x339
CSR_MHPEVENT26      = 0x33a
CSR_MHPEVENT27      = 0x33b
CSR_MHPEVENT28      = 0x33c
CSR_MHPEVENT29      = 0x33d
CSR_MHPEVENT30      = 0x33e
CSR_MHPEVENT31      = 0x33f

# Machine Information Registers

CSR_MVENDORID       = 0xf11
CSR_MARCHID         = 0xf12
CSR_MIMPID          = 0xf13
CSR_MHARTID         = 0xf14

CSR_CYCLEH          = 0xc80
CSR_TIMEH           = 0xc81
CSR_INSTRETH        = 0xc82
CSR_HPMCOUNTER3H    = 0xc83
CSR_HPMCOUNTER4H    = 0xc84
CSR_HPMCOUNTER5H    = 0xc85
CSR_HPMCOUNTER6H    = 0xc86
CSR_HPMCOUNTER7H    = 0xc87
CSR_HPMCOUNTER8H    = 0xc88
CSR_HPMCOUNTER9H    = 0xc89
CSR_HPMCOUNTER10H   = 0xc8a
CSR_HPMCOUNTER11H   = 0xc8b
CSR_HPMCOUNTER12H   = 0xc8c
CSR_HPMCOUNTER13H   = 0xc8d
CSR_HPMCOUNTER14H   = 0xc8e
CSR_HPMCOUNTER15H   = 0xc8f
CSR_HPMCOUNTER16H   = 0xc90
CSR_HPMCOUNTER17H   = 0xc91
CSR_HPMCOUNTER18H   = 0xc92
CSR_HPMCOUNTER19H   = 0xc93
CSR_HPMCOUNTER20H   = 0xc94
CSR_HPMCOUNTER21H   = 0xc95
CSR_HPMCOUNTER22H   = 0xc96
CSR_HPMCOUNTER23H   = 0xc97
CSR_HPMCOUNTER24H   = 0xc98
CSR_HPMCOUNTER25H   = 0xc99
CSR_HPMCOUNTER26H   = 0xc9a
CSR_HPMCOUNTER27H   = 0xc9b
CSR_HPMCOUNTER28H   = 0xc9c
CSR_HPMCOUNTER29H   = 0xc9d
CSR_HPMCOUNTER30H   = 0xc9e
CSR_HPMCOUNTER31H   = 0xc9f
CSR_MCYCLEH         = 0xb80
CSR_MINSTRETH       = 0xb82
CSR_MHPMCOUNTER3H   = 0xb83
CSR_MHPMCOUNTER4H   = 0xb84
CSR_MHPMCOUNTER5H   = 0xb85
CSR_MHPMCOUNTER6H   = 0xb86
CSR_MHPMCOUNTER7H   = 0xb87
CSR_MHPMCOUNTER8H   = 0xb88
CSR_MHPMCOUNTER9H   = 0xb89
CSR_MHPMCOUNTER10H  = 0xb8a
CSR_MHPMCOUNTER11H  = 0xb8b
CSR_MHPMCOUNTER12H  = 0xb8c
CSR_MHPMCOUNTER13H  = 0xb8d
CSR_MHPMCOUNTER14H  = 0xb8e
CSR_MHPMCOUNTER15H  = 0xb8f
CSR_MHPMCOUNTER16H  = 0xb90
CSR_MHPMCOUNTER17H  = 0xb91
CSR_MHPMCOUNTER18H  = 0xb92
CSR_MHPMCOUNTER19H  = 0xb93
CSR_MHPMCOUNTER20H  = 0xb94
CSR_MHPMCOUNTER21H  = 0xb95
CSR_MHPMCOUNTER22H  = 0xb96
CSR_MHPMCOUNTER23H  = 0xb97
CSR_MHPMCOUNTER24H  = 0xb98
CSR_MHPMCOUNTER25H  = 0xb99
CSR_MHPMCOUNTER26H  = 0xb9a
CSR_MHPMCOUNTER27H  = 0xb9b
CSR_MHPMCOUNTER28H  = 0xb9c
CSR_MHPMCOUNTER29H  = 0xb9d
CSR_MHPMCOUNTER30H  = 0xb9e
CSR_MHPMCOUNTER31H  = 0xb9f

#--------------------------------------------------------------------------
#   syscall constants: compare with a7 value
#--------------------------------------------------------------------------

sysconst_list       = [ 80, 214, 64, 57, 93, 63, 62 ]
# SYS_exit            = 93
# SYS_exit_group      = 94
# SYS_getpid          = 172
# SYS_kill            = 129
# SYS_read            = 63
# SYS_write           = 64
# SYS_openat          = 56
# SYS_close           = 57
# SYS_lseek           = 62
# SYS_brk             = 214
# SYS_linkat          = 37
SYS_ERROR           = -1
#define SYS_exit 93
#define SYS_exit_group 94
#define SYS_getpid 172
#define SYS_kill 129
#define SYS_read 63
#define SYS_write 64
#define SYS_openat 56
#define SYS_close 57
#define SYS_lseek 62
#define SYS_brk 214
#define SYS_linkat 37
#define SYS_unlinkat 35
#define SYS_mkdirat 34
#define SYS_renameat 38
#define SYS_chdir 49
#define SYS_getcwd 17
#define SYS_fstat 80
#define SYS_fstatat 79
#define SYS_faccessat 48
#define SYS_pread 67
#define SYS_pwrite 68
#define SYS_uname 160
#define SYS_getuid 174
#define SYS_geteuid 175
#define SYS_getgid 176
#define SYS_getegid 177
#define SYS_mmap 222
#define SYS_munmap 215
#define SYS_mremap 216
#define SYS_mprotect 226
#define SYS_prlimit64 261
#define SYS_getmainvars 2011
#define SYS_rt_sigaction 134
#define SYS_writev 66
#define SYS_gettimeofday 169
#define SYS_times 153
#define SYS_fcntl 25
#define SYS_ftruncate 46
#define SYS_getdents 61
#define SYS_dup 23
#define SYS_dup3 24
#define SYS_readlinkat 78
#define SYS_rt_sigprocmask 135
#define SYS_ioctl 29
#define SYS_getrlimit 163
#define SYS_setrlimit 164
#define SYS_getrusage 165
#define SYS_clock_gettime 113
#define SYS_set_tid_address 96
#define SYS_set_robust_list 99
#define SYS_madvise 233

#define OLD_SYSCALL_THRESHOLD 1024
#define SYS_open 1024
#define SYS_link 1025
#define SYS_unlink 1026
#define SYS_mkdir 1030
#define SYS_access 1033
#define SYS_stat 1038
#define SYS_lstat 1039
#define SYS_time 1062
