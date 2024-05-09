#include <stdlib.h>

#ifndef UTILS_H
#define UTILS_H

#define LIMITADOR_MENSAGENS "??"

#define MAX_MSG_SIZE 512
#define MAX_MSG_ID 100000

int initFifos();
void removeDir(char* path);

#endif