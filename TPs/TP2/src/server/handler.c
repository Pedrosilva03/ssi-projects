#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "files.h"
#include "../utils/paths.h"

void handle_command(char *request){
    int fd;

    char* command = strtok(request, "\n");
    if(strcmp(command, "checkUserActivation") == 0){
        char* user = strtok(NULL, "\n");
        int status = checkActivation(user);
        char response[4];
        sprintf(response, "%d\n", status);
        fd = open(PIPE_WRITE, O_WRONLY);
        write(fd, response, strlen(response));
        close(fd);
    }
    else if(strcmp(command, "ativar") == 0){
        char* user = strtok(NULL, "\n");
        int status = addActivation(user);
        char response[4];
        sprintf(response, "%d\n", status);
        fd = open(PIPE_WRITE, O_WRONLY);
        write(fd, response, strlen(response));
        close(fd);
    }
    else if(strcmp(command, "desativar") == 0){
        char* user = strtok(NULL, "\n");
        removeActivation(user);
    }
    else if(strcmp(command, "enviar") == 0){
        char* rem = strtok(NULL, "\n");
        char* dest = strtok(NULL, "\n");
        char* mensagem = strtok(NULL, "\n");

        addMensagem(rem, dest, mensagem);
    }
    else if(strcmp(command, "remove") == 0){
        char* rem = strtok(NULL, "\n");
        char* mid = strtok(NULL, "\n");

        removeMensagem(rem, mid);   
    }
}