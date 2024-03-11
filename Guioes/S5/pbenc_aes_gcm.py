import os
import sys
from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key_iv_and_nonce(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations based on your security requirements
        salt=salt,
        length=32 + 16 + 12  # 32 bytes for encryption key, 16 bytes for IV, and 12 bytes for nonce
    )
    key_iv_nonce = kdf.derive(passphrase.encode())
    return key_iv_nonce[:32], key_iv_nonce[32:48], key_iv_nonce[48:]

def encrypt(plaintext, key, iv, nonce):
    cipher = Cipher(algorithms.AES(key), mode=modes.GCM(iv, nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag
    return ciphertext, tag

def decrypt(ciphertext, tag, key, iv, nonce):
    cipher = Cipher(algorithms.AES(key), mode=modes.GCM(iv, nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def main():
    if len(sys.argv) != 2:
        print("Usage: python pbenc_aes_gcm.py <enc|dec>")
        sys.exit(1)

    operation = sys.argv[1].lower()

    if operation not in ["enc", "dec"]:
        print("Invalid operation. Use 'enc' for encryption or 'dec' for decryption.")
        sys.exit(1)

    try:
        passphrase = input("Enter passphrase: ")
        salt = os.urandom(16)

        key, iv, nonce = generate_key_iv_and_nonce(passphrase, salt)

        if operation == "enc":
            plaintext = input("Enter plaintext: ").encode()

            ciphertext, tag = encrypt(plaintext, key, iv, nonce)

            print(f"Salt: {b64encode(salt).decode()}")
            print(f"Ciphertext: {b64encode(ciphertext).decode()}")
            print(f"Tag: {b64encode(tag).decode()}")

        elif operation == "dec":
            salt_input = input("Enter salt: ")
            salt = b64decode(salt_input)

            ciphertext_input = input("Enter ciphertext: ")
            ciphertext = b64decode(ciphertext_input)

            tag_input = input("Enter tag: ")
            tag = b64decode(tag_input)

            decrypted_text = decrypt(ciphertext, tag, key, iv, nonce)

            print(f"Decrypted Text: {decrypted_text.decode()}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
