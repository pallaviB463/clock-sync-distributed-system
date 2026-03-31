import socket
import time
import threading
from clock_sync.security import encrypt, decrypt

SERVER_IP = "0.0.0.0"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))

print("Server started... Waiting for clients")

def handle_client(data, addr):
    try:
        t2 = time.time()  # Server receive time

        message = decrypt(data)

        if message is None:
            print(f"[INVALID PACKET from {addr}]")
            return

        parts = message.split(":")
        if len(parts) != 3:
            print(f"[BAD FORMAT from {addr}]")
            return

        _, client_id, t1 = parts
        t1 = float(t1)

        t3 = time.time()  # Server send time

        response = f"SERVER_TIME:{client_id}:{t1}:{t2}:{t3}"
        server_socket.sendto(encrypt(response), addr)

        # ✅ Logging
        print(f"""
[LOG]
Client: {client_id}
Address: {addr}
T1 (Client Sent): {t1}
T2 (Server Received): {t2}
T3 (Server Sent): {t3}
""")

    except Exception as e:
        print(f"[ERROR handling {addr}]: {e}")


while True:
    try:
        data, addr = server_socket.recvfrom(1024)

        thread = threading.Thread(target=handle_client, args=(data, addr))
        thread.start()

    except Exception as e:
        print("[SERVER ERROR]:", e)