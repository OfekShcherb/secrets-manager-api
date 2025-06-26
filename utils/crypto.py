from cryptography.fernet import Fernet
from bcrypt import hashpw, gensalt, checkpw
from utils.kek import encrypt_key, decrypt_key

def generate_key():
    new_key = Fernet.generate_key()
    encrypted_key = encrypt_key(new_key)
    return encrypted_key.decode()

def encrypt_secret(secret, key):
    decrypted_key = Fernet(decrypt_key(key.encode()))
    return decrypted_key.encrypt(secret.encode()).decode()

def decrypt_secret(secret, key):
    decrypted_key = Fernet(decrypt_key(key.encode()))
    return decrypted_key.decrypt(secret.encode()).decode()

def create_hash(string):
    salt = gensalt()
    return hashpw(string.encode(), salt).decode()

def check_hash(string, hash):
    return checkpw(string.encode(), hash.encode())