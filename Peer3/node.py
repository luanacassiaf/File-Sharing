import socket
import os
import threading
import time
import queue

MYIP = 'localhost'
MYPORT = 30333
hosts = [10111, 20222]
dataQueue = queue.Queue()



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
    def __init__(self):
        namefile = str(input('Nome do arquivo a receber: '))
        # confirmar se já possui o arquivo
        have = os.path.exists(namefile)
        if have:
            print('Você já possui esse arquivo no diretório local.\n')
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

                if response.strip() == 'Query hit':
                    # registrar os dados enviados pelo servidor
                    file = open(namefile, 'wb')
                    while True:
                        data = self.client.recv(1000000)
                        if not data:
                            break
                        file.write(data)
                    file.close()

                    print(f'{namefile} recebido.\n')
                else:
                    print(f'{host} não possui o arquivo solicitado.\n')

                # confirmar existência do arquivo
                have = os.path.exists(namefile)

                if have == True:
                    break

            self.client.close()

            return


def main():
    while True:
        entry = str(input('Digite R para requisitar ou X para finalizar: '))
        if entry == 'r' or entry == 'R':
            Client()
        elif entry == 'x' or entry == 'X':
            shutMeDown = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            shutMeDown.connect(('localhost', MYPORT))
            server = dataQueue.get()
            server.close()
            event.set()
            break

    return


if __name__ == "__main__":
    event = threading.Event()
    callServer = threading.Thread(target=Server)
    callMain = threading.Thread(target=main)

    callServer.start()
    time.sleep(2)
    callMain.start()
