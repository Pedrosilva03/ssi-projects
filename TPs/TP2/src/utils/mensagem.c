#include <stdlib.h>
#include "mensagem.h"

struct message{
    int id;
    char* rem;
    char* msg;
};

Mensagem novaMensagem(){
    Mensagem m = malloc(sizeof(struct message));

    return m;
}