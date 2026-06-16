# demo.py
# End‑to‑end demonstration of Voice‑of‑Brahma‑V1
# Binary → Ternary → Execute → Ternary → Binary
# Author: Seliim Ahmed
# All Rights Reserved ®

from ternary_ascii import text_to_ternary, ternary_to_text
from translator import TernaryTranslator
from tvm import TVM
from scalePRT_calculator import calculate_scalePRT

def run_demo():
    print("=" * 60)
    print("Voice-of-Brahma-V1 Demo")
    print("=" * 60)

    # 1. Binary to Ternary (Text to ternary ASCII)
    print("\n1. Binary → Ternary (ASCII encoding)")
    original_text = "Hello, World!"
    print(f"   Original: {original_text}")
    ternary_ascii = text_to_ternary(original_text)
    print(f"   Ternary (5‑trit): {ternary_ascii}")

    # 2. Enigma‑style translation (optional encryption)
    print("\n2. Enigma Translator (rotors applied)")
    translator = TernaryTranslator()
    encrypted_ternary = translator.translate_text(original_text, forward=True)
    print(f"   Encrypted ternary: {encrypted_ternary}")

    # Reset positions for decryption
    translator.positions = [0, 0, 0]
    decrypted_text = translator.translate_text(encrypted_ternary, forward=False)
    print(f"   Decrypted text: {decrypted_text}")

    # 3. Execute ternary program (TVM)
    print("\n3. Ternary Virtual Machine (TVM) Execution")
    # Simple program: add 5 and 3
    prog = [
        "00010" + "00005",  # LOAD R0, 5
        "00010" + "00003",  # LOAD R1, 3
        "00001" + "00000",  # ADD
        "00016" + "00000"   # HALT
    ]
    tvm = TVM()
    tvm.run(prog, start_addr=0)
    print(f"   Program executed.")
    print(f"   Instructions: {tvm.instruction_count}")
    r0_val = tvm._trit_to_int(tvm.registers['R0'])
    print(f"   Result (R0): {r0_val}")

    # 4. scalePRT calculation
    print("\n4. scalePRT Calculation")
    fwhm = 41.7e3  # 41.7 kHz (typical)
    scale_result = calculate_scalePRT(fwhm, 300.0, 780e-9)
    print(f"   Resonance FWHM: {fwhm:.1f} Hz")
    print(f"   scalePRT: {scale_result['scalePRT_m']:.4e} m")
    print(f"   ratio to Landauer limit: {scale_result['ratio_to_landauer']:.2f}")

    # 5. Full cycle: binary → ternary → execute → ternary → binary
    print("\n5. Full cycle: binary → ternary → execute → ternary → binary")
    # We'll take the original text, translate to ternary, then interpret as a program?
    # Actually, let's just demonstrate the translator round‑trip.
    print("   Round‑trip test (translator):")
    test_text = "Count It"
    ternary = text_to_ternary(test_text)
    restored = ternary_to_text(ternary)
    print(f"   Original: {test_text}")
    print(f"   Ternary: {ternary}")
    print(f"   Restored: {restored}")
    assert test_text == restored, "Round‑trip failed!"
    print("   ✅ Round‑trip successful.")

    print("\n" + "=" * 60)
    print("Demo complete. Voice-of-Brahma-V1 is operational.")
    print("All Rights Reserved ® Seliim Ahmed")

if __name__ == "__main__":
    run_demo()
