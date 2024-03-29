# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import sys
from cryptography.hazmat.primitives.serialization import pkcs12

conn_port = 8445
max_msg_size = 10000

class Client:
    """ Classe que implementa a funcionalidade de um CLIENTE. """
    def __init__(self, sckt=None, user='userdata.p12'):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0
        self.user = user

    def get_userdata(p12_fname):
        with open(p12_fname, "rb") as f:
            p12 = f.read()
        password = None # p12 não está protegido...
        (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
        return (private_key, user_cert, ca_cert)

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
        elif tokens[0] == 'exit':
            return '0'
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


async def tcp_echo_client(args):
    reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
    addr = writer.get_extra_info('peername')

    user = None
    if len(args) > 2:
        if args[1] == '-user':
            user = args[2]
    client = Client(addr, f'{user}.p12')

    status = 1

    while status == 1:
        msg = client.send()
        if msg:
            if int(msg) == 0:
                status = 0
            else:
                writer.write(msg)
                msg = await reader.read(max_msg_size)

                if msg:
                    msg = client.recive(msg)
                    writer.write(b'\n')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(sys.argv))


run_client()