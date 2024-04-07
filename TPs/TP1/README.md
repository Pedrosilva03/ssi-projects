# Relatório TP1

Tal como os professores pretendiam, este trabalho resume-se em dois ficheiros: [msg_client.py](https://github.com/uminho-lei-ssi/2324-G09/blob/main/TPs/TP1/msg_client.py) que trata de executar cada cliente para cada utilizador que queira aceder às funcionalidades oferecidas pelo serviço; [msg_server.py](https://github.com/uminho-lei-ssi/2324-G09/blob/main/TPs/TP1/msg_server.py), programa que executa o servidor responsável por responder aos pedidos de cada utilizador e manter o estado da aplicação guardado.

Com estes dois ficheiros conseguimos construir com sucesso o serviço de *Message Relay* em que os vários clientes conseguem trocar mensagens com garantias de autenticidade a partir de encriptografia, utilizando private keys e certificados, em que cada cliente tem o seu **identificador único**.

## Comandos da aplicação cliente

Tal como é pedido, os clientes vão interagir com o sistema a partir do programa [msg_client.py](https://github.com/uminho-lei-ssi/2324-G09/blob/main/TPs/TP1/msg_client.py) que aceitará vários comandos. O nosso cliente interage com o programa de forma interativa podendo no início da execução especificar quem ele é em concreto utilizando o seguinte comando que vamos explicar:

- `-user <USER>` -> é um argumento opcional ao correr o programa do cliente, ou seja, caso se queira especificar qual é o cliente a utilizar o programa correriamo-lo da seguinte forma: `python msg_client.py -user MSG_CLI1`, por exemplo, especificando que é o Cliente1 que está a utilizar o programa. Caso não se especifique quem está a utilizar o programa este utiliza o `userdata.p12` como utilizador *default*.

Além deste comando de inicialização temos quatro outros comandos que o utilizador pode utilizar depois de iniciar a sua execução. Estes comandos são usados de forma iterativa:

- `send <UID> <SUBJECT>` -> este comando envia uma mensagem com o assunto `<SUBJECT>` para o utilizador com o identificador único `<UID>`. Depois de fazermos esse comando, aparece na consola `Mensagem:` para escrevemos na frente a partir do `stdin` a mensagem que deve ser enviada, sendo que o seu tamanho está limitado a 1000 bytes. Após corrermos este comando, o destinatário, o *subject* e a mensagem são enviados para a função `sender` que vai tratar de encriptografar a mensagem, assiná-la e enviá-la a partir da função `tcp_echo_client`, que está a correr em loop à espera de comandos,para o servidor onde vai ficar guardada no `messages.log`.

- `askqueue` -> este comando vai chamar a função `askqueue` que vai tratar de pedir ao servidor todas as mensagens que este cliente ainda não leu, de forma encriptada. Por cada mensagem que se encontre na queue, esta vai devolver uma linha com a segunte estrutura: `<NUM>:<SENDER>:<TIMESTAMP>:<SUBJECT>`, onde **NUM** é o número de ordem da mensagem, **SENDER** é quem enviou a mensagem, **TIMESTAMP** é um *timestamp* adicionado pelo servidor à mensagem quando esta foi recebida e o **SUBJECT** é o assunto da mensagem. Claramente, depois de uma pessoa usar o comando `getmsg <NUM>` em que o **NUM** é o número de uma das mensagens que aparece na *queue*, a próxima vez que fizer `askqueue` esta mensagem não vai aparecer novamente, pois já foi lida. Essas mensagens encontram-se guardadas num `messages.log` que é criado quando é enviada a primeira mensagem, onde a mensagem em si encontra-se encriptada, logo ninguém consegue ver qual é a real mensagem a não ser que tenhas as chaves necessárias para desencriptá-la.

- `getmsg <NUM>` -> este comando vai chamar a função `getmsg` que vai tratar de pedir ao servidor o envio da mensagem da sua *queue* com o número de ordem `<NUM>`, de forma encriptada. Caso essa mensagem exista, o seu conteúdo é demonstrado na consola e altera o seu estado no `messages.log` para demonstrar que esta já foi lida, removendo-a assim da *queue*. Mas se alguém utilizar este comando de novo com o mesmo **NUM**, a mensagem vai aparecer na mesma, apesar de já ter sido lida.

- `help` -> comando que imprime as instruções de uso do programa do cliente

- `exit` -> comando que resolvemos adicionar para fechar o cliente, visto que o nosso programa funciona de forma iterativa

- Erro -> Caso se tente utilizar um comando que não exista, aparece a mensagem `MSG RELAY SERVICE: command error!` e por baixo os comandos do `help`

Falta mencionar que é a função `receive` que trata das respostas do servidor, por exemplo no `getmsg`, depois de estas serem recebidas na função `tcp_echo_client` e trata da sua desencriptação para mostrar posteriormente no `stdout`.

Além das mensagens ficarem todas guardadas num `messages.log`, todos os comandos que são realmente enviados para o servidor ficam registados num `server.log`, com a estrutura `<COMANDO>:<USER> em <TIMESTAMP>:<STATUS>`, mantendo assim um registo de todas as transações do servidor, guardando que comando foi usado, por quem, a que horas e se foi com sucesso ou não.


## Funcionalidade pretendida

1.  Para fazermos com que todas as comunicações entre os clientes e o servidor fossem protegidas contra acesso e/ou manipulação delas, tratamos de encriptografar qualquer mensagem quando esta era enviada para o servidor e quando o servidor enviava de volta para o cliente, onde cada um trata de desencriptá-la por si mesmo. Enquanto que no `msg_client.py` era na função `receive` que se tratava de desencriptografar a mensagem, no servidor encontra-se toda na extensa função `process`. Esta simplesmente dá decode ao comando recebido e depois dependendo de qual é, por exemplo, `send` trata de verificar assinaturas e depois colocar as informações necessárias em cada `.log`, neste caso, a mensagem em si no `messages.log` e que a mensagem foi enviada no `server.log`.

2. Como já temos visto, sempre que é enviada uma mensagem, feito algum pedido ao servidor que fica registado, o servidor trata sempre de atribuir um *timestamp*, para manter um registo do momento em que as mensagens são recebidas e uma pessoa ter em conta se demorou muito tempo para recebê-la, o que pode causar problemas se for o caso. O servidor também não compromete confidencialidade pois a mensagem só passa por ele e é enviada para o cliente ainda encriptada, por exemplo, no `getmsg`, o cliente recebe a mensagem que pediu e é ele que tem de tratar de desencriptá-la, mantendo assim a confidencialidade. Como a mensagem está encriptada, o servidor não consegue manipular então nem conteúdo dela, nem o destino da mensagem 

3. 



## Identificação e credenciais dos utilizadores



## Possíveis valorizações


