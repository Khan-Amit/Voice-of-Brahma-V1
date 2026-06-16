# translator.py
# Enigma‑style Binary ↔ Ternary Translator
# Part of Voice-of-Brahma-V1
# Author: Seliim Ahmed
# All Rights Reserved ®

from ternary_ascii import text_to_ternary, ternary_to_text
import copy

class TernaryTranslator:
    """
    Enigma-style rotor machine for binary ↔ ternary translation.
    Uses 3 rotors (each a permutation of [-1, 0, +1]) and a reflector.
    Rotor positions advance after each ternary symbol.
    """

    def __init__(self, rotor_wirings=None, reflector=None, rotor_positions=None):
        """
        rotor_wirings: list of 3 lists, each a permutation of [-1, 0, +1]
        reflector: dict mapping -1↔+1, 0↔0
        rotor_positions: list of 3 integers (starting offsets)
        """
        if rotor_wirings is None:
            # Default rotors (permutations)
            self.rotors = [
                [-1, 0, +1],   # Rotor I (identity)
                [0, +1, -1],   # Rotor II (shift left)
                [+1, -1, 0]    # Rotor III (shift right)
            ]
        else:
            self.rotors = rotor_wirings

        if reflector is None:
            self.reflector = {-1: +1, 0: 0, +1: -1}
        else:
            self.reflector = reflector

        if rotor_positions is None:
            self.positions = [0, 0, 0]
        else:
            self.positions = rotor_positions

    def _apply_rotor(self, value, rotor_idx, forward=True):
        """Apply a single rotor permutation (forward or inverse)."""
        rotor = self.rotors[rotor_idx]
        if forward:
            # map input value to output via rotor
            # rotor is a list where index is input, value is output
            # but input values are -1,0,1; we need to map to indices 0,1,2
            idx = value + 1  # -1→0, 0→1, 1→2
            return rotor[idx]
        else:
            # inverse: find index where rotor[idx] == value
            idx = rotor.index(value)
            return idx - 1  # map back to -1,0,1

    def _advance_rotors(self):
        """Advance rotors like an odometer."""
        self.positions[0] = (self.positions[0] + 1) % 3
        if self.positions[0] == 0:
            self.positions[1] = (self.positions[1] + 1) % 3
            if self.positions[1] == 0:
                self.positions[2] = (self.positions[2] + 1) % 3

    def _apply_shift(self, value, shift):
        """Shift a ternary value (-1,0,1) by shift (0,1,2) modulo 3."""
        # convert -1,0,1 → 0,1,2
        idx = value + 1
        idx = (idx + shift) % 3
        return idx - 1

    def translate_symbol(self, symbol, forward=True):
        """
        Translate a single ternary symbol (-1,0,1) through the rotors.
        If forward=True: binary→ternary encoding; else ternary→binary decoding.
        Actually, since Enigma is reciprocal, forward/backward is symmetric.
        """
        # Apply rotor positions (shifts)
        val = self._apply_shift(symbol, self.positions[0])
        # Pass through rotors (forward or inverse)
        # For simplicity we use same function for both since we want it to be symmetric
        # But we can implement proper forward/backward if needed.
        # We'll do: through rotor 1, rotor 2, rotor 3, reflector, rotor 3, rotor 2, rotor 1
        # This is the Enigma path.
        # However, since our rotors are small permutations, we can just apply them in sequence.

        # For simplicity, we'll apply each rotor in forward direction, then reflector, then rotors reversed.
        # We'll assume forward=True means encrypt (binary->ternary) and forward=False means decrypt (ternary->binary)
        # But because Enigma is symmetric, we can just use the same function.

        # Let's implement a proper symmetric cipher:
        # 1. Apply rotor 0 forward
        val = self._apply_rotor(val, 0, forward=True)
        # 2. Apply rotor 1 forward
        val = self._apply_rotor(val, 1, forward=True)
        # 3. Apply rotor 2 forward
        val = self._apply_rotor(val, 2, forward=True)
        # 4. Apply reflector
        val = self.reflector[val]
        # 5. Apply rotor 2 inverse
        val = self._apply_rotor(val, 2, forward=False)
        # 6. Apply rotor 1 inverse
        val = self._apply_rotor(val, 1, forward=False)
        # 7. Apply rotor 0 inverse
        val = self._apply_rotor(val, 0, forward=False)

        return val

    def translate_text(self, text, forward=True):
        """
        Translate a text string (ASCII) to ternary or ternary to text.
        If forward=True: binary (text) → ternary.
        If forward=False: ternary (text) → binary.
        """
        if forward:
            # Convert text to ternary ASCII first (base encoding)
            ternary_str = text_to_ternary(text)
            # Then apply rotor translation symbol by symbol
            # Convert ternary string to list of ints (-1,0,1)
            symbols = [int(ch)-1 for ch in ternary_str]  # '0'→-1, '1'→0, '2'→1
            translated = []
            for sym in symbols:
                translated.append(self.translate_symbol(sym, forward=True))
                self._advance_rotors()
            # Convert back to ternary string
            translated_ternary = ''.join(str(s+1) for s in translated)  # -1→0, 0→1, 1→2
            return translated_ternary
        else:
            # Decrypt: ternary string → text
            symbols = [int(ch)-1 for ch in text]  # '0'→-1, '1'→0, '2'→1
            decrypted = []
            for sym in symbols:
                decrypted.append(self.translate_symbol(sym, forward=False))
                self._advance_rotors()
            decrypted_ternary = ''.join(str(s+1) for s in decrypted)
            # Convert back to ASCII
            return ternary_to_text(decrypted_ternary)

# Example usage
if __name__ == "__main__":
    translator = TernaryTranslator()
    original = "Hello, World!"
    print("Original:", original)
    # Encrypt (binary → ternary)
    encrypted = translator.translate_text(original, forward=True)
    print("Encrypted ternary:", encrypted)
    # Reset positions for decryption
    translator.positions = [0,0,0]
    decrypted = translator.translate_text(encrypted, forward=False)
    print("Decrypted:", decrypted)
