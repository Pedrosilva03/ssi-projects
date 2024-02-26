import sys

def preproc(str):
    l = []
    for c in str:
        if c.isalpha():
            l.append(c.upper())
    return "".join(l)

def encode(str, number):
    i = ord(str)
    i += number
    
    while i > 90:
       i -= 91
       i += 65
    
    while i < 65:
        i = 64 - i
        i = 90 - i
        
    return chr(i)


def vigenere(mode, let, str):
    
    str_code = preproc(str)
    result_string = ""
    i = -1

    code = []
    for char in let:
        number = ord(char) - 65
        code.append(number)

    for char in str_code:
        if mode == 'enc':
            if i == len(code) - 1:
                i = 0
                result_string = result_string + encode(char, code[i])
            else:
                i += 1
                result_string = result_string + encode(char, code[i])
    
        else:
            if i == len(code) - 1:
                i = 0
                result_string = result_string + encode(char, -code[i])
            else:
                i += 1
                result_string = result_string + encode(char, -code[i])

    return result_string

def main(inp):
    print("Faltam argumentos") if len(inp) < 4 else print(vigenere(inp[1], inp[2], inp[3]))

if __name__ == "__main__":
    main(sys.argv)
