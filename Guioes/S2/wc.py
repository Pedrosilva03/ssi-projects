import sys
import unicodedata


def count_lines_words_carc(path):
    linhas = 0
    palavras = 0
    caracteres = 0

    try:
        with open(path, 'r') as arquivo:
            for linha in arquivo:
                linhas += linha.count('\n')
                tokens = linha.split()
                palavras += len(tokens)
                linha_normalizada = unicodedata.normalize('NFD', linha)
                caracteres += len(linha_normalizada)
        
        return linhas, palavras, caracteres

    except FileNotFoundError:
        print(f"Erro: O arquivo {path} não foi encontrado.")
        return 0, 0, 0

def main(inp):
    if len(inp) != 2:
        print("Uso: python script.py nome_do_arquivo")
        return
    
    linhas, palavras, caracteres = count_lines_words_carc(inp[1])
    if(linhas != 0 or palavras != 0 or caracteres != 0):
        print(f'\t{linhas}\t{palavras}\t{caracteres}')

# Se for chamada como script...
if __name__ == "__main__":
    main(sys.argv)
