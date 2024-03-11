import os
import sys
from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization

def generate_key_and_nonce(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations based on your security requirements
        salt=salt,
        length=32 + 12  # 32 bytes for encryption key and 12 bytes for nonce
    )
    key_nonce = kdf.derive(passphrase.encode())
    return key_nonce[:32], key_nonce[32:]

def encrypt(plaintext, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def main():
    if len(sys.argv) != 2:
        print("Usage: python pbenc_chacha20_poly1305.py <enc|dec>")
        sys.exit(1)

    operation = sys.argv[1].lower()

    if operation not in ["enc", "dec"]:
        print("Invalid operation. Use 'enc' for encryption or 'dec' for decryption.")
        sys.exit(1)

    try:
        passphrase = input("Enter passphrase: ")
        salt = os.urandom(16)

        key, nonce = generate_key_and_nonce(passphrase, salt)

        if operation == "enc":
            plaintext = input("Enter plaintext: ").encode()

            ciphertext = encrypt(plaintext, key, nonce)

            print(f"Salt: {b64encode(salt).decode()}")
            print(f"Ciphertext: {b64encode(ciphertext).decode()}")

        elif operation == "dec":
            salt_input = input("Enter salt: ")
            salt = b64decode(salt_input)

            ciphertext_input = input("Enter ciphertext: ")
            ciphertext = b64decode(ciphertext_input)

            decrypted_text = decrypt(ciphertext, key, nonce)

            print(f"Decrypted Text: {decrypted_text.decode()}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
