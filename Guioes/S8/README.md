# Resposta às questões

## Q1

### Criar ficheiros, exercitar permissões e controlo de acesso

- Criar ficheiro: `touch nome_do_ficheiro`

- Exercitar permissões e controlo de acesso:
    - `chmod u+r nome_do_ficheiro` -> adiciona permissão de leitura para o usuário proprietário
    - `chmod a-x nome_do_ficheiro` -> remove permissão de execução para todos os usuários
    - `chmod g+w nome_do_ficheiro` -> adiciona permissão de escrita para o grupo
    - `chmod o-w nome_do_ficheiro` -> remove permissão de escrita para todos os usuários fora do grupo
    - `chown novo_proprietário arquivo` -> altera o proprietário do arquivo
    - `chgrp novo_grupo arquivo_ou_diretório` -> altera o grupo do arquivo

### Criar diretorias (contendo ficheiros), exercitar permissões e controlo de acesso

- Criar diretorias (contendo ficheiros):
    - `mkdir nome_da_diretoria`
    - `cd nome_da_diretoria`
    - `touch ficheiro1`; `touch ficheiro2`; `touch ficheiro3`

- Exercitar permissões e controlo de acesso:
    - ao fazer `ls -l` na pasta onde criamos a nova diretoria aparecem estas permissões para essa pasta: `drwxrwxr-x 2 antonio antonio 4096 Apr 17 10:00 teste`. Podemos ver que por ser uma diretoria, o primeiro caracter em vez de um -, é um d.
    - ao fazer `ls -l` dentro da pasta aparecem estas permissões:

        total 0

        -rw-rw-r-- 1 antonio antonio 0 Apr 17 10:00 ficheiro1

        -rw-rw-r-- 1 antonio antonio 0 Apr 17 10:00 ficheiro2

        -rw-rw-r-- 1 antonio antonio 0 Apr 17 10:00 ficheiro3
    - podemos alterar as permissões de cada ficheiro com os códigos anteriores, mas também podemos alterar as permissões das diretorias com os mesmos comandos, quando não estamos dentro da diretoria que queremos alterar, mas sim na sua diretoria-pai

## Q2

### Criar utilizador para cada membro da equipa

- Para fazer isso basta simplesmente fazer
    - `sudo useradd membro1`
    - `sudo useradd membro2`
    - `sudo useradd membro3`

### Criar grupos contendo dois elementos da equipa e um contendo todos os elementos da equipa

- Para criar um grupo com dois elementos faz-se os seguintes comandos:
    - `sudo grupoadd grupo2elementos`
    - `sudo usermod -aG grupo2elementos membro1`
    - `sudo usermod -aG grupo2elementos membro2`
    - Ao fazer `cat /etc/group | grep grupo2elementos` recebemos o seguinte resultado, mostrando que tem todos os membros: `grupo2elementos:x:1005:membro1,membro2`

- Para criar o grupo com todos os elementos faz-se os seguintes comandos:
    - `sudo grupoadd grupotodo`
    - `sudo usermod -aG grupotodo membro1`
    - `sudo usermod -aG grupotodo membro2`
    - `sudo usermod -aG grupotodo membro3`
    - Ao fazer `cat /etc/group | grep grupotodo` recebemos o seguinte resultado, mostrando que tem todos os membros: `grupotodo:x:1004:membro1,membro2,membro3`

### Iniciar sessão com os diferentes utilizadores e revistar os exercícios anteriores

- Para iniciar sessão com outro utilizador basta correr o comando: `su outro_utilizador` e como ele não tem permissões não consigo revistar os exercícios anteriores. Para poder aceder aos exercícios teria de adicioná-lo a um grupo que tem acesso aos exercícios ou acrescentá-lo aos users que estão permitidos a aceder a eles.

## Q3

### Criar um programa binário executável que imprima o conteúdo de um ficheiro de texto cujo nome é passado como único argumento da sua linha de comando (ou erro caso não o consiga fazer)

