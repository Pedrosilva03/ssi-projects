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
        i -= 91
        i += 65
    
    while i < 65:
        i = 64 - i
        i = 90 - i
    
    return chr(i)

def cesar(mode, let, string):
    key = ord(let) - 65
    str_compact = preproc(string)
    if mode == 'enc':
        result_string = ''.join(map(lambda x: cifra(x, key), str_compact))
    else:
            result_string = ''.join(map(lambda x: cifra(x, -key), str_compact))
    return result_string

def main(inp):
    print("Faltam argumentos") if len(inp) < 4 else print(cesar(inp[1], inp[2], inp[3]))

if __name__ == "__main__":
    main(sys.argv)