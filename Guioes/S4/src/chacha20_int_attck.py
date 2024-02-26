import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

doc_folder = '../doc/'
def manipulate_ciphertext(file_name, position, original_text, new_text):
    with open(doc_folder + file_name, 'rb') as f:
        ciphertext = f.read()

    # Determina o tamanho do nonce e do contador baseado no tamanho do bloco do algoritmo
    nonce_size = ciphertext[:16]
    counter_size = ciphertext[16:]

    # Divide o texto cifrado em nonce, contador e o restante do texto
    nonce = ciphertext[:nonce_size]
    counter = ciphertext[nonce_size:nonce_size+counter_size]
    encrypted_data = ciphertext[nonce_size+counter_size:]

    # Decifra o texto original na posição especificada
    cipher = Cipher(algorithms.ChaCha20(os.urandom(32), nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data)

    # Substitui o texto original pelo novo texto na posição especificada
    manipulated_data = decrypted_data[:position] + new_text.encode() + decrypted_data[position+len(new_text):]

    # Cifra novamente o texto manipulado
    cipher = Cipher(algorithms.ChaCha20(os.urandom(32), nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    manipulated_encrypted_data = encryptor.update(manipulated_data)

    # Escreve o novo texto cifrado no arquivo com a extensão .attck
    output_file = file_name + '.attck'
    with open(doc_folder + output_file, 'wb') as f:
        f.write(nonce + counter + manipulated_encrypted_data)

    print("Texto cifrado manipulado salvo em", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python chacha20_int_attck.py <fctxt> <pos> <ptxtAtPos> <newPtxtAtPos>")
        sys.exit(1)

    file_name = sys.argv[1]
    position = int(sys.argv[2])
    original_text = sys.argv[3]
    new_text = sys.argv[4]

    manipulate_ciphertext(file_name, position, original_text, new_text)
