from cryptography.fernet import Fernet
KEY = b'TinoaNRcv1QhNqb8vcO0ZeDr4uH7_kljxX8sENpkJZY='
cipher = Fernet(KEY)
def encrypt(msg):
    return cipher.encrypt(msg.encode())
def decrypt(msg):
    try:
        return cipher.decrypt(msg).decode()
    except Exception as e:
        print("[DECRYPT FAILED]:", e)
        return None


