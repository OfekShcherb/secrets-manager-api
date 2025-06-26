import os
from cryptography.fernet import Fernet

KEK_SECRET = os.getenv("KEK")

kek_fernet = Fernet(KEK_SECRET.encode())

def encrypt_key(key: str) -> str:
    encrypted_key = kek_fernet.encrypt(key)
    return encrypted_key

def decrypt_key(encrypted_key: str) -> str:
    decrypted_key = kek_fernet.decrypt(encrypted_key)
    return decrypted_key
