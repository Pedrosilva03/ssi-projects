# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import sys
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import load_pem_x509_certificate
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import datetime
import pytz
from cryptography.hazmat.primitives import serialization

conn_port = 8446
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
        def verifica_validade_certificado(certificado):
            try:
                # Carrega o certificado
                cert = x509.load_der_x509_certificate(certificado.public_bytes(serialization.Encoding.DER), default_backend())

                # Obtém as datas de início e término de validade do certificado em UTC
                not_valid_before_utc = cert.not_valid_before_utc
                not_valid_after_utc = cert.not_valid_after_utc

                # Obtém a data atual em UTC
                data_atual_utc = datetime.datetime.now(datetime.timezone.utc)

                # Verifica se o certificado está válido
                if not_valid_before_utc <= data_atual_utc <= not_valid_after_utc:
                    return True
                else:
                    return False
            except Exception as e:
                print("Ocorreu um erro ao verificar o certificado:", e)
                return False

        with open(f'{folder}{p12_fname}', "rb") as f:
            p12 = f.read()
        password = None # p12 não está protegido...
        (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
        public_key = user_cert.public_key()
        if verifica_validade_certificado(user_cert):
            return (private_key, user_cert, ca_cert, public_key)
        else:
            return None
    
    



    def receive(self, msg=b''):
        if msg.decode() == "ME": print("Mensagem enviada com sucesso")
        if msg.decode() == self.user: print("Nenhuma mensagem por ler")
        else:
            partes = msg.decode().split("//")
            if partes[0] == self.user:
                for i in range(1, len(partes)):
                    mensagens = partes[i].split(";;")
                    print(f'<{mensagens[0]}>:<{mensagens[1]}>:<{mensagens[2]}>:<{mensagens[3]}>')
            elif partes[0] == "R":
                if partes[1] == "NE": print("Número de mensagem inválido")
                elif partes[1] == "SA": print("Sem autorização de consulta dessa mensagem")
                else:
                    argumentos = partes[1].split(";;")
                    encrypted_message = bytes.fromhex(argumentos[3])
                    if self.get_userdata(self.user) == None:
                        print("Certificado inválido")
                        return None
                    
                    (private_key, user_cert, ca_cert, public_key) = self.get_userdata(self.user)
                        
                    decrypted_message = private_key.decrypt(
                        encrypted_message,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    print("-------------------- MENSAGEM ---------------------")
                    print(f'De: {argumentos[0]}')
                    print(f'Data e Hora: {argumentos[1]}')
                    print(f'Assunto: {argumentos[2]}')
                    print(f'Mensagem: {decrypted_message.decode()}')
                    print("--------------------------------------------------")
        
        return None


    
    def sender(self, dest, subj, msg):
        dest_data = dest + ".p12"
        if self.get_userdata(dest_data) == None:
            print("Certificado inválido")
            return None
        
        if self.get_userdata(self.user) == None:
                        print("Certificado inválido")
                        return None
            
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

    def askqueue(self):
        if self.get_userdata(self.user) == None:
            print("Certificado inválido")
            return None
        (dest_private_key, dest_user_cert, dest_ca_cert, dest_public_key) = self.get_userdata(self.user)

        encrypted_message = dest_public_key.encrypt(
            self.user.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Convertendo as mensagens criptografadas e assinatura para hexadecimal
        encrypted_message_hex = encrypted_message.hex()
        signed_message = f'askqueue;;{self.user}//{encrypted_message_hex}'
        return signed_message

    def getmsg(self, num):
        if self.get_userdata(self.user) == None:
            print("Certificado inválido")
            return None
        (dest_private_key, dest_user_cert, dest_ca_cert, dest_public_key) = self.get_userdata(self.user)

        encrypted_message = dest_public_key.encrypt(
            num.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Convertendo as mensagens criptografadas e assinatura para hexadecimal
        encrypted_message_hex = encrypted_message.hex()
        signed_message = f'getmsg;;{self.user}//{encrypted_message_hex}'
        return signed_message
    
    def send(self):
        print('Input message to send (empty to finish)')
        new_msg = input()
    
        tokens = new_msg.split()
        if len(tokens) > 1 and tokens[0] == 'send':
            mensagem = input("Mensagem: ")
            subject = tokens[2]
            for i in range(3, len(tokens)):
                subject += " " + tokens[i]
            return self.sender(tokens[1], subject, mensagem)
        elif tokens[0] == 'askqueue':
            return self.askqueue()
        elif len(tokens) > 1 and tokens[0] == 'getmsg':
            # resposta = "getmsg;;" + self.user + "//" + tokens[1]
            return self.getmsg(tokens[1])
        elif tokens[0] == 'help':
            print("-------------------- HELP ---------------------")
            print("send <user> <subject> - Envia uma mensagem no máximo de 1000 bytes para o utilizador <user> com o assunto <subject>")
            print("askqueue - Lista as mensagens por ler do utilizador")
            print("getmsg <NUM> - solicita ao servidor o envio da mensagem da sua queue com o número <NUM>")
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
