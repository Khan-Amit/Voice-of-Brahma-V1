# demo.py – Full demonstration
# All Rights Reserved ® Seliim Ahmed

from ternary_ascii import text_to_ternary, ternary_to_text, format_ternary
from translator import enigma_transform
from tvm import TVM
from scalePRT_calculator import compute_scalePRT

def main():
    print("=" * 60)
    print("Voice-of-Brahma-V1 Demo")
    print("=" * 60)

    # 1. ASCII → Ternary
    text = "Hello, World!"
    print(f"\n1. Text: {text}")
    ternary = text_to_ternary(text)
    print(f"   Ternary (5-trit): {format_ternary(ternary)}")

    # 2. Enigma
    print("\n2. Enigma Transform")
    encrypted = enigma_transform(ternary)
    print(f"   Encrypted: {format_ternary(encrypted)}")

    # 3. TVM
    print("\n3. TVM: Add 5 + 3")
    prog = [
        "00010" + "00005",  # LOAD R0, 5
        "00010" + "00003",  # LOAD R1, 3
        "00001" + "00000",  # ADD
        "00016" + "00000"   # HALT
    ]
    tvm = TVM()
    tvm.load_program(prog, 0)
    tvm.run()
    print(f"   R0 = {tvm.registers['R0']} (dec: {int(tvm.registers['R0'], 3)})")

    # 4. scalePRT
    print("\n4. scalePRT")
    result = compute_scalePRT(41700, 300)
    print(f"   scalePRT = {result['scalePRT_m']:.4e} m")
    print(f"   Ratio to Landauer: {result['ratio_to_landauer']:.4e}")

    print("\n" + "=" * 60)
    print("Demo complete.")

if __name__ == "__main__":
    main()
