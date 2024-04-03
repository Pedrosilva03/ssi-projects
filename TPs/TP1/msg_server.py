# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes

conn_cnt = 0
conn_port = 8445
max_msg_size = 9999

folder = 'projCA/certs/'

class Message:
    def __init__(self, dest, subj, msg_text):
        self.dest = dest
        self.subj = subj
        self.msg_text = msg_text

    def __str__(self):
        return f"{self.dest};;{self.subj};;{self.msg_text}"

class ServerWorker(object):
    """ Classe que implementa a funcionalidade do SERVIDOR. """
    def __init__(self, cnt, addr=None):
        """ Construtor da classe. """
        self.id = cnt
        self.addr = addr
        self.msg_cnt = 0

    def get_userdata(self, p12_fname):
        with open(f'{folder}{p12_fname}', "rb") as f:
            p12 = f.read()
        password = None # p12 não está protegido...
        (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
        public_key = user_cert.public_key()
        return (private_key, user_cert, ca_cert, public_key)

    def process(self, msg):
        self.msg_cnt += 1

        msg = msg.decode()
        tipo, tail = msg.split(';;')
        message, signature = tail.split('\n\n')
        dest, subj, msg_text = message.split("||")

        (private_key, user_cert, ca_cert, public_key) = self.get_userdata(f'{dest}.p12')
        if tipo == 'send':
            if verify_signature(public_key, msg_text.encode(), signature):
                # Criar uma instância da classe Message com os dados recebidos
                message_obj = Message(dest, subj, msg_text)
                # Salvar a mensagem em algum lugar, como um arquivo de log
                with open('messages.log', 'a') as f:
                    f.write(str(message_obj) + '\n')
                print("Mensagem nº %d recebida e salva em messages.log" % self.id)

                txt = msg_text
                new_msg = txt.upper().encode()
                return new_msg if len(new_msg) > 0 else None
            else:
                print("Assinatura inválida. Mensagem descartada.")
                return None



#
#
# Funcionalidade Cliente/Servidor
#
# obs: não deverá ser necessário alterar o que se segue
#

def verify_signature(public_key, message, signature_hex):
    try:
        # Convertendo a assinatura de hexadecimal para bytes
        signature = bytes.fromhex(signature_hex)
        
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

    
async def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt += 1
    addr = writer.get_extra_info('peername')
    srvwrk = ServerWorker(conn_cnt, addr)
    
    while True:
        data = await reader.read(max_msg_size)
        if not data:
            break

        data_str = data.decode()
        if not data_str.strip():
            break
        
        srvwrk.process(data)
        
        # Se desejar enviar uma resposta ao cliente, você pode fazer isso aqui
        # writer.write(response_data)
        # await writer.drain()

    print("[%d]" % srvwrk.id)
    writer.close()


def run_server():
    loop = asyncio.new_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', conn_port)
    server = loop.run_until_complete(coro)
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('  (type ^C to finish)\n')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('\nFINISHED!')

run_server()