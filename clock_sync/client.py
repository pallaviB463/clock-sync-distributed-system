import socket
import time
import random
from security import encrypt, decrypt

SERVER_IP = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Auto-generate client ID
client_id = random.randint(1000, 9999)
print(f"[CLIENT STARTED] ID = {client_id}")

def request_time():
    t1 = time.time()

    message = f"REQUEST_TIME:{client_id}:{t1}"
    encrypted_msg = encrypt(message)

    client_socket.sendto(encrypted_msg, (SERVER_IP, PORT))

    try:
        client_socket.settimeout(2)
        data, _ = client_socket.recvfrom(1024)

        t4 = time.time()  # Client receive time

        decrypted = decrypt(data)

        if decrypted is None:
            print("[DECRYPT FAILED]")
            return

        parts = decrypted.split(":")

        if len(parts) != 5:
            print("[INVALID RESPONSE FORMAT]")
            return

        _, cid, t1, t2, t3 = parts

        t1 = float(t1)
        t2 = float(t2)
        t3 = float(t3)

        # ✅ Calculations
        delay = (t4 - t1) - (t3 - t2)
        offset = ((t2 - t1) + (t3 - t4)) / 2

        adjusted_time = time.time() + offset

        print(f"""
[CLIENT {cid}]
T1: {t1}
T2: {t2}
T3: {t3}
T4: {t4}

Delay: {delay:.6f} sec
Offset: {offset:.6f} sec
Adjusted Time: {time.ctime(adjusted_time)}
""")

    except socket.timeout:
        print("[ERROR]: No response from server")


while True:
    request_time()
    time.sleep(2)