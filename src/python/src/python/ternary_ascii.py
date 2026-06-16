# ternary_ascii.py – 5-trit ASCII codec
# All Rights Reserved ® Seliim Ahmed

def int_to_ternary_5(n: int) -> str:
    if n == 0:
        return '00000'
    digits = ''
    while n > 0:
        digits = str(n % 3) + digits
        n //= 3
    return digits.zfill(5)

# Build lookup tables
ASCII_TO_TERNARY = {}
TERNARY_TO_ASCII = {}

for code in range(128):
    trits = int_to_ternary_5(code)
    char = chr(code)
    ASCII_TO_TERNARY[char] = trits
    ASCII_TO_TERNARY[code] = trits
    TERNARY_TO_ASCII[trits] = char

def text_to_ternary(text: str) -> str:
    return ''.join(ASCII_TO_TERNARY.get(ch, '?????') for ch in text)

def ternary_to_text(ternary_str: str) -> str:
    ternary_str = ternary_str.replace(' ', '').replace('\n', '')
    if len(ternary_str) % 5 != 0:
        raise ValueError('Ternary string length must be multiple of 5')
    result = ''
    for i in range(0, len(ternary_str), 5):
        chunk = ternary_str[i:i+5]
        result += TERNARY_TO_ASCII.get(chunk, '?')
    return result

def format_ternary(ternary_str: str) -> str:
    groups = [ternary_str[i:i+5] for i in range(0, len(ternary_str), 5)]
    return ' '.join(groups)

def text_to_binary(text: str) -> str:
    return ''.join(format(ord(ch), '08b') for ch in text)

def binary_to_text(binary_str: str) -> str:
    if len(binary_str) % 8 != 0:
        raise ValueError('Binary length must be multiple of 8')
    result = ''
    for i in range(0, len(binary_str), 8):
        result += chr(int(binary_str[i:i+8], 2))
    return result

def format_binary(binary_str: str) -> str:
    groups = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ' '.join(groups)
