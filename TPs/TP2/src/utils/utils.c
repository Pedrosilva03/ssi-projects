#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include "paths.h"
#include <dirent.h>
#include <string.h>

int initFifos(){
    unlink(PIPE_WRITE);
    unlink(PIPE_READ);

    int pipeWrite = mkfifo(PIPE_WRITE, 0666);
    int pipeRead = mkfifo(PIPE_READ, 0666);

    chmod(PIPE_WRITE, 0666); // TODO: Permissões
    chmod(PIPE_READ, 0666);

    if(pipeWrite == 0 && pipeRead == 0) return 1;
    return 0;
}

void removeDir(char* path){
    DIR* dir = opendir(path);
    struct dirent *entrada;
    struct stat info_arquivo;

    while ((entrada = readdir(dir)) != NULL) {
        // Ignora as entradas '.' e '..'
        if (strcmp(entrada->d_name, ".") != 0 && strcmp(entrada->d_name, "..") != 0) {
            // Constrói o caminho completo do arquivo ou diretório
            char caminho[1000];
            sprintf(caminho, "%s/%s", path, entrada->d_name);

            // Obtém informações sobre o arquivo ou diretório
            if (lstat(caminho, &info_arquivo) != 0) {
                perror("Erro ao obter informações do arquivo");
                exit(EXIT_FAILURE);
            }

            // Se for um diretório, chama a função recursivamente
            if (S_ISDIR(info_arquivo.st_mode)) {
                removeDir(caminho);
            } else { // Se for um arquivo, remove
                if (remove(caminho) != 0) {
                    perror("Erro ao remover o arquivo");
                    exit(EXIT_FAILURE);
                }
            }
        }
    }
    rmdir(path);
}