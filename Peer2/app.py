from multiprocessing.dummy import active_children
from tkinter import *
from tkinter import messagebox
from multiprocessing import Process, Pipe
from node import main
import time

can_destroy = 0

class Application:
    def __init__(self, parent_conn, p, master=None):
        self.parent_conn = parent_conn
        self.p = p

        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.fontePadrao = ("Arial", "12")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Digite o nome do arquivo desejado.")
        self.titulo["font"] = ("Arial", "12", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer,text="Arquivo:", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Requisitar"
        self.autenticar["font"] = ("Arial", "12")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.option
        self.autenticar.pack()

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Desconectar"
        self.autenticar["font"] = ("Arial", "12")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.kill
        self.autenticar.pack()

        self.mensagem = Label(self.quartoContainer, text="Nó conectado", font=self.fontePadrao)
        self.mensagem.pack()

    def option(self):
        flag = -1
        self.parent_conn.send([True, self.nome.get()])

        while True:
            flag = self.parent_conn.recv()

            if flag == 0:
                self.mensagem["text"] = "Erro ao reeber o arquivo."
            elif flag == 1:
                self.mensagem["text"] = "Arquivo recebido com sucesso."
            elif flag == 2:
                self.mensagem["text"] = "Hosts não possuem o arquivo."
            elif flag == 3:
                self.mensagem["text"] = "Você já possui esse arquivo no diretório local."

            if flag != -1:
                break

    def kill(self):
        global can_destroy
        
        self.parent_conn.send([False, 0])
        time.sleep(2)

        for child in active_children():
            child.terminate()

        parent_conn.close()
        self.p.terminate()

        self.mensagem["text"] = "Nó desconectado"
        can_destroy = 1
        print(can_destroy)

    def on_closing(self):
        if can_destroy != 1:
            if messagebox.askokcancel("Aviso!", "Você não desconectou o nó, as portas ainda estão ocupadas. Tem certeza que deseja fechar a aplicação?"):
                root.destroy()
        else:
            root.destroy()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=main, args=(child_conn,))
    p.start()

    parent_conn.send([False, 1])

    root = Tk()
    root.title('Rede da Empresa XYZ')
    Application(parent_conn, p, root)
    root.mainloop()
