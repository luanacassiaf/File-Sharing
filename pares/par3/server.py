import socket

MYIP = 'localhost'
MYPORT = 9999

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
            indice = open('indice.txt', 'r')
            for linha in indice:
                if linha.strip() == namefile.strip():
                    self.queryHit = True
            indice.close()

            if self.queryHit:
                text = 'QUERYHIT'
                connection.send(text.encode('utf-8'))
                # ler arquivo em bytes
                with open(namefile, 'rb') as f:
                    for data in f.readlines():
                        connection.send(data)
                    print(f'{namefile} enviado.\n')
                f.close()
            else:
                text = 'Não tenho.'
                connection.send(text.encode('utf-8'))
                print(f'Não tenho o arquivo {namefile}.\n')

            self.queryHit = False
            connection.close()

if __name__ == "__main__":
        Server()

