import socket
import threading

clients = []

def broadcast_message(message, sender_socket):
    for client_socket, _ in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"[ERROR] Nie udało się wysłać wiadomości: {e}")

def handle_client(client_socket, address):
    print(f"[INFO] Połączono z {address}")
    clients.append((client_socket, address))
    
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data or data.lower() == 'bye':
                print(f"[INFO] Klient {address} rozłączył się")
                break
            print(f"[{address}] {data}")
            broadcast_message(f"[{address}] {data}", client_socket)
    except Exception as e:
        print(f"[ERROR] Błąd u klienta {address}: {e}")
    finally:
        clients.remove((client_socket, address))
        client_socket.close()

def main():
    """
    Uruchamia serwer i obsługuje połączenia klientów.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)
    print("[INFO] Serwer uruchomiony na porcie 12345")
    
    try:
        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[INFO] Zamknięcie serwera")
    finally:
        server.close()

if __name__ == "__main__":
    main()