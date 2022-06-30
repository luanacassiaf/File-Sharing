import socket

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # endereço que deseja conectar
        self.client.connect(('localhost', 7777))
        print('Conectado.\n')

    def query(self):
        namefile = str(input('Nome do arquivo a receber: '))

        # envia nome do arquivo para o servidor
        self.client.send(namefile.encode('utf-8'))

        response = self.client.recv(1024).decode('utf-8')
        if response == 'QUERYHIT':
            # escrever os dados do servidor
            with open(namefile, 'wb') as f:
                while True:
                    data = self.client.recv(1000000)
                    if not data:
                        break
                    f.write(data)

            print(f'{namefile} recebido.\n')
        else:
            print('Não foi dessa vez.\n')

        self.client.close()


if __name__ == "__main__":
    while True:
        requisitar = str(input('Digite R para requisitar: '))
        if requisitar == 'r':
            c = Client()
            c.query()
