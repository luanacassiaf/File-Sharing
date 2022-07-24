# P2P-File-Sharing
Trabalho desenvolvido como projeto final da disciplina de Sistemas Distribuídos, do curso Ciência da Computação.

Foi implementada uma rede peer-to-peer com objetivo de compartilhar mídias digitais entre seus pares. A rede utiliza sockets para criar conexões TCP entre seus nós.

Esse projeto possui influência da rede Gnutella, logo não são utilizados trackers para buscar arquivos. Em vez disso, é implementada a propagação de mensagens de solicitação.
Assim, um nó envia para os demais nós da rede o nome do arquivo que deseja receber; o nó que possuir o arquivo desejado irá enviá-lo ao solicitante.

* Execução:
```bash
$ python3 app.py
```
