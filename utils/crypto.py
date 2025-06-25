from cryptography.fernet import Fernet
from bcrypt import hashpw, gensalt, checkpw

def generate_key():
    return Fernet.generate_key().decode()

def encrypt_secret(secret, key):
    fernet = Fernet(key.encode())
    return fernet.encrypt(secret.encode()).decode()

def decrypt_secret(secret, key):
    fernet = Fernet(key.encode())
    return fernet.decrypt(secret.encode()).decode()

def create_hash(string):
    salt = gensalt()
    return hashpw(string.encode(), salt).decode()

def check_hash(string, hash):
    return checkpw(string.encode(), hash.encode())