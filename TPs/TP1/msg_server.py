import asyncio
import os
import sys
import base64
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

conn_cnt = 0
conn_port = 8443
max_msg_size = 9999
backend = default_backend()
salt = b'salt'
iterations = 100000
key_len = 32

class ServerWorker(object):
    def __init__(self, cnt, addr=None, user_cert=None):
        self.id = cnt
        self.addr = addr
        self.msg_cnt = 0
        self.aead = None
        self.user_cert = user_cert

    def process(self, msg, nonce):
        if not self.user_cert:
            return b"MSG RELAY SERVICE: client authentication error!\n"
        
        self.msg_cnt += 1

        txt = msg.decode()
        print('%d : %r' % (self.id, txt))
        print(f'{nonce}\n\n\n\n\n')
        decrypted_text = self.aead.decrypt(nonce=nonce, data=txt.encode(), associated_data=None)
        print('%d : %r' % (self.id,decrypted_text))
        new_msg = txt.upper().self.aead.encrypt(nonce=nonce, data=txt.encode(), associated_data=None)

        return new_msg

    def load_user_cert(self):
        with open(f'projCA/certs/MSG_CA.crt', 'rb') as f:
            ca_cert_data = f.read()
        ca_cert = x509.load_pem_x509_certificate(ca_cert_data, backend=default_backend())

        with open(f'projCA/certs/{self.user_cert}.crt', 'rb') as f:
            client_cert_data = f.read()
        self.user_cert = x509.load_pem_x509_certificate(client_cert_data, backend=default_backend())

    def generate_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_len,
            salt=salt,
            iterations=iterations,
            backend=backend
        )
        key = kdf.derive(self.user_cert.subject.public_bytes(serialization.Encoding.DER))
        self.aead = AESGCM(key)

async def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt += 1
    addr = writer.get_extra_info('peername')
    name = await reader.read(max_msg_size)
    srvwrk = ServerWorker(conn_cnt, addr, name.decode())
    srvwrk.load_user_cert()
    srvwrk.generate_key()

    data = await reader.read(max_msg_size)
    nonce = await reader.read(max_msg_size)

    while True:
        if not data:
            continue
        if data[:1] == b'\n':
            break

        data = srvwrk.process(data, nonce)

        if not data:
            break

        writer.write(data)
        await writer.drain()
        data = await reader.read(max_msg_size)

    print("[%d]" % srvwrk.id)
    writer.close()


def run_server():
    loop = asyncio.new_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', conn_port)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('  (type ^C to finish)\n')

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('\nFINISHED!')

if __name__ == '__main__':
    run_server()
