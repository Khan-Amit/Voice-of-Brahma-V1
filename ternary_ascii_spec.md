# Ternary ASCII Specification (5‑Trit Standard)

## Encoding

Each ASCII character (0–127) is encoded as a 5‑trit ternary number (base‑3).

- Trits: `0, 1, 2`
- Range: `00000₃` to `11122₃` (0–127 decimal)
- Padding: Leading zeros to exactly 5 digits

## Examples

| ASCII | Decimal | Ternary (5‑trit) |
|-------|---------|------------------|
| Space | 32 | 01012 |
| '0'   | 48 | 01210 |
| 'A'   | 65 | 02102 |
| 'a'   | 97 | 10121 |
| 'z'   | 122 | 11112 |

## Extended Characters

For Unicode (up to 4,294,967,295 values), use 20 trits (`3²⁰ = 3.48e9`). The standard 5‑trit table covers the ASCII subset.

## Lookup Tables

- `ASCII_TO_TERNARY`: char → 5‑trit string
- `TERNARY_TO_ASCII`: 5‑trit string → char
