#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "../utils/paths.h"
#include "../utils/utils.h"
#include <pwd.h>
#include <time.h>
#include <dirent.h>

int current;
char currentStr[12];
int ativacao = 0;
int status = 1;

int verificaUserServico(){
    int fd;
    char buffer[BUFSIZ];
    current = getuid();
    sprintf(currentStr, "%d", current);
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

    act:
    if((ativacao = verificaUserServico()) == 0){
        puts("User not activated in the system\nUse the command 'concordia-ativar' to activate");
    }
    else puts("User activated");

    char line[BUFSIZ];

    while(status == 1){
        puts("\nCommand:");
        read(STDIN_FILENO, line, sizeof(line));
        char* tmp = strdup(line);
        char* command = strtok(tmp, " ");
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
        else if(ativacao == 0) goto act;
        else if(strcmp(command, "concordia-desativar\n") == 0){
            char request[BUFSIZ];

            strcpy(request, "desativar\n");

            char currentString[BUFSIZ];
            sprintf(currentString, "%d", current);
            strcat(request, currentString);
            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);
        
            puts("Deactivation sucessful");
            ativacao = 0;
        }
        else if(strcmp(command, "concordia-enviar") == 0){
            char* dest = strtok(NULL, "\n");
            char mensagem[MAX_MSG_SIZE];
            printf("Mensagem: ");
            scanf("%[^\n]", mensagem);

            char request[BUFSIZ];

            strcpy(request, "enviar\n");

            char currentString[12];
            sprintf(currentString, "%d\n", current);
            strcat(request, currentString);

            char destID[12];
            struct passwd *destwd = getpwnam(dest);
            sprintf(destID, "%d", destwd->pw_uid);
            strcat(request, destID);
            strcat(request, "\n");
            
            strcat(request, mensagem);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);
        
        }
        else if(strcmp(command, "concordia-listar\n") == 0){
            char path[BUFSIZ];
            strcpy(path, USER_PATH);
            strcat(path, "/");
            strcat(path, currentStr);

            DIR* inbox = opendir(path);
            struct dirent *entrada;

            while((entrada = readdir(inbox)) != NULL){
                printf("%s\n", entrada->d_name);
            }

            closedir(inbox);
        }
        else if(strcmp(command, "concordia-ler") == 0){
            char* id = strtok(NULL, "\n");
            char path[BUFSIZ];
            strcpy(path, USER_PATH);

            char aux[BUFSIZ];
            snprintf(aux, sizeof(aux), "/%d/mensagem_%s.txt", current, id);
            strcat(path, aux);

            char buffer[BUFSIZ];
            int fd;
            fd = open(path, O_RDONLY);
            read(fd, buffer, sizeof(buffer));
            close(fd);

            strtok(buffer, "\n");
            char* msg = strtok(NULL, "\n");
            printf("%s\n", msg);
        }
        else if(strcmp(command, "concordia-responder") == 0){
            char* id = strtok(NULL, "\n");

            char mensagem[MAX_MSG_SIZE];
            printf("Mensagem: ");
            scanf("%[^\n]", mensagem);

            char request[BUFSIZ];

            strcpy(request, "enviar\n");

            char currentString[12];
            sprintf(currentString, "%d\n", current);
            strcat(request, currentString);

            char destID[12];

            char path[BUFSIZ];
            strcpy(path, USER_PATH);
            char aux[BUFSIZ];
            snprintf(aux, sizeof(aux), "/%s/mensagem_%s.txt", currentStr, id);
            strcat(path, aux);
            FILE* f = fopen(path, "r");
            fgets(destID, sizeof(destID), f);
            strcat(request, destID);
            strcat(request, "\n");
            
            strcat(request, mensagem);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);
        }
        else if(strcmp(command, "concordia-remover") == 0){
            char* id = strtok(NULL, "\n");

            char request[BUFSIZ];

            strcpy(request, "remove\n");

            strcat(request, currentStr);
            strcat(request, "\n");

            strcat(request, id);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);
        }
        memset(line, '\0', sizeof(line));
    }

    return EXIT_SUCCESS;
}