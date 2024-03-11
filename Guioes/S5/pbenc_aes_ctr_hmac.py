import os
import sys
from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key_iv_and_mac_key(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations based on your security requirements
        salt=salt,
        length=32 + 16 + 32  # 32 bytes for encryption key, 16 bytes for IV, and 32 bytes for MAC key
    )
    key_iv_mac_key = kdf.derive(passphrase.encode())
    return key_iv_mac_key[:32], key_iv_mac_key[32:48], key_iv_mac_key[48:]

def encrypt_then_mac(plaintext, key, iv, mac_key):
    cipher = Cipher(algorithms.AES(key), mode=modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    tag = h.finalize()

    return ciphertext, tag

def verify_mac(ciphertext, tag, key, iv, mac_key):
    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    h.verify(tag)

def main():
    if len(sys.argv) != 2:
        print("Usage: python pbenc_aes_ctr_hmac.py <enc|dec>")
        sys.exit(1)

    operation = sys.argv[1].lower()

    if operation not in ["enc", "dec"]:
        print("Invalid operation. Use 'enc' for encryption or 'dec' for decryption.")
        sys.exit(1)

    try:
        passphrase = input("Enter passphrase: ")
        salt = os.urandom(16)

        key, iv, mac_key = generate_key_iv_and_mac_key(passphrase, salt)

        if operation == "enc":
            plaintext = input("Enter plaintext: ").encode()

            ciphertext, tag = encrypt_then_mac(plaintext, key, iv, mac_key)

            print(f"Salt: {b64encode(salt).decode()}")
            print(f"Ciphertext: {b64encode(ciphertext).decode()}")
            print(f"MAC Tag: {b64encode(tag).decode()}")

        elif operation == "dec":
            salt_input = input("Enter salt: ")
            salt = b64decode(salt_input)

            ciphertext_input = input("Enter ciphertext: ")
            ciphertext = b64decode(ciphertext_input)

            tag_input = input("Enter MAC Tag: ")
            tag = b64decode(tag_input)

            verify_mac(ciphertext, tag, key, iv, mac_key)

            cipher = Cipher(algorithms.AES(key), mode=modes.CTR(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            print(f"Decrypted Text: {plaintext.decode()}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