- Para criamos esse programa binário executável que faz o que é pedido escrevemos um programa em C para fazer isso:[program.c](https://github.com/uminho-lei-ssi/2324-G09/tree/main/Guioes/S8/program.c). Para criarmos o seu programa binário executável simplesmente corremos na consola o seguinte comando: `gcc -o program program.c`.

### Definir permissão de setuid para o ficheiro executável

- Para fazermos isto executamos os seguintes dois comandos:
    - `sudo chown user program` -> alterando o proprietário para esse user
    - `sudo chmod u+s program` -> agora, o programa `program` será executado com os privilégios do proprietário do arquivo, neste caso, o usuário user.

### Revisitar os exercícios de permissões anteriores usando sessões com os diferentes utilizadores criados, nas quais é invocado o programa executável com o setuid para o utilizador dono e se passa como argumento o caminho para um ficheiro que só pode ser lido por esse dono

- Se tentarmos correr esse programa utilizando um diferente utilizador com um ficheiro que só pode ser lido por esse dono recebemos a mensagem que `Error opening file: Permission denied`, visto que este só pode ser lido pelo dono, logo qualquer outro utilizador que tente executar o programa com esse ficheiro, não vai conseguir executá-lo com sucesso.

### Estudar os comandos su, sudo, passwd e gpasswd à luz das permissões base da de setuid (para root)

- `su` -> O comando `su` é usado para substituir a identidade do usuário atual pela identidade de outro usuário. Quando é executado, geralmente solicita a senha do usuário para o qual deseja alternar. No entanto, quando este comando é usado em conjunto com permissões `setuid`,por exemplo para o usuário root, não é necessário inserir uma senha. Isso ocorre porque o `setuid` permite que o comando `su` seja executado com os privilégios do proprietário do arquivo (geralmente root), mesmo quando é chamado por um usuário comum. Assim, um usuário comum pode usar o `su` para assumir a identidade de root sem fornecer uma senha.

- `sudo` -> O comando `sudo` permite que usuários autorizados executem comandos com os privilégios de outro usuário, geralmente o root. Por padrão, o `sudo` solicita a senha do usuário atual antes de executar o comando especificado. No entanto, ao usar permissões `setuid`, o sudo pode ser configurado para permitir que usuários específicos executem comandos específicos sem solicitar uma senha. Isso é útil para automatizar determinadas tarefas em scripts ou conceder permissões restritas a usuários específicos.

- `passwd` -> O comando `passwd` é usado para alterar a senha de um usuário. Quando usado pelo usuário root, o passwd pode alterar a senha de qualquer usuário no sistema. No entanto, o passwd não é afetado pelas permissões `setuid`, pois já possui permissões elevadas para alterar senhas.

- `gpasswd` -> O comando `gpasswd` é usado para administrar grupos no sistema, permitindo que você adicione ou remova usuários de grupos e defina administradores de grupos. Assim como o `passwd`, o `gpasswd` não é afetado pelas permissões `setuid`, pois já possui permissões elevadas para gerenciar grupos.

Resumindo, `su` e `sudo` são os comandos mais diretamente afetados pelas permissões `setuid` para o usuário root, pois permitem a execução de comandos com privilégios elevados sem autenticação explícita. Por outro lado, `passwd` e `gpasswd` são comandos que já têm permissões elevadas e, portanto, não são impactados pelas permissões `setuid`.

## Q4

### Definir permissões específicas para os utilizadores e grupos criados (via ACL estendida)

- Utilizando o group `grupotodo` criado na Q2 podemos ver os efeitos dos dois comandos, `setfacl` e `getfacl`, num ficheiro `teste.txt`. Começamos por fazer `getfacl` para ver o ACL atual. Este demonstrou o seguinte resultado:

```
# file: teste.txt
# owner: antonio
# group: antonio
user::rw-
group::rw-
other::rw-
```

- Depois fizemos dois comandos para adicionar um utilizador chamado `novousuario` e outro para adicionar o grupo `grupotodo`:
    - setfacl -m u:novousuario:rw teste.txt
    - setfacl -m g:grupotodo:rw teste.txt
    - Como podemos ver demos quer ao utilizador, quer ao grupo, autorização para ler e escrever nesse ficheiro

- Fazendo agora `getfacl` recebemos a seguinte mensagem:
```
# file: teste.txt
# owner: antonio
# group: antonio
user::rw-
user:novousuario:rw-
group::rw-
group:grupotodo:rw-
mask::rw-
other::rw-
```

- Conseguimos assim ver então que extendemos a ACL desse ficheiro e o que cada utilizador/grupo consegue aceder

### Experimentar os mecanismos de controlo de acesso à luz das novas permissões definidas

- Visto que agora quer o utilizador `novousuario`, quer o grupo `grupotodo` têm permissões de leitura e escrita, se fizermos `su` para um desses utilizadores, agora poderemos ler e escrever nesse ficheiro `teste.txt`.
