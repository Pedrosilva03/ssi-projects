# Relatório TP1

Tal como os professores pretendiam este trabalho resume-se em dois ficheiros: [msg_client.py](https://github.com/uminho-lei-ssi/2324-G09/blob/main/TPs/TP1/msg_client.py) que trata de executar cada cliente para cada utilizador que queira aceder às funcionalidades oferecidas pelo serviço; [msg_server.py](https://github.com/uminho-lei-ssi/2324-G09/blob/main/TPs/TP1/msg_server.py), programa que executa o servidor responsável por responder aos pedidos de cada utilizador e manter o estado da aplicação guardado.

Com estes dois ficheiros conseguimos construir com sucesso o serviço de *Message Relay* em que os vários clientes conseguem trocar mensagens com garantias de autenticidade a partir de encriptografia, utilizando private keys e certificados, em que cada cliente tem o seu **identificador único**.

## Comandos da aplicação cliente

Tal como é pedido os clientes vão interagir com o sistema a partir do programa [msg_client.py](https://github.com/uminho-lei-ssi/2324-G09/blob/main/TPs/TP1/msg_client.py) que aceitará vários comandos. O nosso cliente interage com o programa de forma interativa podendo no início da execução especificar quem ele é em concreto utilizando o seguinte comando que vamos explicar:

- `-user <USER>` -> é um argumento opcional ao correr o programa do cliente, ou seja, caso se queira especificar qual é o cliente a utilizar o programa de forma iterativa correria-mo-lo da seguinte forma: `python msg_client.py -user MSG_CLI1`, por exemplo, especificando que é o Cliente1 que está a utilizar o programa. Caso não se especifique quem está a utilizar o programa este utiliza o `userdata.p12` como utilizador *default*.

Além deste comando de inicialização temos quatro outros comandos que o utilizador pode utilizar depois de iniciar a sua execução. Estes comandos são usados de forma iterativa:

- `send <UID> <SUBJECT>` -> este comando envia uma mensagem com o assunto `<SUBJECT>` para o utilizador com o identificador único `<UID>`. Depois de fazermos esse comando, aparece na consola `Mensagem:` para escrevemos na frente a partir do `stdin` a mensagem que deve ser enviada, sendo que o seu tamanho está limitado a 1000 bytes. Após corrermos este comando, o destinatário, o subject e a mensagem são enviados para a função `sender` que vai tratar de encriptografar a mensagem, assiná-la e enviá-la a partir do `tcp_echo_client`.

- `askqueue` -> este comando vai chamar a função `askqueue` que vai tratar de pedir ao servidor todas as mensagens que este cliente ainda não leu de forma encriptada. Por cada mensagem que se encontre na queue, esta vai devolver uma linha com a segunte estrutura: `<NUM>:<SENDER>:<TIMESTAMP>:<SUBJECT>`, onde **NUM** é o número de ordem da mensagem, **SENDER** é quem enviou a mensagem, **TIMESTAMP** é um *timestamp* adicionado pelo servidor à mensagem quando esta foi recebida e o **SUBJECT** é o assunto da mensagem. Claramente, depois de uma pessoa usar o comando `getmsg <NUM>` em que o **NUM** é o número de uma das mensagens que aparece na queue, a próxima vez que fizer `askqueue` esta mensagem não vai aparecer novamente, pois já foi lida. Essas mensagens encontram-se guardadas num `messages.log` que é criado quando é enviada a primeira mensagem, onde a mensagem em si encontra-se encriptada, logo ninguém consegue ver qual é a real mensagem a não ser que tenhas as chaves necessárias para desencriptá-la.

- `getmsg <NUM>` -> este comando vai chamar a função `getmsg` que vai tratar de pedir ao servidor o envio da mensagem da sua *queue* com o número de ordem `<NUM>` de forma encriptada. Caso essa mensagem exista, o seu conteúdo é demonstrado na consola e altera o seu estado no `messages.log` para demonstrar que esta já foi lida, removendo-a assim da *queue*. Mas se alguém utilizar este comando de novo com o mesmo **NUM** a mensagem vai aparecer na mesma apesar de já ter sido lida.

- `help` -> comando que imprime as instruções de uso do programa do cliente

- `exit` -> comando que resolvemos adicionar para fechar o cliente, visto que o nosso programa funciona de forma iterativa

- Erro -> Caso se tente utilizar um comando que não exista aparece a mensagem `MSG RELAY SERVICE: command error!` e por baixo os comandos do `help`

Falta mencionar que é a função `receive` que trata das respostas do servidor, por exemplo no `getmsg`, depois de estas serem recebidas no `tcp_echo_client` e trata da sua desencriptação para mostrar posteriormente no `stdout`.

Além das mensagens ficarem todas guardadas num `messages.log`, todos os comandos que são realmente enviados para o servidor ficam registados num `server.log`, mantendo assim um registo de todas as transações do servidor.


## Funcionalidade pretendida



## Identificação e credenciais dos utilizadores



## Possíveis valorizações


