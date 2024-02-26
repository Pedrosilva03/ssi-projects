import os
import sys


def generate_key(n_by, file):
    byt = os.urandom(int(n_by))
    with open(file, 'wb') as arquivo:
        arquivo.write(byt)

def enc(path_message, path_key):
    
    with open(path_key, 'rb') as arquivo_key:
        key_bytes = arquivo_key.readline()
    
    with open(path_message, 'r') as arquivo_message:
        message = arquivo_message.readline()
    
    print(message)
    
    try:
        message_bytes = message.encode('utf-8')
    except UnicodeEncodeError as e:
        print(f"Erro de codificação: {e}")
        sys.exit(1)

    resultado_bytes = bytes(a ^ b for a, b in zip(key_bytes, message_bytes))
    path_resultado = path_message + ".enc"

    with open(path_resultado, 'wb') as arquivo_resultado:
        arquivo_resultado.write(resultado_bytes)

def dec(path_message, path_key):
    with open(path_key, 'rb') as arquivo_key:
        key_bytes = arquivo_key.readline()
    
    with open(path_message, 'rb') as arquivo_message:
        message_bytes = arquivo_message.readline()
    
    resultado_bytes = bytes(a ^ b for a, b in zip(key_bytes, message_bytes))
    path_resultado = path_message + ".dec"
    resultado = resultado_bytes.decode('utf-8')
    with open(path_resultado, 'w') as arquivo_resultado:
        arquivo_resultado.write(resultado)


def main(inp):
    print(inp)
    if inp[1] == "setup":
        generate_key(inp[2], inp[3])
    if inp[1] == "enc":
        enc(inp[2], inp[3])
    if inp[1] == "dec":
        dec(inp[2], inp[3])



if __name__ == "__main__":
    main(sys.argv)

