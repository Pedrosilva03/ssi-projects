# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket

conn_port = 8445
max_msg_size = 10000

class Client:
    """ Classe que implementa a funcionalidade de um CLIENTE. """
    def __init__(self, sckt=None):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0

    def recive(self, msg=b''):

        """ Processa uma mensagem (`bytestring`) enviada pelo SERVIDOR.
            Retorna a mensagem a transmitir como resposta (`None` para
            finalizar ligação) """
        self.msg_cnt +=1
        #
        # ALTERAR AQUI COMPORTAMENTO DO CLIENTE
        #

        print('Received (%d): %r' % (self.msg_cnt , msg.decode()))
        return None
    
    def send(self):
        print('Input message to send (empty to finish)')
        new_msg = input()
    
        tokens = new_msg.split()
        if len(tokens) > 1 and tokens[0] == '-user':
            print("Falta configurar")
        elif len(tokens) > 1 and tokens[0] == 'send':
            mensagem = input("Mensagem: ")
            return (tokens[1] + " " + tokens[2] + " " + mensagem).encode() if len(new_msg)>0 else None
        elif tokens[0] == 'askqueue':
            print("Falta configurar")
            return None
        elif len(tokens) > 1 and tokens[0] == 'getmsg':
            print("Falta configurar")
            return None
        elif tokens[0] == 'help':
            print("-------------------- HELP ---------------------")
            print("send <user> <msg> - Envia uma mensagem para o utilizador <user>")
            print("askqueue - Lista as mensagens por ler do utilizador")
            print("getmsg - solicita ao servidor o envio da mensagem da sua queue com o número <NUM>")
            print("exit - Termina a ligação")
            print("-----------------------------------------------")
            return None
        else:
            print("MSG RELAY SERVICE: command error!")
            print("-------------------- HELP ---------------------")
            print("send <user> <msg> - Envia uma mensagem para o utilizador <user>")
            print("askqueue - Lista as mensagens por ler do utilizador")
            print("getmsg - solicita ao servidor o envio da mensagem da sua queue com o número <NUM>")
            print("exit - Termina a ligação")
            print("-----------------------------------------------")
            return None

#
#
# Funcionalidade Cliente/Servidor
#
# obs: não deverá ser necessário alterar o que se segue
#


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
    addr = writer.get_extra_info('peername')
    client = Client(addr)
    msg = client.send()
    if msg:
        writer.write(msg)
        msg = await reader.read(max_msg_size)

        if msg :
            msg = client.recive(msg)
            writer.write(b'\n')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()