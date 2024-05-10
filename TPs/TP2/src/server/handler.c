#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "files.h"
#include "../utils/paths.h"
#include "groups.h"

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
    else if(strcmp(command, "grupoc") == 0){
        char* uid = strtok(NULL, "\n");
        char* nome = strtok(NULL, "\n");

        int status = criarGrupo(uid, nome);

        char response[4];
        sprintf(response, "%d\n", status);
        fd = open(PIPE_WRITE, O_WRONLY);
        write(fd, response, strlen(response));
        close(fd);
    }
    else if(strcmp(command, "grupoadd") == 0){
        char* uid = strtok(NULL, "\n");
        char* nome = strtok(NULL, "\n");
        char *newUID = strtok(NULL, "\n");
        int status = 1;
        if(verifyAdmin(nome, uid) == 1){
            status = addMember(nome, newUID);
        }
        char response[4];
        sprintf(response, "%d\n", status);
        fd = open(PIPE_WRITE, O_WRONLY);
        write(fd, response, strlen(response));
        close(fd);
    }
    else if(strcmp(command, "gruporem") == 0){
        char* uid = strtok(NULL, "\n");
        char* nome = strtok(NULL, "\n");
        char *newUID = strtok(NULL, "\n");
        int status = 1;
        if(verifyAdmin(nome, uid) == 1){
            status = remMember(nome, newUID);
        }
        char response[4];
        sprintf(response, "%d\n", status);
        fd = open(PIPE_WRITE, O_WRONLY);
        write(fd, response, strlen(response));
        close(fd);
    }
    else if(strcmp(command, "grupodel") == 0){
        char* uid = strtok(NULL, "\n");
        char* nome = strtok(NULL, "\n");
        int status = 1;
        if(verifyAdmin(nome, uid) == 1){
            status = delGrupo(nome, uid);
        }
        char response[4];
        sprintf(response, "%d\n", status);
        fd = open(PIPE_WRITE, O_WRONLY);
        write(fd, response, strlen(response));
        close(fd);
    }
}