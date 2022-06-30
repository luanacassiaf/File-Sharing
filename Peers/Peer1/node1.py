import socket
import os.path
import threading
import time

MYIP = 'localhost'
MYPORT = 1111
hosts = [2222, 3333]


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queryHit = False
        # define endereço do servidor
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
            for linha in file:
                if linha.strip() == namefile.strip():
                    self.queryHit = True
            file.close()

            if self.queryHit:
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

            self.queryHit = False
            connection.close()


class Client:
    def __init__(self):
        self.namefile = str(input('Nome do arquivo a receber: '))
        self.obtive = False

        for host in hosts:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # endereços que deseja conectar
            self.client.connect(('localhost', host))
            print(f'\nConectado com {host}.')
            self.query(host)

            file = open('index.txt', 'r')
            for linha in file:
                if linha.strip() == self.namefile.strip():
                    self.obtive = True
            file.close()

            if self.obtive == True:
                break

    def query(self, host):
        # envia nome do arquivo para o servidor
        self.client.send(self.namefile.encode())

        response = self.client.recv(1024).decode('utf-8')
        if response == 'QUERYHIT':
            # escrever os dados do servidor
            file = open(self.namefile, 'wb')
            while True:
                data = self.client.recv(1000000)
                if not data:
                    break
                file.write(data)

            # adiciona nome do arquivo no próprio índice
            file = open('index.txt', 'w')
            file.write(str(self.namefile))
            file.close()

            print(f'{self.namefile} recebido.\n')
        else:
            print(f'{host} não possui o arquivo solicitado.\n')

        self.client.close()


def main():
    while True:
             # remove nome de arquivos no índice que este nó não possui
            file = open("index.txt", "r")
            linhas = file.readlines()
            file = open("index.txt", "w")
            for linha in linhas:
                existe = os.path.exists(linha)
                if existe:
                    file.write(linha)
            file.close()

            entrada = str(input('Digite R para requisitar: '))
            if entrada == 'r':
                Client()


if __name__ == "__main__":
    x = threading.Thread(target=Server)
    y = threading.Thread(target=main)
    x.start()
    time.sleep(2)
    y.start()
