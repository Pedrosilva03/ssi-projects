import asyncio
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

conn_port = 8443
max_msg_size = 9999
key_i = 10
key = key_i.to_bytes(16, 'big')

class Client:
    def __init__(self, sckt=None):
        self.sckt = sckt
        self.msg_cnt = 0
        self.aead = AESGCM(key)

    def process(self, msg=b""):
        self.msg_cnt += 1
        print('Received (%d): %r' % (self.msg_cnt, msg.decode()))

        # Encripta a mensagem
        ciphertext = self.aead.encrypt(nonce=b'unique_nonce', data=msg, associated_data=None)

        decrypted_text = self.aead.decrypt(nonce=b'unique_nonce', data=ciphertext, associated_data=None)

        new_msg = input("Input message to send (empty to finish): ").encode()
        return new_msg if len(new_msg) > 0 else None


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
    addr = writer.get_extra_info('peername')
    client = Client(addr)

    msg = client.process()
    while msg:
        writer.write(msg)
        msg = await reader.read(max_msg_size)

        if msg:
            msg = client.process(msg)
        else:
            break

    writer.write(b'\n')
    print('Socket closed!')
    writer.close()


def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()
