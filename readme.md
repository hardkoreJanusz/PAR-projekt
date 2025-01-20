# Dokumentacja Aplikacji Rozproszonej

## 1. Wprowadzenie
Aplikacja rozproszona została stworzona w Pythonie przy użyciu biblioteki `socket`. Składa się z serwera oraz co najmniej dwóch klientów. Główna funkcjonalność to umożliwienie komunikacji między klientami za pośrednictwem serwera.

---

## 2. Architektura Aplikacji

### 2.1 Komponenty
- **Serwer**:
  - Odpowiada za zarządzanie połączeniami klientów.
  - Obsługuje komunikację między klientami poprzez przesyłanie wiadomości.
- **Klienci**:
  - Łączą się z serwerem i komunikują się z innymi klientami poprzez serwer.

### 2.2 Mechanizm Działania
1. Klient wysyła wiadomość do serwera.
2. Serwer odbiera wiadomość i przesyła ją do wszystkich pozostałych klientów.
3. Klient odbiera wiadomości od serwera w sposób równoległy, dzięki zastosowaniu wątków.

---

## 3. Szczegóły Techniczne

### 3.1 Wykorzystane Protokoły i Narzędzia
- **TCP/IP**:
  - Protokół komunikacyjny zapewniający niezawodną wymianę danych między serwerem a klientami.
- **Biblioteka `socket`**:
  - Umożliwia tworzenie połączeń sieciowych w Pythonie.
- **Wątki (`threading`)**:
  - Zapewniają równoległą obsługę klientów przez serwer oraz jednoczesne wysyłanie i odbieranie wiadomości przez klientów.

### 3.2 Struktura Komunikacji
- Wiadomości przesyłane są jako ciągi tekstowe zakodowane w UTF-8.
- Klient może wysyłać wiadomości w dowolnym momencie, a serwer natychmiast je rozsyła do innych klientów.

---

## 4. Implementacja

### 4.1 Kod Serwera
Serwer uruchamia gniazdo TCP, nasłuchuje połączeń i obsługuje klientów w osobnych wątkach.

```python
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
```

### 4.2 Kod Klienta
Każdy klient działa w wątku umożliwiającym równoczesne wysyłanie i odbieranie wiadomości.

```python
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
```

---

## 5. Problemy i Rozwiązania

### Problem 1: Blokowanie połączeń
- **Opis**: Klient nie mógł jednocześnie wysyłać i odbierać wiadomości.
- **Rozwiązanie**: Zastosowanie wątków (`threading`) do równoległej obsługi odbierania wiadomości.

### Problem 2: Rozłączanie klientów
- **Opis**: Po rozłączeniu klienta serwer próbował nadal wysyłać wiadomości do jego gniazda.
- **Rozwiązanie**: Po zamknięciu połączenia klient jest usuwany z listy aktywnych klientów.

### Problem 3: Obsługa błędów połączenia
- **Opis**: Przerwanie połączenia powodowało błędy na serwerze.
- **Rozwiązanie**: Dodanie obsługi wyjątków i zamykanie gniazd w blokach `finally`.

---

## 6. Uruchamianie Aplikacji

1. Uruchom serwer za pomocą polecenia:
   ```bash
   python server.py
   ```
2. Uruchom klienta w osobnym terminalu:
   ```bash
   python client.py
   ```
3. Wpisuj wiadomości w klientach – zostaną one przesłane do pozostałych klientów za pośrednictwem serwera.

---

## 7. Wnioski
Aplikacja rozproszona umożliwia efektywną komunikację między wieloma klientami poprzez centralny serwer. Zastosowanie protokołu TCP/IP oraz wątków zapewnia płynność i niezawodność działania. W przyszłości można rozbudować aplikację o dodatkowe funkcjonalności, takie jak uwierzytelnianie użytkowników, szyfrowanie wiadomości czy wsparcie dla prywatnych wiadomości.
