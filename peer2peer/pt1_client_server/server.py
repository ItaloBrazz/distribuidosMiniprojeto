import socket
import threading

clients = []

lock = threading.Lock()  

def handle_client(client_socket, addr):
    with lock:
        clients.append(client_socket)
    print(f"✅ Cliente {addr} conectado. Total de clientes: {len(clients)}")

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"📩 Mensagem recebida de {addr}: {message}")
            response = f"Hello, Client! Conexões ativas: {len(clients)}"
            client_socket.send(response.encode())
    except Exception as e:
        print(f"Erro com cliente {addr}: {e}")
    finally:
        with lock:
            clients.remove(client_socket)
        client_socket.close()
        print(f"❌ Cliente {addr} desconectado. Total de clientes: {len(clients)}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9000))
    server.listen()
    print("🚀 Servidor rodando em localhost:9000")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    main()
