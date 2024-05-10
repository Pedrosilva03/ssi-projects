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
