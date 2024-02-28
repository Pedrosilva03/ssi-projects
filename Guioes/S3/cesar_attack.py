import sys

def preproc(str):
    l = []
    for c in str:
        if c.isalpha():
            l.append(c.upper())
    return "".join(l)

def cifra(str, number):
    i = ord(str)
    i += number

    while i > 90:
        i -= 26

    while i < 65:
        i += 26

    return chr(i)

def cesar(mode, let, string):
    key = ord(let) - 65
    str_compact = preproc(string)
    if mode == "enc":
        result = ''.join(map(lambda x: cifra(x, key), str_compact))
    else:
        result = ''.join(map(lambda x: cifra(x, -key), str_compact))
    return result

def main(ciphertext, *words):
    candidates = []
    for word in words:
        for i in range(26):
            decrypted = cesar("dec", chr(65 + i), ciphertext)
            if word.upper() in decrypted:
                candidates.append((chr(65 + i), decrypted))
                break
    if candidates:
        for candidate in candidates:
            print(candidate[0])
            print(candidate[1])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Faltam argumentos")
    else:
        main(sys.argv[1], *sys.argv[2:])