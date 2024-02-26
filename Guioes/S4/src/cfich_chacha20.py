import sys
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

doc_folder = '../doc/'
def generate_key(file_name):
    # Gera uma chave aleatória
    backend = default_backend()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(b"password")  # Senha fixa apenas para fins de exemplo
    # Salva a chave em um arquivo
    with open(doc_folder + file_name, 'wb') as f:
        f.write(key)
    print("Chave gerada e salva em", file_name)

def encrypt_file(input_file, key_file):
    with open(doc_folder + key_file, 'rb') as f:
        key = f.read()
    with open(doc_folder + input_file, 'rb') as f:
        plaintext = f.read()
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    output_file = input_file + '.enc'
    with open(doc_folder + output_file, 'wb') as f:
        f.write(nonce)
        f.write(ciphertext)
    print("Arquivo cifrado salvo em", output_file)

def decrypt_file(input_file, key_file):
    with open(doc_folder + key_file, 'rb') as f:
        key = f.read()
    with open(doc_folder + input_file, 'rb') as f:
        nonce = f.read(16)
        ciphertext = f.read()
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    output_file = input_file[:-4]  # Remove a extensão .enc
    output_file = output_file + '.dec'
    with open(doc_folder + output_file, 'wb') as f:
        f.write(plaintext)
    print("Arquivo decifrado salvo em", output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python cfich_chacha20.py <operacao> [<arquivo> <chave>]")
        sys.exit(1)

    operacao = sys.argv[1]
    if operacao == "setup":
        if len(sys.argv) != 3:
            print("Uso: python cfich_chacha20.py setup <arquivo_chave>")
            sys.exit(1)
        generate_key(sys.argv[2])
    elif operacao == "enc":
        if len(sys.argv) != 4:
            print("Uso: python cfich_chacha20.py enc <arquivo_original> <arquivo_chave>")
            sys.exit(1)
        encrypt_file(sys.argv[2], sys.argv[3])
    elif operacao == "dec":
        if len(sys.argv) != 4:
            print("Uso: python cfich_chacha20.py dec <arquivo_cifrado> <arquivo_chave>")
            sys.exit(1)
        decrypt_file(sys.argv[2], sys.argv[3])
    else:
        print("Operação não reconhecida. Escolha entre 'setup', 'enc' ou 'dec'.")
        sys.exit(1)
