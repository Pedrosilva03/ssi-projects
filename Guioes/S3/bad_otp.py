import os
import sys
import random

def bad_prng(n):
    """Um gerador de números pseudo-aleatórios INSEGURO."""
    random.seed(random.randbytes(2))
    return random.randbytes(n)

def generate_random_bytes(num_bytes, output_file):
    with open(output_file, 'wb') as file:
        random_bytes = bad_prng(num_bytes)
        file.write(random_bytes)

def encrypt(message_file, key_file):
    with open(message_file, 'rb') as message, open(key_file, 'rb') as key:
        message_data = message.read()
        key_data = key.read()

        if len(message_data) != len(key_data):
            print("Erro: Tamanho da mensagem e da chave não coincidem.")
            return

        cipher_text = bytes(x ^ y for x, y in zip(message_data, key_data))

        output_file = f"{message_file}.enc"
        with open(output_file, 'wb') as output:
            output.write(cipher_text)

def decrypt(ciphertext_file, key_file):
    with open(ciphertext_file, 'rb') as cipher, open(key_file, 'rb') as key:
        cipher_data = cipher.read()
        key_data = key.read()

        if len(cipher_data) != len(key_data):
            print("Erro: Tamanho do criptograma e da chave não coincidem.")
            return

        decrypted_text = bytes(x ^ y for x, y in zip(cipher_data, key_data))

        output_file = f"{ciphertext_file}.dec"
        with open(output_file, 'wb') as output:
            output.write(decrypted_text)

def main(args):
    if len(args) < 2:
        print("Uso: python bad_otp.py <setup|enc|dec> <argumento1> <argumento2>")
        sys.exit(1)

    command = args[1]

    if command == "setup":
        if len(args) != 5:
            print("Uso: python bad_otp.py setup <num_bytes> <output_file>")
            sys.exit(1)
        num_bytes = int(args[3])
        output_file = args[4]
        generate_random_bytes(num_bytes, output_file)
    elif command == "enc":
        if len(args) != 4:
            print("Uso: python bad_otp.py enc <message_file> <key_file>")
            sys.exit(1)
        message_file = args[2]
        key_file = args[3]
        encrypt(message_file, key_file)
    elif command == "dec":
        if len(args) != 4:
            print("Uso: python bad_otp.py dec <ciphertext_file> <key_file>")
            sys.exit(1)
        ciphertext_file = args[2]
        key_file = args[3]
        decrypt(ciphertext_file, key_file)
    else:
        print("Comando inválido. Use 'setup', 'enc' ou 'dec'.")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
