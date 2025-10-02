import socket
import threading

peers = []

def handle_peer(conn, addr):
    """Recebe mensagens de outros nós"""
    print(f"✅ Conexão recebida de {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"\n📩 {addr} disse: {msg}\n> ", end="")
        except:
            break
    conn.close()
    peers.remove(conn)
    print(f"❌ Desconectado de {addr}")

def server(node_port):
    """Parte servidor do nó P2P"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", node_port))
    s.listen()
    print(f"🚀 Nó escutando em localhost:{node_port}")
    while True:
        conn, addr = s.accept()
        peers.append(conn)
        threading.Thread(target=handle_peer, args=(conn, addr), daemon=True).start()

def connect_to_peer(host, port):
    """Conecta a outro nó P2P"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        peers.append(s)
        threading.Thread(target=handle_peer, args=(s, (host, port)), daemon=True).start()
        print(f"✅ Conectado a peer {host}:{port}")
    except:
        print(f"❌ Falha ao conectar a {host}:{port}")

def main():
    node_port = int(input("Digite a porta deste nó: "))
    threading.Thread(target=server, args=(node_port,), daemon=True).start()

    while True:
        cmd = input("> ")
        if cmd.startswith("connect"):
            _, host, port = cmd.split()
            connect_to_peer(host, int(port))
        else:
            for peer in peers:
                try:
                    peer.send(cmd.encode())
                except:
                    pass

if __name__ == "__main__":
    main()
