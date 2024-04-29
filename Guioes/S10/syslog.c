#include <stdio.h>
#include <syslog.h>

int main() {
    // Abrir o log com identificador "my_program" e opções padrão
    openlog("my_program", LOG_PID, LOG_USER);

    // Exemplo de mensagens com diferentes níveis de severidade e origens
    syslog(LOG_EMERG, "Mensagem de emergência");
    syslog(LOG_ALERT, "Mensagem de alerta");
    syslog(LOG_CRIT, "Mensagem crítica");
    syslog(LOG_ERR, "Mensagem de erro");
    syslog(LOG_WARNING, "Mensagem de aviso");
    syslog(LOG_NOTICE, "Mensagem de notificação");
    syslog(LOG_INFO, "Mensagem informativa");
    syslog(LOG_DEBUG, "Mensagem de depuração");

    // Definir o nível mínimo de severidade para filtrar as mensagens
    setlogmask(LOG_MASK(LOG_ERR));

    // Mensagens abaixo do nível de severidade definido não serão enviadas para o syslog
    syslog(LOG_DEBUG, "Esta mensagem de depuração não será enviada");

    // Fechar o log
    closelog();

    return 0;
}