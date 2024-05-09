#include "files.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "../utils/paths.h"

int addActivation(char* user){
    FILE* f = fopen(ACTIVE_USERS, "a");
    int n = fprintf(f, "%s\n", user);
    fclose(f);
    if(n > 0) return 1;
    return 0;
}

int checkActivation(char* user){
    FILE *file;
    char line[50];

    // Abre o ficheiro para leitura
    file = fopen(ACTIVE_USERS, "r");
    if (file == NULL) {
        printf("Erro ao abrir o ficheiro.\n");
        return 0; // Retorna 0 indicando que a string não foi encontrada
    }

    // Lê cada linha do ficheiro e verifica se contém a string alvo
    while (fgets(line, sizeof(line), file) != NULL) {
        // Remove o carácter de nova linha do final da linha
        line[strcspn(line, "\n")] = '\0';

        // Verifica se a linha contém a string alvo
        if (strcmp(line, user) == 0) {
            // Fecha o ficheiro e retorna 1 indicando que a string foi encontrada
            fclose(file);
            return 1;
        }
    }

    // Fecha o ficheiro e retorna 0 indicando que a string não foi encontrada
    fclose(file);
    return 0;
}