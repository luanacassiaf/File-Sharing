import socket

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queryHit = False
        # define endereço do servidor
        self.server.bind(('localhost', 9999))

        # coloca servidor para ouvir conexões no endereço definido
        self.server.listen(10)

        print('Ouvindo conexões.\n')

        # responsável por aceitar a conexão do cliente
        connection, address = self.server.accept()

        # recebe solicitação do cliente
        namefile = connection.recv(1024).decode()

        # verifica se possui o arquivo
        indice = open('indice.txt', 'r')
        for linha in indice:
            if linha.strip() == namefile.strip():
                self.queryHit = True
        indice.close()

        if self.queryHit:
            text = 'QUERYHIT'
            connection.send(text.encode())
            # ler arquivo em bytes
            with open(namefile, 'rb') as f:
                for data in f.readlines():
                    connection.send(data)
                print(f'{namefile} enviado.\n')
        else:
            text = 'Não tenho.'
            connection.send(text.encode())

if __name__ == "__main__":
        Server()

