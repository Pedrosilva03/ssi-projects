import sys
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def pad(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    return padder.update(data) + padder.finalize()

def unpad(data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def encrypt_file_ctr(input_file, key_file):
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Adiciona padding para garantir que o texto limpo tem um tamanho múltiplo do tamanho do bloco
    plaintext = pad(plaintext)

    with open(key_file, 'rb') as f:
        key = f.read()

    # Gera um vetor de inicialização (nonce) aleatório
    nonce = os.urandom(16)

    # Cria um objeto de cifra AES no modo CTR com a chave e o nonce fornecidos
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    # Cifra o texto limpo
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    output_file = input_file + '.enc'
    with open(output_file, 'wb') as f:
        f.write(nonce + ciphertext)

    print("Arquivo cifrado salvo em", output_file)

def decrypt_file_ctr(input_file, key_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    # Extrai o nonce do início do arquivo
    nonce = data[:16]
    ciphertext = data[16:]

    with open(key_file, 'rb') as f:
        key = f.read()

    # Cria um objeto de cifra AES no modo CTR com a chave e o nonce fornecidos
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decifra o texto cifrado
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove o padding adicionado anteriormente
    decrypted_data = unpad(decrypted_data)

    output_file = input_file[:-4]  # Remove a extensão .enc
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    print("Arquivo decifrado salvo em", output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python cfich_aes_ctr.py <modo> <ficheiro> <chave>")
        sys.exit(1)

    modo = sys.argv[1]
    if modo == "enc":
        if len(sys.argv) != 4:
            print("Uso: python cfich_aes_ctr.py enc <ficheiro> <chave>")
            sys.exit(1)
        encrypt_file_ctr(sys.argv[2], sys.argv[3])
    elif modo == "dec":
        if len(sys.argv) != 4:
            print("Uso: python cfich_aes_ctr.py dec <ficheiro> <chave>")
            sys.exit(1)
        decrypt_file_ctr(sys.argv[2], sys.argv[3])
    else:
        print("Modo não reconhecido. Escolha 'enc' para cifrar ou 'dec' para decifrar.")
        sys.exit(1)
