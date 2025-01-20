import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
    except Exception as e:
        print(f"[ERROR] Połączenie przerwane: {e}")
    finally:
        client_socket.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))
    print("[INFO] Połączono z serwerem")
    
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    
    try:
        while True:
            message = input("Ty: ")
            client.send(message.encode())
            if message.lower() == "exit":
                break
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()
        print("[INFO] Połączenie zamknięte")

if __name__ == "__main__":
    main()