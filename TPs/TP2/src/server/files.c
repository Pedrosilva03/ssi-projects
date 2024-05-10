#include "files.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include "../utils/paths.h"
#include "../utils/utils.h"

int createInbox(char* user){
    char path[BUFSIZ];

    strcpy(path, USER_PATH);
    strcat(path, "/");
    strcat(path, user);

    int status = mkdir(path, S_IRWXU | S_IRGRP | S_IWGRP | S_IXGRP);
    chown(path, -1, atoi(user));
    return status;
}

int addActivation(char* user){
    FILE* f = fopen(ACTIVE_USERS, "a");
    int n = fprintf(f, "%s\n", user);
    fclose(f);

    if(n > 0 && createInbox(user) == 0) return 1;
    return 0;
}

void removeActivation(char* user){
    FILE* f = fopen(ACTIVE_USERS, "r");

    char novaData[BUFSIZ];
    strcpy(novaData, "");
    char linha[12];

    while(fgets(linha, sizeof(linha), f) != NULL){
        if(!(atoi(linha) == atoi(user))){
            strcat(novaData, linha);
        }
    }
    fclose(f);

    f = fopen(ACTIVE_USERS, "w");
    fprintf(f, "%s", novaData);
    fclose(f);

    char path[BUFSIZ];

    strcpy(path, USER_PATH);
    strcat(path, "/");
    strcat(path, user);

    removeDir(path);
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

void addMensagem(char* rem, char* dest, char* msg){
    char path[BUFSIZ];
    char aux[100];

    if(atoi(dest) > 0 ) strcpy(path, USER_PATH);
    else strcpy(path, GROUP_PATH);

    snprintf(aux, sizeof(aux), "/%s/mensagem_%d.txt", dest, rand() % MAX_MSG_ID);
    strcat(path, aux);

    FILE* mensagem = fopen(path, "a");
    fprintf(mensagem, "%s\n", rem);
    fprintf(mensagem, "%s\n", msg);
    fprintf(mensagem, "%ld\n", strlen(msg));
    fclose(mensagem);
}

void removeMensagem(char* currentStr, char* id){
    char pathComparison[BUFSIZ];
    snprintf(pathComparison, sizeof(pathComparison), "mensagem_%s.txt", id);

    char path[BUFSIZ];
    strcpy(path, USER_PATH);
    strcat(path, "/");
    strcat(path, currentStr);

    DIR* inbox = opendir(path);
    struct dirent *entrada;

    while((entrada = readdir(inbox)) != NULL){
        if(strcmp(entrada->d_name, pathComparison) == 0){
            strcat(path, "/");
            strcat(path, entrada->d_name);
            remove(path);
            break;
        }
    }

    closedir(inbox);
}