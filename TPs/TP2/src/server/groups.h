#ifndef GROUPS_H
#define GROUPS_H

int verifyAdmin(char* nome, char* uid);
int criarGrupo(char* uid, char* nome);
int delGrupo(char* nome, char* uid);
int addMember(char* nome, char* new);
int remMember(char* nome, char* new);

#endif