<h1 align="center">Projeto 2 da UC de Segurança de Sistemas Informáticos - 2023/2024</h1>
<h2 align="center">Concórdia - Serviço local de troca de mensagens</h2>

## Definição
Sistema de conversação local num sistema Linux.
- Notas:
  - Este README irá focar se nas instruções de utilização do serviço. Toda a explicação detalhada do projeto pode ser encontrada [aqui]().
  - Todos os comandos assumem que o ```PWD``` é o diretório raiz deste projeto ```../TPs/TP2```.

## Compilação do serviço
- O serviço dispõe de dois programas, um servidor e um cliente.
- Os programas devem ser compilados através do comando:
```console
make
```
## Execução do serviço
### Servidor
- O servidor coordena todo o serviço. Este controla as permissões e a segurança dos utilizadores no sistema.
- Requer permissões especiais para efetuar ações no sistema pelo que deve ser executado com ```sudo```
```console
sudo ./bin/server
```
- O servidor entrará em modo de espera de pedidos.
- Para fachar o servidor basta fazer ```Ctrl+C```

### Cliente
O cliente deve ser executado com um utilizador diferente do servidor. Para trocar de utilizador basta usar o comando
```console
su "user"
```
E colocar a password do utilizador.
- Para executar o cliente basta utilizar o comando
```console
./bin/client
```
O cliente entrará em modo de espera de comandos.
### Lista de comandos
Em seguida serão listados um conjunto de comandos que o cliente disponibiliza para interação com o serviço.
- Encerramento do cliente:
  - O cliente pode ser fechado de forma "elegante" com o comando
```console
close
```
- Ativação do utilizador
  - Antes de utilizar o serviço o utilizador tem que ser ativado no sistema
```console
concordia-ativar
```
- Desativação do utilizador
  - Da mesma maneira o utilizador pode ser desativado no sistema
```console
concordia-desativar
```
#### Mensagens pessoais
- Enviar uma mensagem
  - Para enviar uma mensagem para uma pessoa ou um grupo
  - O ```destinatario``` pode ser um utilizador ou um grupo
```console
concordia-enviar destinatario
```
- Listar as mensagens na caixa de entrada
  - O serviço ofereçe uma caixa de entrada de mensagens
  - Este comando lista apenas as mensagens na caixa de entrada pessoal
```console
concordia-listar
```
- Ler uma mensagem
  - Ao listar as mensagens da caixa de entrada, é possível obter os seus IDs que podem ser usados para ler as mensagens com este comando
  - ```mid``` representa o ID da mensagem que se pretende ler
```console
concordia-ler mid
```
- Responder a uma mensagem
  - É possível responder a uma mensagem diretamente
  - ```mid``` representa o ID da mensagem que se pretende responder
```console
concordia-responder mid
```
- Apagar uma mensagem
  - É possível apagar uma mensagem da caixa de entrada
  - - ```mid``` representa o ID da mensagem que se pretende apagar
```console
concordia-apagar mid
```
#### Mensagens de grupos
- Criar um grupo
  - Ao criar um grupo, o utilizador é colocado como administrador e tem permissões sobre o grupo
  - ```grupoName``` representa o nome do grupo que se pretende criar
```console
concordia-grupo-criar grupoName
```
- Remover um grupo
  - Da mesma forma, é possível eliminar grupos
  - Apenas os administradores do grupo podem fazer isso
  - ```grupoName``` representa o nome do grupo que se pretende criar
```console
concordia-grupo-remover grupoName
```
- Adicionar um membro a um grupo
  - Apenas os admins podem adicionar membros ao seu grupo
```console
concordia-grupo-destinatario-adicionar grupoName user
```
- Remover um membro de um grupo
  - Da mesma maneira apenas os admins podem remover membros do seu grupo
```console
concordia-grupo-destinatario-remover grupoName user
```
- Listar membros de um grupo
  - Qualquer pessoa consegue ver os membros que pertencem a um grupo
```console
concordia-grupo-listar grupoName
```
- Ler mensagens de um grupo
  - Apenas membros que pertencem ao grupo conseguem ler as suas mensagens
```console
concordia-grupo-ler grupoName
```
## Desinstalação do serviço
Os artifactos de compilação do serviço podem ser apagados com o comando
```console
make clean
```
