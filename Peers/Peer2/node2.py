import socket
import os.path
import threading
import time

MYIP = 'localhost'
MYPORT = 2222
hosts = [1111, 3333]


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        queryHit = False

        # define endereço deste servidor
        self.server.bind((MYIP, MYPORT))

        # coloca servidor para ouvir conexões no endereço definido
        self.server.listen(10)
        print(f'Ouvindo conexões em {MYIP}:{MYPORT}.\n')

        while True:
            # responsável por aceitar a conexão do cliente
            connection, address = self.server.accept()

            # recebe solicitação do cliente
            namefile = connection.recv(1024).decode('utf-8')

            # verifica se possui o arquivo
            file = open('index.txt', 'r')
            for line in file:
                if line.strip() == namefile.strip():
                    queryHit = True
            file.close()

            if queryHit:
                text = 'QUERYHIT'
                connection.send(text.encode('utf-8'))

                # ler arquivo em bytes
                file = open(namefile, 'rb')
                for data in file.readlines():
                    connection.send(data)
                file.close()

            else:
                text = 'Não tenho.'
                connection.send(text.encode('utf-8'))

            queryHit = False
            connection.close()


class Client:
    def __init__(self):
        namefile = str(input('Nome do arquivo a receber: '))

        # conectar-se aos endereços listados
        for host in hosts:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('localhost', host))
            print(f'\nConectado com {host}.')

            # envia nome do arquivo para o servidor
            self.client.send(namefile.encode())

            response = self.client.recv(1024).decode('utf-8')
            if response == 'QUERYHIT':
                # registrar os dados enviados pelo servidor
                file = open(namefile, 'wb')
                while True:
                    data = self.client.recv(1000000)
                    if not data:
                        break
                    file.write(data)

                # adiciona nome do arquivo no próprio índice
                file = open('index.txt', 'w')
                file.write(str(namefile))
                file.close()

                print(f'{namefile} recebido.\n')
            else:
                print(f'{host} não possui o arquivo solicitado.\n')

            # confirmar existência do arquivo
            exists = os.path.exists(namefile)

            if exists == True:
                break

        self.client.close()


def checkIndex():
    while True:
        # remove do índice os arquivos que foram deletados
        with open("index.txt", "r") as fread:
            lines = fread.readlines()
            for line in lines:
                exists = os.path.exists(line.strip())
                if not exists:
                    fwrite = open("index.txt", "w")
                    lines.remove(line)
                    fwrite.writelines(lines)
                    fwrite.close()
        fread.close()


def main():
    while True:
        entry = str(input('Digite R para requisitar: '))
        if entry == 'r':
            Client()


if __name__ == "__main__":
    callCheckIndex = threading.Thread(target=checkIndex)
    callServer = threading.Thread(target=Server)
    callMain = threading.Thread(target=main)

    callCheckIndex.start()
    callServer.start()
    time.sleep(2)
    callMain.start()
