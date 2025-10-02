# Cliente-Servidor Multi-thread - Projeto Peer-to-Peer

## Descrição

Este projeto implementa a **Parte 1: Modelo Cliente-Servidor Multi-thread** do exercício de P2P.

O servidor aceita múltiplos clientes simultaneamente, utilizando **threads** para cada conexão. Cada cliente envia uma mensagem inicial e pode enviar mensagens adicionais, recebendo a resposta do servidor com o número de conexões ativas.

* Servidor: `server.py`
* Cliente: `client.py`

## Funcionalidades

### Servidor (`server.py`)

* Escuta na porta 8080 (ou porta configurável).
* Aceita múltiplos clientes simultaneamente.
* Para cada cliente, recebe mensagens e responde com:

  ```
  Hello, Client! Conexões ativas: X
  ```

  onde `X` é o número de clientes conectados.

### Cliente (`client.py`)

* Conecta ao servidor na porta 8080.
* Envia a primeira mensagem: `Hello, Server!`
* Permite enviar múltiplas mensagens interativamente.
* Recebe e exibe a resposta do servidor.
* Para encerrar, digite `sair`.

## Como usar

### 1. Rodar o servidor

Abra um terminal e execute:

```bash
python3 server.py
```

O servidor iniciará e aguardará conexões na porta 8080.

### 2. Rodar clientes

Abra outros terminais e execute:

```bash
python3 client.py
```

Digite mensagens e veja as respostas do servidor. Para encerrar o cliente, digite `sair`.

### 3. Testar múltiplos clientes

* Abra quantos terminais quiser e execute `client.py` em cada um.
* O servidor mostrará o número de conexões ativas.
* Todos os clientes podem enviar mensagens ao servidor simultaneamente.

## Observações

* Certifique-se de que **a porta 8080 não esteja sendo usada** por outro processo.
* Para mudar a porta, altere o valor tanto no `server.py` quanto no `client.py`.
* O projeto utiliza apenas bibliotecas padrão do Python (`socket` e `threading`), então **não é necessário instalar pacotes externos**.

## Ambiente Virtual (opcional)

Caso queira isolar o projeto ou adicionar bibliotecas externas no futuro:

1. Criar o ambiente virtual:

```bash
python3 -m venv venv
```

2. Ativar o venv:

```bash
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows
```

3. Instalar pacotes externos (se necessário):

```bash
pip install websocket
```

4. Rodar o projeto dentro do venv.

## Exemplo de execução

**Servidor:**

```
🚀 Servidor rodando em localhost:8080
✅ Cliente ('127.0.0.1', 52634) conectado. Total de clientes: 1
📩 Mensagem recebida de ('127.0.0.1', 52634): Hello, Server!
```

**Cliente:**

```
✅ Conectado ao servidor!
📩 Resposta do servidor: Hello, Client! Conexões ativas: 1
> Digite sua mensagem (ou 'sair' para fechar): Olá!
📩 Resposta do servidor: Hello, Client! Conexões ativas: 1
```
