# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import sys
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import load_pem_x509_certificate

conn_port = 8445
max_msg_size = 10000
folder = 'projCA/certs/'

class Client:
    """ Classe que implementa a funcionalidade de um CLIENTE. """
    def __init__(self, sckt=None, user='userdata.p12'):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0
        self.user = user

    def get_userdata(self, p12_fname):
        with open(f'{folder}{p12_fname}', "rb") as f:
            p12 = f.read()
        password = None # p12 não está protegido...
        (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
        public_key = user_cert.public_key()
        return (private_key, user_cert, ca_cert, public_key)


    def receive(self, msg=b''):
        if msg.decode() == "ME": print("Mensagem enviada com sucesso")
        else:
            partes = msg.decode().split("//")
            if partes[0] == self.user:
                for i in range(1, len(partes)):
                    mensagens = partes[i].split(";;")
                    print(f'<{mensagens[0]}>:<{mensagens[1]}>:<{mensagens[2]}>:<{mensagens[3]}>')
            elif partes[0] == "R":
                print(partes[1])
                # FALTA DESCODIFICAR A MENSAGEM E DE RESTO ESTÁ FEITO ACHO EU
        
        return None


    
    def sender(self, dest, subj, msg):
        dest_data = dest + ".p12"
        (dest_private_key, dest_user_cert, dest_ca_cert, dest_public_key) = self.get_userdata(dest_data)

        encrypted_message = dest_public_key.encrypt(
            msg.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        (private_key, user_cert, ca_cert, public_key) = self.get_userdata(self.user)

        signature = private_key.sign(
            encrypted_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Convertendo a assinatura para uma sequência de bytes
        signature_bytes = signature

        # Convertendo as mensagens criptografadas e assinatura para hexadecimal
        encrypted_message_hex = encrypted_message.hex()
        signature_hex = signature_bytes.hex()

        # Criando a mensagem com os dados criptografados e assinatura
        signed_message = f'send;;{self.user}||{dest}||{subj}||{encrypted_message_hex}\n\n{signature_hex}'

        return signed_message


        
    def send(self):
        print('Input message to send (empty to finish)')
        new_msg = input()
    
        tokens = new_msg.split()
        if len(tokens) > 1 and tokens[0] == 'send':
            mensagem = input("Mensagem: ")
            return self.sender(tokens[1], tokens[2], mensagem)
        elif tokens[0] == 'askqueue':
            resposta = "askqueue;;" + self.user
            return resposta
        elif len(tokens) > 1 and tokens[0] == 'getmsg':
            resposta = "getmsg;;" + self.user + "//" + tokens[1]
            return resposta
        elif tokens[0] == 'help':
            print("-------------------- HELP ---------------------")
            print("send <user> <subject> - Envia uma mensagem no máximo de 1000 bytes para o utilizador <user> com o assunto <subject>")
            print("askqueue - Lista as mensagens por ler do utilizador")
            print("getmsg - solicita ao servidor o envio da mensagem da sua queue com o número <NUM>")
            print("exit - Termina a ligação")
            print("-----------------------------------------------")
            return None
        elif tokens[0] == 'exit':
            return "exit"
        else:
            print("MSG RELAY SERVICE: command error!")
            print("-------------------- HELP ---------------------")
            print("send <user> <msg> - Envia uma mensagem para o utilizador <user>")
            print("askqueue - Lista as mensagens por ler do utilizador")
            print("getmsg <NUM> - solicita ao servidor o envio da mensagem da sua queue com o número <NUM>")
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
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
        addr = writer.get_extra_info('peername')
    except ConnectionRefusedError:
        print("Erro: Servidor Indisponível")
        return

    user = None
    if len(args) > 2:
        if args[1] == '-user':
            user = args[2]
    client = Client(addr, f'{user}.p12')

    status = 1

    while status == 1:
        msg = client.send()
        if msg:
            if msg == "exit":
                writer.close()
                return KeyboardInterrupt
            writer.write(msg.encode())
            await writer.drain()  # Aguarda até que todos os dados sejam enviados
            msg = await reader.read(max_msg_size)

            if msg:
                msg = client.receive(msg)
                
    writer.close()


def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(sys.argv))


run_client()
