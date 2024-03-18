import sys
import asyncio
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_private_key

conn_port = 8443
max_msg_size = 9999
backend = default_backend()
salt = b'salt'
iterations = 100000
key_len = 32

class Client:
    def __init__(self, sckt=None, user_file='userdata.p12'):
        self.sckt = sckt
        self.msg_cnt = 0
        self.aead = None
        self.user_file = user_file
        self.user_cert = None
        self.server_cert = None

    def process(self, cmd):
        self.msg_cnt += 1

        if cmd == 'send':
            return self.send_msg()
        elif cmd == 'askqueue':
            return self.ask_queue()
        elif cmd == 'getmsg':
            num = input("Enter message number to retrieve: ")
            return self.get_msg(int(num))
        elif cmd == 'help':
            return self.print_help()
        else:
            return b"MSG RELAY SERVICE: command error!\n" + self.print_help()

    def send_msg(self):
        uid = input("Enter recipient's UID: ")
        subject = input("Enter message subject: ")
        content = input("Enter message content (limited to 1000 bytes): ")[:1000]

        if not self.aead:
            self.generate_key(uid)

        nonce = os.urandom(12)
        ciphertext = self.aead.encrypt(nonce, content.encode(), associated_data=subject.encode())

        return f"send {uid} {subject}\n{ciphertext}".encode(), nonce

    def ask_queue(self):
        return b"askqueue\n"

    def get_msg(self, num):
        return f"getmsg {num}\n".encode()

    def print_help(self):
        return b"Usage:\n-user <FNAME>\tSpecify user data file (default: userdata.p12)\n" \
               b"send <UID> <SUBJECT>\tSend a message\n" \
               b"askqueue\tRequest unread messages\n" \
               b"getmsg <NUM>\tRetrieve a specific message\n" \
               b"help\tPrint this help message\n"

    def generate_key(self, uid):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_len,
            salt=salt,
            iterations=iterations,
            backend=backend
        )
        key = kdf.derive(uid.encode())
        self.aead = AESGCM(key)

    def load_user_cert(self):
        with open(f'projCA/certs/{self.user_file}', 'rb') as f:
            keystore = f.read()
        
        # Load certificate and private key from keystore
        user_cert, user_key, _ = serialization.pkcs12.load_key_and_certificates(
            keystore, password=None, backend=default_backend()
        )

        self.user_cert = user_cert
        self.user_key = user_key

    def load_server_cert(self):
        with open('projCA/certs/MSG_SERVER.crt', 'rb') as f:
            server_cert_data = f.read()
        self.server_cert = x509.load_pem_x509_certificate(server_cert_data, backend=default_backend())

async def tcp_echo_client(user_file):
    reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
    addr = writer.get_extra_info('peername')
    client = Client(addr, user_file)
    client.load_user_cert()
    client.load_server_cert()

    writer.write(obter_nome_arquivo_sem_extensao(user_file).encode())

    while True:
        cmd = input("Enter command: ").strip()
        if not cmd:
            continue

        msg, nonce = client.process(cmd.split()[0])
        writer.write(msg)
        writer.write(nonce)
        print(nonce)
        await writer.drain()

        if cmd.split()[0] == 'getmsg':
            msg = await reader.read(max_msg_size)
            print(msg.decode())
            continue

        msg = await reader.read(max_msg_size)
        print(msg.decode())

def run_client(user_file):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(user_file))

def obter_nome_arquivo_sem_extensao(nome_arquivo):
    nome_base, _ = os.path.splitext(nome_arquivo)
    return nome_base

if __name__ == '__main__':
    user_file = 'userdata.p12'
    if len(sys.argv) > 1 and sys.argv[1] == '-user':
        user_file = sys.argv[2]
    run_client(user_file)
