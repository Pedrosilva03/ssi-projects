import sys

def preproc(str):
    l = []
    for c in str:
        if c.isalpha():
            l.append(c.upper())
    return "".join(l)

def vigenere_decrypt(ciphertext, key):
    plaintext = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_index = i % key_length
            shift = ord(key[key_index]) - 65
            if char.isupper():
                plaintext += chr(((ord(char) - 65 - shift) % 26) + 65)
            else:
                plaintext += chr(((ord(char) - 97 - shift) % 26) + 97)
        else:
            plaintext += char
    return plaintext

def calculate_score(text):
    letter_frequency = {
        'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57, 'F': 1.02,
        'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40, 'K': 0.02, 'L': 2.78,
        'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 'Q': 1.20, 'R': 6.53,
        'S': 7.81, 'T': 4.34, 'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21,
        'Y': 0.01, 'Z': 0.47
    }
    score = sum(letter_frequency.get(char, 0) for char in text.upper())
    return score

def vigenere_attack(key_length, ciphertext, words):
    ciphertext = preproc(ciphertext)
    best_score = float('-inf')
    best_plaintext = ''
    frequent_letters = "AEOSRINDMUTCLPVGHQBFZJXKWY"
    for i in range(26 ** key_length):
        key = ''
        num = i
        for _ in range(key_length):
            key = frequent_letters[num % len(frequent_letters)] + key
            num //= len(frequent_letters)
        plaintext = vigenere_decrypt(ciphertext, key)
        score = calculate_score(plaintext)
        if any(word in plaintext for word in words):
            score = calculate_score(plaintext)
            if score > best_score:
                best_score = score
                best_plaintext = plaintext
                best_key = key
    print(best_key)
    print(best_plaintext)

def main(args):
    if len(args) < 4:
        print("Faltam argumentos")
    else:
        key_length = int(args[1])
        ciphertext = args[2]
        words = args[3:]
        vigenere_attack(key_length, ciphertext, words)

if __name__ == "__main__":
    main(sys.argv)