"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Add list properties to the `CPU` class to hold 256 bytes of memory and 8
        # general-purpose registers.
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.sp = 0b00000111  # 7



        # Also add properties for any internal registers you need, e.g. `PC`.
        self.pc = 0

    # In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
    # the `CPU` object.

    # `ram_read()` should accept the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    # `raw_write()` should accept a value to write, and the address to write it to.
    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
            sys.exit(1)
        else:
            filepath = sys.argv[1]
            try:
                with open(filepath) as f:
                    for line in f:
                        # Split before and after comment symbols.
                        comment_split = line.split("#")
                        # Strip the extra space on each line.
                        num = comment_split[0].strip()
                        if num == "":
                            continue
                        instruction = int(num, 2)
                        self.ram[address] = instruction
                        address += 1

            except FileNotFoundError:
                print(f"{sys.argv[0]}: {sys.argv[1]} not found")
                sys.exit(2)

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
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI  = 0b10000010
        PRN  = 0b01000111
        HLT  = 0b00000001
        MUL  = 0b10100010
        PUSH = 0b01000101
        POP  = 0b01000110

        running = True
        self.reg[self.sp] = 0b11111111  # 255
        while running:
            # It needs to read the memory address that's stored in register `PC`, and store
            # that result in `IR`, the _Instruction Register_. This can just be a local
            # variable in `run()`.
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                self.reg[self.sp] -= 1  # Decrement SP.
                value = self.reg[operand_a]  # Get the register number operand.
                self.ram[self.reg[self.sp]] = value  # Store value in ram at the SP.
                self.pc += 2
            elif IR == POP:
                value = self.ram[self.reg[self.sp]]  # Get the value from ram at AT.
                self.reg[operand_a] = value  # Store the value from the stack in the register.
                self.reg[self.sp] += 1  # Increment SP.
                self.pc += 2
            elif IR == HLT:
                running = False
            else:
                print(f"{self.ram[self.pc]} is an unknown instruction!")
                break
