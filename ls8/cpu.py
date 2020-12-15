"""CPU functionality."""

import sys
HLT = 0b00000001  # Halt function,
LDI = 0b10000010  # SAVE function
PRN = 0b01000111  # PRINT function
MUL = 0b10100010  # MULTIPLY function
PUSH = 0b01000101  # PUSH function 
POP = 0b01000110   # POP function
CALL = 0b01010000  # CALL function
RET = 0b00010001  # RET function
ADD = 0b10100000  # ADD function
JMP = 0b01010100  # JMP - jump to address stored in given register
CMP = 0b10100111 # CMP - compare,
JEQ = 0b01010101 #JQE function
JNE = 0b01010110  # JNE - Jump Not Equal 


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.reg[self.SP] = len(self.ram) - 1
        self.running = False
        self.EQUAL = None
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

    def load(self):
        """Load a program into memory."""
        address = 0
        
        if len(sys.argv) == 2:
            filename = sys.argv[1]
        else:
            print('No filename provided')
            return None

        with open(filename) as file_in:
            program = []
            for line in file_in:
                str = line[0:8]
                if str.isnumeric():
                    final_str = '0b' + str
                    program.append(int(final_str, base=2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            self.EQUAL = (self.reg[reg_a] == self.reg[reg_b])
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return(self.ram[MAR])

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def handle_HLT(self):
        self.running = False
        self.pc += 1

    def handle_LDI(self):
        val_to_save = self.ram[self.pc + 2]
        destination = self.ram[self.pc + 1]
        self.reg[destination] = val_to_save
        self.pc += 3

    def handle_MUL(self):
        self.alu('MUL', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_ADD(self):
        self.alu('ADD', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_PRN(self):
        reg_loc = self.ram[self.pc + 1]
        val_to_print = self.reg[reg_loc]
        print(f'PRINTING VALUE: {val_to_print}')
        self.pc += 2

    def handle_PUSH(self):
        reg = self.ram[self.pc + 1]
        self.reg[self.SP] -= 1
        reg_value = self.reg[reg]
        self.ram[self.reg[self.SP]] = reg_value
        self.pc += 2

    def handle_POP(self):
        value = self.ram[self.reg[self.SP]]
        reg = self.ram[self.pc + 1]
        self.reg[reg] = value
        self.reg[self.SP] += 1
        self.pc += 2

    def handle_CALL(self):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.pc + 2
        reg = self.ram[self.pc + 1]
        reg_value = self.reg[reg]
        self.pc = reg_value

    def handle_RET(self):
        return_value = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc = return_value

    def handle_JMP(self):
        reg_loc = self.ram[self.pc + 1]
        jump_to = self.reg[reg_loc]
        self.pc = jump_to

    def handle_CMP(self):
        self.alu('CMP', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_JEQ(self):
        if self.EQUAL == True:
            reg_loc = self.ram[self.pc + 1]
            jump_to = self.reg[reg_loc]
            self.pc = jump_to
        else:
            self.pc += 2

    def handle_JNE(self):
        if self.EQUAL == False:
            reg_loc = self.ram[self.pc + 1]
            jump_to = self.reg[reg_loc]
            self.pc = jump_to
        else:
            self.pc += 2


    def run(self):
        """Run the CPU."""
        IR = None
        self.running = True

        while self.running:
            IR = self.ram[self.pc]
            COMMAND = IR
            if COMMAND in self.branchtable:
                self.branchtable[COMMAND]()
            else:
                sys.exit(1)