#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <syslog.h>
#include <sys/stat.h>
#include <signal.h>

// Função para lidar com sinais, como SIGTERM (pedido de término)
void signal_handler(int sig) {
    switch(sig) {
        case SIGTERM:
            syslog(LOG_INFO, "Received SIGTERM. Exiting...");
            closelog();
            exit(EXIT_SUCCESS);
            break;
        // Adicione tratamento para outros sinais, se necessário
    }
}

int main() {
    // Abrindo o log
    openlog("daemon_syslog", LOG_PID | LOG_CONS, LOG_DAEMON);

    // Definindo o tratador de sinal para SIGTERM
    signal(SIGTERM, signal_handler);

    // Rodando como daemon
    pid_t pid, sid;
    pid = fork();

    // Verificando erro no fork
    if (pid < 0) {
        syslog(LOG_ERR, "Failed to fork.");
        exit(EXIT_FAILURE);
    }

    // Finalizando processo pai
    if (pid > 0) {
        exit(EXIT_SUCCESS);
    }

    // Mudando diretório raiz para / para evitar problemas com a remoção do diretório original
    if (chdir("/") < 0) {
        syslog(LOG_ERR, "Failed to change directory to /");
        exit(EXIT_FAILURE);
    }

    // Fechando os descritores de arquivo padrão
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    // Criando uma nova sessão
    sid = setsid();
    if (sid < 0) {
        syslog(LOG_ERR, "Failed to create new session");
        exit(EXIT_FAILURE);
    }

    // Simulação de atividade do daemon
    while (1) {
        syslog(LOG_INFO, "Daemon running...");
        sleep(5); // Exemplo: espera de 5 segundos
    }

    closelog();
    return EXIT_SUCCESS;
}