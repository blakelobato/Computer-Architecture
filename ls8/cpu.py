"""CPU functionality."""

import sys
import os.path

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.isPaused = False

    # accept a memory address to read and return the value stored 
    def ram_read(self, address):
        return self.ram[address] or 'Nothing there'

    # take a value to write -- write to the ram[memory data register]
    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self, file_name):
        """Load a program into memory."""
        address = 0

        file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_path) as f:
                for line in f:
                    num = line.split("#")[0].strip()
                    try:
                        instruction = int(num, 2)
                        self.ram[address] = instruction
                        address += 1
                    except:
                        continue
        except:
            print(f'Could not find file with the name of: {file_name}')
            sys.exit(1)

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.isPaused:

            IR = self.ram_read[self.pc]

            # LDI
            if IR == 0b10000010:
                nreg = self.ram[self.pc + 1]
                nval = self.ram[self.pc + 2]
                self.reg[nreg] = nval
                # self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
            # PRN
            elif IR == 0b01000111:
                print(self.reg[self.ram_read(self.ram[self.pc + 1])])
                self.pc += 2

            # HLT
            elif IR == 0b00000001:
                self.isPaused = True
                break

            elif IR == 0b10100010:
                multiple1 = self.ram_read(self.ram[pc + 1])
                multiple2 = self.ram_read(self.ram[pc + 2])
                self.alu("MUL", multiple1, multiple2)
                self.pc += 1
            # increment self.pc after running each command
            # self.pc += 1
