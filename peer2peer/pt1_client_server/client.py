import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9000))
    print("✅ Conectado ao servidor!")

    client.send("Hello, Server!".encode())
    response = client.recv(1024).decode()
    print(f"📩 Resposta do servidor: {response}")

    while True:
        msg = input("> Digite sua mensagem (ou 'sair' para fechar): ")
        if msg.lower() == "sair":
            break
        client.send(msg.encode())
        response = client.recv(1024).decode()
        print(f"📩 Resposta do servidor: {response}")

    client.close()
    print("❌ Conexão encerrada.")

if __name__ == "__main__":
    main()
