#include "groups.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <dirent.h>
#include "../utils/paths.h"
#include <sys/stat.h>
#include <grp.h>
#include "files.h"

int verifyAdmin(char* nome, char* uid){
    struct group *grupo = getgrnam(nome);
    if(grupo){
        if(strcmp(grupo->gr_mem[0], uid) == 0) return 1;
        else return 0;
    }
    else return 0;
}

void createGroupInbox(char* uid, char* name){
    char path[BUFSIZ];

    strcpy(path, GROUP_PATH);
    strcat(path, "/");
    strcat(path, name);

    mkdir(path, S_IRWXU | S_IRGRP | S_IWGRP | S_IXGRP);

    struct group *grupo = getgrnam(name);
    chown(path, -1, grupo->gr_gid);
}

int criarGrupo(char* uid, char* nome){
    char command[128];

    snprintf(command, sizeof(command), "sudo groupadd %s", nome);
    int status = system(command);

    createGroupInbox(uid, nome);

    memset(command, '\0', sizeof(command));

    if(status == 0){
        memset(command, '\0', sizeof(command));
        snprintf(command, sizeof(command), "sudo usermod -aG %s %s", nome, uid);
        status = system(command);
        if(status == 0){
            return 1;
        }
        else{
            snprintf(command, sizeof(command), "sudo groupdel %s", nome);
            system(command);
            return 0;
        }
    }
    else{
        snprintf(command, sizeof(command), "sudo groupdel %s", nome);
        system(command);
        return 0;
    }
}

int delGrupo(char* uid, char* nome){
    return 0;
}

int addMember(char* nome, char* new){
    int status = 0;
    char command[128];
    if(!checkActivation(new)) return 1;
    snprintf(command, sizeof(command), "sudo usermod -aG %s %s", nome, new);
    status = system(command);
    return status;
}