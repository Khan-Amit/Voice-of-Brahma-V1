# Ternary Virtual Machine (TVM) Instruction Set

## Registers

| Register | Purpose |
|----------|---------|
| R0       | Accumulator |
| R1       | General purpose |
| R2       | General purpose |
| R3       | Stack pointer |
| R4       | Program counter |
| R5       | Status register (carry, zero, etc.) |

## Memory

- 64K ternary words (each word = 5 trits = 1 ASCII character)
- Addressable by 5‑trit addresses

## Instruction Format

Each instruction is a 5‑trit opcode followed by 0–3 operands.

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 00000  | NOP      | No operation |
| 00001  | ADD      | R0 = R0 + R1 |
| 00002  | SUB      | R0 = R0 - R1 |
| 00003  | MUL      | R0 = R0 * R1 |
| 00004  | DIV      | R0 = R0 / R1 |
| 00005  | MOD      | R0 = R0 % R1 |
| 00006  | CMP      | Compare R0, R1 |
| 00007  | JMP      | Jump to address |
| 00008  | JEZ      | Jump if zero |
| 00009  | JNZ      | Jump if not zero |
| 00010  | LOAD     | R0 = memory[addr] |
| 00011  | STORE    | memory[addr] = R0 |
| 00012  | PUSH     | Push R0 onto stack |
| 00013  | POP      | Pop into R0 |
| 00014  | CALL     | Call subroutine |
| 00015  | RET      | Return from subroutine |
| 00016  | HALT     | Stop execution |

## Ternary Arithmetic

- Addition: Ternary full adder (carry = 1 when sum ≥ 3)
- Subtraction: Ternary borrow (borrow = 1 when minuend < subtrahend)
- Multiplication: Ternary shift & add
- Division: Ternary long division

## Example Program
