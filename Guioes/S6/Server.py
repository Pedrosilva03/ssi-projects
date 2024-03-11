import asyncio
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

conn_cnt = 0
conn_port = 8443
max_msg_size = 9999
key_i = 10
key = key_i.to_bytes(16, 'big')

class ServerWorker(object):
    def __init__(self, cnt, addr=None):
        self.id = cnt
        self.addr = addr
        self.msg_cnt = 0
        self.aead = AESGCM(key)

    def process(self, msg):
        txt = msg.decode()
        print('%d : %r' % (self.id, txt))
        decrypted_text = self.aead.decrypt(nonce=b'unique_nonce', data=txt, associated_data=None)
        print('%d : %r' % (self.id,decrypted_text))
        new_msg = txt.upper().self.aead.encrypt(nonce=b'unique_nonce', data=txt.encode(), associated_data=None)


        

        new_msg if len(new_msg) > 0 else None
        return new_msg


async def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt += 1
    addr = writer.get_extra_info('peername')
    srvwrk = ServerWorker(conn_cnt, addr)
    
    data = await reader.read(max_msg_size)
    while True:
        if not data:
            continue
        if data[:1] == b'\n':
            break

        data = srvwrk.process(data)

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

run_server()

