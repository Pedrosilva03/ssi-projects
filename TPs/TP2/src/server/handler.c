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
}