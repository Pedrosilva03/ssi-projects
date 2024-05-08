#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include "paths.h"

int initFifos(){
    unlink(PIPE_WRITE);
    unlink(PIPE_READ);

    int pipeWrite = mkfifo(PIPE_WRITE, 0666);
    int pipeRead = mkfifo(PIPE_READ, 0666);
    
    if(pipeWrite == 0 && pipeRead == 0) return 1;
    return 0;
}