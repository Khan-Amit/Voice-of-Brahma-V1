# tvm.py
# Ternary Virtual Machine (TVM) Interpreter
# Part of Voice-of-Brahma-V1
# Author: Seliim Ahmed
# All Rights Reserved ®

from ternary_ascii import text_to_ternary, ternary_to_text

class TVM:
    """
    Ternary Virtual Machine
    Executes ternary instructions on a 5-trit word size.
    Memory: 64K ternary words (each word = 5 trits = 1 ASCII char)
    Registers: R0-R5 (each holds a ternary word)
    """

    def __init__(self, memory_size=65536):
        self.memory = ['00000'] * memory_size  # 5-trit words
        self.registers = {
            'R0': '00000',  # Accumulator
            'R1': '00000',  # General purpose
            'R2': '00000',  # General purpose
            'R3': '00000',  # Stack pointer
            'R4': '00000',  # Program counter
            'R5': '00000'   # Status register (carry, zero, etc.)
        }
        self.stack = []
        self.running = True
        self.instruction_count = 0

    def _trit_to_int(self, trits):
        """Convert 5-trit string to integer (0..242)."""
        val = 0
        for ch in trits:
            val = val * 3 + (ord(ch) - 48)
        return val

    def _int_to_trits(self, n, length=5):
        """Convert integer to ternary string with fixed length."""
        if n == 0:
            return '0' * length
        digits = []
        while n > 0:
            digits.append(str(n % 3))
            n //= 3
        return ''.join(reversed(digits)).zfill(length)

    def _get_reg(self, name):
        return self.registers[name]

    def _set_reg(self, name, value):
        self.registers[name] = value

    def _fetch(self):
        """Fetch instruction at program counter."""
        pc = self._trit_to_int(self._get_reg('R4'))
        if pc >= len(self.memory):
            raise ValueError("PC out of memory")
        return self.memory[pc]

    def _execute(self, instruction):
        """Execute a single instruction."""
        opcode = instruction[:5]  # First 5 trits = opcode
        operand = instruction[5:] if len(instruction) > 5 else ''
        op_int = self._trit_to_int(opcode)

        if op_int == 0:   # NOP
            pass
        elif op_int == 1: # ADD R0 = R0 + R1
            a = self._trit_to_int(self._get_reg('R0'))
            b = self._trit_to_int(self._get_reg('R1'))
            result = a + b
            carry = 1 if result >= 243 else 0  # 5-trit overflow
            result = result % 243
            self._set_reg('R0', self._int_to_trits(result))
            self._set_reg('R5', self._int_to_trits(carry))
        elif op_int == 2: # SUB R0 = R0 - R1
            a = self._trit_to_int(self._get_reg('R0'))
            b = self._trit_to_int(self._get_reg('R1'))
            result = a - b
            borrow = 1 if result < 0 else 0
            result = result % 243
            self._set_reg('R0', self._int_to_trits(result))
            self._set_reg('R5', self._int_to_trits(borrow))
        elif op_int == 3: # MUL R0 = R0 * R1
            a = self._trit_to_int(self._get_reg('R0'))
            b = self._trit_to_int(self._get_reg('R1'))
            result = (a * b) % 243
            self._set_reg('R0', self._int_to_trits(result))
        elif op_int == 4: # DIV R0 = R0 / R1
            a = self._trit_to_int(self._get_reg('R0'))
            b = self._trit_to_int(self._get_reg('R1'))
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            result = a // b
            self._set_reg('R0', self._int_to_trits(result))
        elif op_int == 5: # MOD R0 = R0 % R1
            a = self._trit_to_int(self._get_reg('R0'))
            b = self._trit_to_int(self._get_reg('R1'))
            if b == 0:
                raise ZeroDivisionError("Modulo by zero")
            result = a % b
            self._set_reg('R0', self._int_to_trits(result))
        elif op_int == 6: # CMP (compare R0, R1)
            a = self._trit_to_int(self._get_reg('R0'))
            b = self._trit_to_int(self._get_reg('R1'))
            if a == b:
                self._set_reg('R5', '00001')  # zero flag
            elif a < b:
                self._set_reg('R5', '00002')  # less flag
            else:
                self._set_reg('R5', '00010')  # greater flag
        elif op_int == 7: # JMP (jump to address)
            addr = self._trit_to_int(operand)
            self._set_reg('R4', self._int_to_trits(addr))
            return  # Skip PC increment
        elif op_int == 8: # JEZ (jump if zero)
            status = self._trit_to_int(self._get_reg('R5'))
            if status == 1:  # zero flag
                addr = self._trit_to_int(operand)
                self._set_reg('R4', self._int_to_trits(addr))
                return
        elif op_int == 9: # JNZ (jump if not zero)
            status = self._trit_to_int(self._get_reg('R5'))
            if status != 1:
                addr = self._trit_to_int(operand)
                self._set_reg('R4', self._int_to_trits(addr))
                return
        elif op_int == 10: # LOAD (R0 = memory[addr])
            addr = self._trit_to_int(operand)
            self._set_reg('R0', self.memory[addr])
        elif op_int == 11: # STORE (memory[addr] = R0)
            addr = self._trit_to_int(operand)
            self.memory[addr] = self._get_reg('R0')
        elif op_int == 12: # PUSH
            self.stack.append(self._get_reg('R0'))
        elif op_int == 13: # POP
            if self.stack:
                self._set_reg('R0', self.stack.pop())
        elif op_int == 14: # CALL (subroutine)
            pc = self._trit_to_int(self._get_reg('R4'))
            self.stack.append(self._int_to_trits(pc + 1))
            addr = self._trit_to_int(operand)
            self._set_reg('R4', self._int_to_trits(addr))
            return
        elif op_int == 15: # RET (return from subroutine)
            if self.stack:
                ret_addr = self.stack.pop()
                self._set_reg('R4', ret_addr)
                return
        elif op_int == 16: # HALT
            self.running = False
            return

        # Increment program counter
        pc = self._trit_to_int(self._get_reg('R4'))
        self._set_reg('R4', self._int_to_trits(pc + 1))

    def run(self, program, start_addr=0):
        """
        Load a program into memory and execute.
        Program is a list of 10-trit instructions (5 opcode + 5 operand).
        """
        # Load program into memory
        for i, instr in enumerate(program):
            self.memory[start_addr + i] = instr

        # Set program counter
        self._set_reg('R4', self._int_to_trits(start_addr))
        self.running = True
        self.instruction_count = 0

        # Execute
        while self.running:
            try:
                instr = self._fetch()
                self._execute(instr)
                self.instruction_count += 1
            except Exception as e:
                print(f"Error at instruction {self.instruction_count}: {e}")
                break

        return self.instruction_count

    def dump_memory(self, start=0, end=100):
        """Dump memory contents for debugging."""
        for i in range(start, min(end, len(self.memory))):
            print(f"{i:04d}: {self.memory[i]}")

    def dump_registers(self):
        """Dump register contents."""
        for reg, val in self.registers.items():
            print(f"{reg}: {val}")


# Example program: add two numbers
def add_program():
    """
    Program: Add R0 and R1, store in R0.
    Opcodes: LOAD (10), ADD (1), HALT (16)
    """
    # LOAD R0, 5   (opcode 10, operand 00005)
    # LOAD R1, 3   (opcode 10, operand 00003)
    # ADD          (opcode 1)
    # HALT         (opcode 16)

    # Program in 10-trit format (5 opcode + 5 operand)
    prog = [
        "00010" + "00005",  # LOAD R0, 5
        "00010" + "00003",  # LOAD R1, 3
        "00001" + "00000",  # ADD
        "00016" + "00000"   # HALT
    ]
    return prog


if __name__ == "__main__":
    # Create VM
    tvm = TVM()

    # Load and run add program
    prog = add_program()
    tvm.memory[0] = "00012"  # initial value for R0 (will be overwritten)

    print("Registers before:")
    tvm.dump_registers()

    tvm.run(prog, start_addr=0)

    print("\nRegisters after:")
    tvm.dump_registers()

    print(f"\nInstructions executed: {tvm.instruction_count}")
