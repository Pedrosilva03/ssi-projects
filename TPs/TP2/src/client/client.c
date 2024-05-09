#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "../utils/paths.h"
#include "../utils/utils.h"

int current;
int ativacao = 0;
int status = 1;

int verificaUserServico(){
    int fd;
    char buffer[BUFSIZ];
    current = getuid();
    if(current <= 0){
        puts("System user error");
        return 0;
    }

    strcpy(buffer, "checkUserActivation\n");

    char currentString[BUFSIZ];
    sprintf(currentString, "%d", current);

    strcat(buffer, currentString);
    strcat(buffer, "\n");

    fd = open(PIPE_READ, O_WRONLY);
    write(fd, buffer, strlen(buffer));
    close(fd);

    char response[1];
    fd = open(PIPE_WRITE, O_RDONLY);
    read(fd, response, sizeof(response));
    close(fd);

    return atoi(response);
}

int main(){
    int fd;
    char buffer[BUFSIZ];

    if((ativacao = verificaUserServico()) == 0){
        puts("User not activated in the system\nUse the command 'concordia-ativar' to activate");
    }
    else puts("User activated");

    char command[BUFSIZ];

    while(status == 1){
        read(STDIN_FILENO, command, sizeof(command));
        if(strcmp(command, "close\n") == 0){
            status = 0;
            continue;
        }
        else if(strcmp(command, "concordia-ativar\n") == 0){
            char request[BUFSIZ];

            strcpy(request, "ativar\n");

            char currentString[BUFSIZ];
            sprintf(currentString, "%d", current);
            strcat(request, currentString);
            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);

            fd = open(PIPE_WRITE, O_RDONLY);
            read(fd, buffer, sizeof(buffer));
            close(fd);

            int res = atoi(strtok(strdup(buffer), "\n"));
            if(res == 1){
                puts("Activation sucessful");
                ativacao = 1;
            }
            else puts("Activation error");
        }
    }

    return EXIT_SUCCESS;
}