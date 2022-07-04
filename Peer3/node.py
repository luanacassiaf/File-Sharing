import socket
import os
import queue
import threading
import time

MYIP = 'localhost'
MYPORT = 3333
hosts = [1111, 2222]
dataQueue = queue.Queue()
event = threading.Event()
flag = -2


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queryHit = False
        dataQueue.put(self.server)

        # define endereço deste servidor
        self.server.bind((MYIP, MYPORT))

        # coloca servidor para ouvir conexões no endereço definido
        self.server.listen(10)
        print(f'Ouvindo conexões em {MYIP}:{MYPORT}.\n')

        while True:
            # responsável por aceitar a conexão do cliente
            try:
                connection, address = self.server.accept()
                if address == MYPORT:
                    break
            except:
                break

            # recebe solicitação do cliente
            namefile = connection.recv(1024).decode('utf-8', 'ignore')

            # verifica se possui o arquivo
            self.queryHit = os.path.exists(namefile)

            if self.queryHit:
                text = 'Query hit'
                connection.send(text.encode('utf-8'))

                time.sleep(2)
                # ler arquivo em bytes
                file = open(namefile, 'rb')
                for data in file.readlines():
                    connection.send(data)
                file.close()

            else:
                text = 'Não tenho.'
                connection.send(text.encode('utf-8'))

            self.queryHit = False
            connection.close()

        return


class Client:
    def __init__(self, namefile):
        global flag
        # confirmar se já possui o arquivo
        have = os.path.exists(namefile)
        if have:
            print('Você já possui esse arquivo no diretório local.\n')
            flag = 3
        else:
            # conectar-se aos endereços listados
            for host in hosts:
                try:
                    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client.connect(('localhost', host))
                    print(f'\nConectado com {host}.')
                except:
                    print(f'Host {host} offline.\n')
                    continue

                # envia nome do arquivo para o servidor
                self.client.send(namefile.encode('utf-8'))

                response = self.client.recv(1024).decode('utf-8', 'ignore')
                print(response)

                if response.strip() == 'Query hit':
                    # registrar os dados enviados pelo servidor
                    file = open(namefile, 'wb')
                    while True:
                        data = self.client.recv(1000000)
                        if not data:
                            flag = 0
                            break
                        file.write(data)
                    file.close()

                    print(f'{namefile} recebido.\n')
                    flag = 1
                else:
                    print(f'{host} não possui o arquivo solicitado.\n')
                    flag = 2

                # confirmar existência do arquivo
                have = os.path.exists(namefile)

                if have == True:
                    self.client.close()
                    break

        return


def run(child_conn):
    while True:
        data = child_conn.recv()
        print(data)
        if data[0]:
            if(data[1] != 0):
                print(data[1])
                Client(data[1])
                child_conn.send(flag)
        elif data[1] == 0:
            break

        data[0] = False

    child_conn.close()

    return


def main(child_conn):
    callServer = threading.Thread(target=Server)
    callServer.start()

    run(child_conn)
