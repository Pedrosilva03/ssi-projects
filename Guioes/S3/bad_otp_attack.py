import sys
from itertools import cycle
import random

def bad_prng(n):
    """Um gerador de números pseudo-aleatórios INSEGURO."""
    random.seed(random.randbytes(2))
    return random.randbytes(n)

def decrypt(ciphertext, key):
    decrypted_text = bytes(x ^ y for x, y in zip(ciphertext, cycle(key)))
    return decrypted_text.decode()

def main(args):
    if len(args) < 4:
        print("Uso: python bad_otp_attack.py <ciphertext_file> <word1> <word2> ...")
        sys.exit(1)

    ciphertext_file = args[1]
    words_to_find = set(args[2:])

    with open(ciphertext_file, 'rb') as cipher:
        cipher_data = cipher.read()

    # Tentativa de descriptografar usando palavras conhecidas
    for word in words_to_find:
        key_candidate = bytes(x ^ ord(y) for x, y in zip(cipher_data, cycle(word)))
        decrypted_text = decrypt(cipher_data, key_candidate)

        # Verifica se a palavra está presente no texto decifrado
        if word in decrypted_text:
            print("Texto-limpo recuperado:")
            print(decrypted_text)
            sys.exit(0)

    print("Texto-limpo não recuperado. Tente com outras palavras.")
    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
