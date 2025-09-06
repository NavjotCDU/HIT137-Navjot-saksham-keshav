from __future__ import annotations

def _shift_within_half(ch: str, base: str, span: int, delta: int) -> str:
    
    idx = ord(ch) - ord(base)
    new_idx = (idx + delta) % span
    return chr(ord(base) + new_idx)

def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    if 'a' <= ch <= 'm':
        return _shift_within_half(ch, 'a', 13, shift1 * shift2)
    if 'n' <= ch <= 'z':  
        return _shift_within_half(ch, 'n', 13, -(shift1 + shift2))
    if 'A' <= ch <= 'M':  
        return _shift_within_half(ch, 'A', 13, -shift1)
    if 'N' <= ch <= 'Z':  
        return _shift_within_half(ch, 'N', 13, shift2 * shift2)
    return ch  

def decrypt_char(ch: str, shift1: int, shift2: int) -> str:
    if 'a' <= ch <= 'm':
        return _shift_within_half(ch, 'a', 13, -(shift1 * shift2))
    if 'n' <= ch <= 'z':
        return _shift_within_half(ch, 'n', 13, +(shift1 + shift2))
    if 'A' <= ch <= 'M':
        return _shift_within_half(ch, 'A', 13, +shift1)
    if 'N' <= ch <= 'Z':
        return _shift_within_half(ch, 'N', 13, -(shift2 * shift2))
    return ch

def encrypt_file(input_file: str, output_file: str, shift1: int, shift2: int) -> None:
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    encrypted = ''.join(encrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(encrypted)

def decrypt_file(input_file: str, output_file: str, shift1: int, shift2: int) -> None:
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    decrypted = ''.join(decrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(decrypted)

def verify_files(file1: str, file2: str) -> bool:
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()

def main() -> None:
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))
    encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2)
    decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)
    if verify_files("raw_text.txt", "decrypted_text.txt"):
        print("Decryption successful! Files match.")
    else:
        print("Decryption failed. Files do not match.")

if __name__ == "__main__":
    main()
