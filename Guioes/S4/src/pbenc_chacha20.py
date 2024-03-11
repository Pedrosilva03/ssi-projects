import os
import sys
from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key_and_iv(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations based on your security requirements
        salt=salt,
        length=32 + 16  # 32 bytes for the key and 16 bytes for the IV
    )
    key_and_iv = kdf.derive(passphrase.encode())
    return key_and_iv[:32], key_and_iv[32:]

def encrypt(plaintext, key, iv):
    cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def main():
    if len(sys.argv) != 2:
        print("Usage: python cfich_chacha20.py <enc|dec>")
        sys.exit(1)

    operation = sys.argv[1].lower()

    if operation not in ["enc", "dec"]:
        print("Invalid operation. Use 'enc' for encryption or 'dec' for decryption.")
        sys.exit(1)

    try:
        passphrase = input("Enter passphrase: ")
        salt = os.urandom(16)

        key, iv = generate_key_and_iv(passphrase, salt)

        if operation == "enc":
            plaintext = input("Enter plaintext: ").encode()
            ciphertext = encrypt(plaintext, key, iv)
            print(f"Salt: {b64encode(salt).decode()}")
            print(f"Ciphertext: {b64encode(ciphertext).decode()}")

        elif operation == "dec":
            salt_input = input("Enter salt: ")
            salt = b64decode(salt_input)
            ciphertext_input = input("Enter ciphertext: ")
            ciphertext = b64decode(ciphertext_input)

            key, iv = generate_key_and_iv(passphrase, salt)

            plaintext = decrypt(ciphertext, key, iv)
            print(f"Decrypted Text: {plaintext.decode()}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
