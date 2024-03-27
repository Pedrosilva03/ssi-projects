import asyncio
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography import x509
import datetime
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from verific import cert_load, cert_validexts, cert_validsubject, cert_validtime

conn_port = 8443
max_msg_size = 9999
key_i = 10
key = key_i.to_bytes(16, 'big')

class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.msg_cnt = 0
        self.aead = AESGCM(key)

    async def process(self, msg=b""):
        self.msg_cnt += 1
        print('Received (%d): %r' % (self.msg_cnt, msg.decode()))

        # Encripta a mensagem
        ciphertext = self.aead.encrypt(nonce=b'unique_nonce', data=msg, associated_data=None)

        decrypted_text = self.aead.decrypt(nonce=b'unique_nonce', data=ciphertext, associated_data=None)

        new_msg = input("Input message to send (empty to finish): ").encode()
        return new_msg if len(new_msg) > 0 else None

    async def initialize_connection(self):
        # Abrir e enviar o certificado do cliente
        with open("MSG_CLI1.crt", "rb") as f:
            client_cert_data = f.read()
        self.writer.write(client_cert_data)
        await self.writer.drain()

        # Aguardar a resposta do servidor (certificado)
        server_cert_data = await self.reader.read(max_msg_size)

        # Carregar e validar o certificado do servidor
        server_cert = x509.load_pem_x509_certificate(server_cert_data)
        try:
            cert_validtime(server_cert)
            cert_validsubject(server_cert, [(x509.NameOID.COMMON_NAME, "MSG_SERVER")])

            print("Certificate of the server is valid.")

        except x509.verification.VerificationError as e:
            print(f"Certificate validation error: {e}")
            return False

        # Aguardar e processar mensagens
        msg = await self.process()
        while msg:
            self.writer.write(msg)
            await self.writer.drain()

            data = await self.reader.read(max_msg_size)

            if data:
                msg = await self.process(data)
            else:
                break

        self.writer.write(b'\n')
        print('Socket closed!')
        self.writer.close()
        return True


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
    client = Client(reader, writer)

    connection_success = await client.initialize_connection()

    if not connection_success:
        print("Failed to establish connection.")

    writer.close()


def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()
