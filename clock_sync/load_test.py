import threading
import time
import socket
from security import encrypt, decrypt

SERVER_IP = "127.0.0.1"
PORT = 5000

NUM_CLIENTS = 20

def simulate_client(i):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for _ in range(5):
        t1 = time.time()
        msg = f"REQUEST_TIME:{i}:{t1}"

        sock.sendto(encrypt(msg), (SERVER_IP, PORT))

        try:
            sock.settimeout(2)
            data, _ = sock.recvfrom(1024)
            t4 = time.time()

            decrypted = decrypt(data)
            if decrypted:
                parts = decrypted.split(":")
                if len(parts) == 5:
                    _, _, t1, t2, t3 = parts
                    t1, t2, t3 = float(t1), float(t2), float(t3)

                    delay = (t4 - t1) - (t3 - t2)
                    print(f"[Client {i}] Delay: {delay:.6f}")

        except:
            print(f"[Client {i}] Timeout")


threads = []
start = time.time()

for i in range(NUM_CLIENTS):
    t = threading.Thread(target=simulate_client, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()

print("\nTOTAL TIME:", end - start)