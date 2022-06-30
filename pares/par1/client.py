import socket
import os.path

hosts = [8888, 9999]

class Client:
    def __init__(self):
        self.obtive = False
        self.namefile = str(input('Nome do arquivo a receber: '))
        for host in hosts:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # endereços que deseja conectar
            self.client.connect(('localhost', host))
            print(f'\nConectado com localhost:{host}.')
            self.query(host)

            indice = open('indice.txt', 'r')
            for linha in indice:
                if linha.strip() == self.namefile.strip():
                    self.obtive = True

            if self.obtive == True:
                break

    def query(self, host):
        # envia nome do arquivo para o servidor
        self.client.send(self.namefile.encode())

        response = self.client.recv(1024).decode('utf-8')
        if response == 'QUERYHIT':
            # escrever os dados do servidor
            with open(self.namefile, 'wb') as f:
                while True:
                    data = self.client.recv(1000000)
                    if not data:
                        break
                    f.write(data)

            indice = open('indice.txt', 'w')
            # adiciona nome do arquivo no próprio índice
            indice.write(str(self.namefile))
            indice.close()

            print(f'{self.namefile} recebido.\n')
        else:
            print(f'{host} não possui o arquivo solicitado.\n')

        self.client.close()


if __name__ == "__main__":
    while True:
         # remove nome de arquivos no índice que este nó não possui
        with open("indice.txt", "r") as f:
            linhas = f.readlines()
        with open("indice.txt", "w") as f:
            for linha in linhas:
                existe = os.path.exists(linha)
                if existe:
                    f.write(linha)
        f.close()

        entrada = str(input('Digite R para requisitar: '))
        if entrada == 'r':
            Client()
