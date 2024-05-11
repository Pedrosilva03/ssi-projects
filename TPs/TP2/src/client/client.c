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
#include <grp.h>

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
        puts("User not activated in the system\nUse the command 'concordia-ativar' to activate so you can use the service");
    }
    else puts("User activated");

    char line[BUFSIZ];

    while(status == 1){
        memset(line, '\0', sizeof(line));
        memset(buffer, '\0', sizeof(buffer));
        puts("\nCommand:");
        read(STDIN_FILENO, line, sizeof(line));
        char* tmp = strdup(line);
        char* command = strtok(tmp, " ");
        if(strcmp(command, "close\n") == 0){
            status = 0;
            continue;
        }
        else if(strcmp(command, "concordia-ativar\n") == 0){
            if(ativacao == 1){
                puts("User is active already");
                continue;
            }
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
            if(ativacao == 0){
                puts("User is inactive already");
                continue;
            }
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
            scanf(" %[^\n]", mensagem);

            char request[BUFSIZ];

            strcpy(request, "enviar\n");

            char currentString[12];
            sprintf(currentString, "%d\n", current);
            strcat(request, currentString);

            char destID[12];
            struct passwd *destwd = getpwnam(dest);
            struct group *grwd = getgrnam(dest);
            if(destwd == NULL && grwd == NULL){
                puts("User or group not found");
                continue;
            }
            if(destwd != NULL) sprintf(destID, "%d", destwd->pw_uid);
            else{
                sprintf(destID, "%s", grwd->gr_name);

                int i = 0;
                while(grwd->gr_mem[i] != NULL){
                    if(strcmp(grwd->gr_mem[i], getpwuid(current)->pw_name) == 0) goto sender;
                    i++;
                }
                puts("User is not in this group. Ask an admin to join");
                continue;
            }
            sender:
            strcat(request, destID);
            strcat(request, "\n");
            
            strcat(request, mensagem);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);
            memset(mensagem, '\n', sizeof(mensagem));
        }
        else if(strcmp(command, "concordia-listar\n") == 0){
            char path[BUFSIZ];
            strcpy(path, USER_PATH);
            strcat(path, "/");
            strcat(path, currentStr);

            DIR* inbox = opendir(path);
            struct dirent *entrada;

            while((entrada = readdir(inbox)) != NULL){
                if(strchr(entrada->d_name, '_') == NULL) continue;
                char currentPath[BUFSIZ];
                strcpy(currentPath, path);
                strcat(currentPath, "/");
                strcat(currentPath, entrada->d_name);

                char line[1024];
                int fd = open(currentPath, O_RDONLY);    
                read(fd, line, sizeof(line));
                close(fd);

                char* data = strtok(line, "\n");
                char* rem = strtok(NULL, "\n");
                strtok(NULL, "\n");
                int tamanho = atoi(strtok(NULL, "\n"));

                printf("%s ---- %s ---- %d carateres ---- %s\n", data, rem, tamanho, entrada->d_name);
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
            if(fd < 0){
                puts("Mensagem não encontrada");
                continue;
            }
            read(fd, buffer, sizeof(buffer));
            close(fd);

            printf("\n");
            printf("Data: %s\n", strtok(buffer, "\n"));
            printf("Remetente: %s\n", getpwuid(atoi(strtok(NULL, "\n")))->pw_name);
            char* msg = strtok(NULL, "\n");
            printf("Mensagem: %s\n", msg);
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

            char destID[128];

            char path[BUFSIZ];
            strcpy(path, USER_PATH);
            char aux[BUFSIZ];
            snprintf(aux, sizeof(aux), "/%s/mensagem_%s.txt", currentStr, id);
            strcat(path, aux);
            FILE* f = fopen(path, "r");
            if(f == NULL){
                puts("Mensagem não encontrada");
                continue;
            }
            fgets(destID, sizeof(destID), f);
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
        else if(strcmp(command, "concordia-grupo-criar") == 0){
            char* nome = strtok(NULL, "\n");

            char request[BUFSIZ];

            strcpy(request, "grupoc\n");

            char destID[12];
            struct passwd *destwd = getpwuid(current);
            sprintf(destID, "%s", destwd->pw_name);
            strcat(request, destID);
            strcat(request, "\n");

            strcat(request, nome);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);

            fd = open(PIPE_WRITE, O_RDONLY);
            read(fd, buffer, sizeof(buffer));
            close(fd);

            int res = atoi(strtok(strdup(buffer), "\n"));
            if(res == 1) puts("Group created");
            else puts("Error creating group (group already exists or group name is invalid)");

        }
        else if(strcmp(command, "concordia-grupo-remover") == 0){
            char* nome = strtok(NULL, "\n");

            char request[BUFSIZ];

            strcpy(request, "grupodel\n");

            char destID[12];
            struct passwd *destwd = getpwuid(current);
            sprintf(destID, "%s", destwd->pw_name);
            strcat(request, destID);
            strcat(request, "\n");

            strcat(request, nome);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);

            fd = open(PIPE_WRITE, O_RDONLY);
            read(fd, buffer, sizeof(buffer));
            close(fd);

            int res = atoi(strtok(strdup(buffer), "\n"));
            if(res == 0) puts("Group deleted");
            else puts("Error deleting group");

        }
        else if(strcmp(command, "concordia-grupo-destinatario-adicionar") == 0){
            char* nome = strtok(NULL, " ");
            char* new = strtok(NULL, "\n");

            char request[BUFSIZ];

            strcpy(request, "grupoadd\n");

            char destID[12];
            struct passwd *destwd = getpwuid(current);
            sprintf(destID, "%s", destwd->pw_name);
            strcat(request, destID);
            strcat(request, "\n");

            strcat(request, nome);
            strcat(request, "\n");

            strcat(request, new);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);

            fd = open(PIPE_WRITE, O_RDONLY);
            read(fd, buffer, sizeof(buffer));
            close(fd);

            int res = atoi(strtok(strdup(buffer), "\n"));
            if(res == 0) puts("Member added or already exists in group");
            else puts("Error adding member (only the creator of the group can add members)");
        }
        else if(strcmp(command, "concordia-grupo-destinatario-remover") == 0){
            char* nome = strtok(NULL, " ");
            char* new = strtok(NULL, "\n");

            char request[BUFSIZ];

            strcpy(request, "gruporem\n");

            char destID[12];
            struct passwd *destwd = getpwuid(current);
            sprintf(destID, "%s", destwd->pw_name);
            if(strcmp(destID, new) == 0){
                puts("You are trying to remove yourself from the group. If you are an admin, use the command 'concordia-grupo-remover'");
                continue;
            }
            strcat(request, destID);
            strcat(request, "\n");

            strcat(request, nome);
            strcat(request, "\n");

            strcat(request, new);
            strcat(request, "\n");

            strcat(request, LIMITADOR_MENSAGENS);

            fd = open(PIPE_READ, O_WRONLY);
            write(fd, request, strlen(request));
            close(fd);

            fd = open(PIPE_WRITE, O_RDONLY);
            read(fd, buffer, sizeof(buffer));
            close(fd);

            int res = atoi(strtok(strdup(buffer), "\n"));
            if(res == 0) puts("Member removed");
            else puts("Error removing member");
        }
        else if(strcmp(command, "concordia-grupo-listar") == 0){
            char* nome = strtok(NULL, "\n");
            
            struct group* grupo = getgrnam(nome);

            if(grupo == NULL){
                puts("Group doesn't exist");
                continue;
            }

            int i = 0;
            while(grupo->gr_mem[i]){
                printf("Member %d: %s\n", i, grupo->gr_mem[i]);
                i++;
            }
        }
        else if(strcmp(command, "concordia-grupo-ler") == 0){
            char* nome = strtok(NULL, "\n");

            char path[BUFSIZ];
            strcpy(path, GROUP_PATH);
            strcat(path, "/");
            strcat(path, nome);

            DIR* grupo = opendir(path);
            if(grupo == NULL){
                puts("User is not in this group. Ask an admin to join");
                continue;
            }
            else{
                struct dirent* msg;
                while((msg = readdir(grupo)) != NULL){
                    if(strchr(msg->d_name, '_') == NULL) continue;
                    char pathFile[BUFSIZ];
                    strcpy(pathFile, path);
                    strcat(pathFile, "/");
                    strcat(pathFile, msg->d_name);

                    char line[1024];
                    int fd = open(pathFile, O_RDONLY);    
                    read(fd, line, sizeof(line));
                    close(fd);

                    char* data = strtok(line, "\n");
                    char* rem = strtok(NULL, "\n");
                    char* msg = strtok(NULL, "\n");

                    printf("%s ---- %s ---- %s\n", data, rem, msg);
                }
            }
            
        }
    }

    return EXIT_SUCCESS;
}