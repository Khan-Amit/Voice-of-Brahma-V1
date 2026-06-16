# tvm.py – Ternary Virtual Machine
# All Rights Reserved ® Seliim Ahmed

class TVM:
    def __init__(self, memory_size=65536):
        self.memory = ['00000'] * memory_size
        self.registers = {f'R{i}': '00000' for i in range(6)}
        self.stack = []
        self.pc = 0
        self.running = True
        self.instructions_executed = 0

    def _trits_to_int(self, trits: str) -> int:
        val = 0
        for ch in trits:
            val = val * 3 + int(ch)
        return val

    def _int_to_trits(self, n: int, length: int = 5) -> str:
        if n == 0:
            return '0' * length
        digits = ''
        while n > 0:
            digits = str(n % 3) + digits
            n //= 3
        return digits.zfill(length)

    def _get_reg(self, name):
        return self.registers[name]

    def _set_reg(self, name, value):
        self.registers[name] = value

    def load_program(self, program: list, start_addr=0):
        for i, instr in enumerate(program):
            self.memory[start_addr + i] = instr
        self.pc = start_addr

    def step(self):
        if not self.running:
            return
        instr = self.memory[self.pc]
        opcode = instr[:5]
        operand = instr[5:]
        op_int = self._trits_to_int(opcode)

        if op_int == 0:   # NOP
            pass
        elif op_int == 1: # ADD
            a = self._trits_to_int(self._get_reg('R0'))
            b = self._trits_to_int(self._get_reg('R1'))
            self._set_reg('R0', self._int_to_trits((a + b) % 243))
        elif op_int == 2: # SUB
            a = self._trits_to_int(self._get_reg('R0'))
            b = self._trits_to_int(self._get_reg('R1'))
            self._set_reg('R0', self._int_to_trits((a - b) % 243))
        elif op_int == 10: # LOAD
            addr = self._trits_to_int(operand)
            self._set_reg('R0', self.memory[addr])
        elif op_int == 11: # STORE
            addr = self._trits_to_int(operand)
            self.memory[addr] = self._get_reg('R0')
        elif op_int == 16: # HALT
            self.running = False
            return

        self.pc += 1
        self.instructions_executed += 1

    def run(self):
        self.running = True
        while self.running:
            self.step()
        return self.instructions_executed

    def dump_registers(self):
        return {k: v for k, v in self.registers.items()}
