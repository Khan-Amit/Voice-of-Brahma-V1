# ternary_ascii.py
# Ternary ASCII codec - 5-trit representation

def _to_ternary_5(n):
    """Convert integer 0..242 to 5-trit string."""
    if n == 0:
        return "00000"
    digits = []
    while n:
        digits.append(str(n % 3))
        n //= 3
    return ''.join(reversed(digits)).zfill(5)

# Build lookup tables
ASCII_TO_TERNARY = {}
TERNARY_TO_ASCII = {}
for code in range(128):
    ternary = _to_ternary_5(code)
    char = chr(code)
    ASCII_TO_TERNARY[char] = ternary
    ASCII_TO_TERNARY[code] = ternary
    TERNARY_TO_ASCII[ternary] = char

def text_to_ternary(text):
    return ''.join(ASCII_TO_TERNARY[ch] for ch in text)

def ternary_to_text(ternary_str):
    if len(ternary_str) % 5 != 0:
        raise ValueError("Ternary string length must be multiple of 5")
    return ''.join(TERNARY_TO_ASCII[ternary_str[i:i+5]] for i in range(0, len(ternary_str), 5))

def bytes_to_ternary(data):
    return text_to_ternary(data.decode('ascii', errors='replace'))

def ternary_to_bytes(ternary_str):
    return ternary_to_text(ternary_str).encode('ascii')
