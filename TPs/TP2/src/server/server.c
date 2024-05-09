#include <stdlib.h>
#include <stdio.h>
#include "../utils/utils.h"
#include "../utils/paths.h"
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "handler.h"

int main(){
    srand(time(NULL));
    
    if(!initFifos()){
        puts("Erro ao iniciar FIFO's");
        return EXIT_FAILURE;
    }

    int fd_pipe;

    char request[BUFSIZ];

    while(1){
        fd_pipe = open(PIPE_READ, O_RDONLY);
        read(fd_pipe, request, sizeof(request));
        close(fd_pipe);

        char* buffer = strdup(request);
        char* savePtr;

        char* command = strtok_r(buffer, LIMITADOR_MENSAGENS, &savePtr);
        while(command != NULL){
            handle_command(strdup(command));
            command = strtok_r(NULL, LIMITADOR_MENSAGENS, &savePtr);
        }
        free(buffer);

        memset(request, '\0', sizeof(request));
    }

    return EXIT_SUCCESS;
}