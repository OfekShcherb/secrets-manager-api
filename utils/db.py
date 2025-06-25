import sqlite3
from utils.crypto import generate_key
from datetime import datetime, timedelta

DB_PATH = 'secrets.db'

def get_user_by_username(username):
    with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        return c.fetchone()

def insert_user(username, password, key):
    with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO users VALUES (?, ?)', (username, password))
        c.execute('INSERT INTO keys (username, key) VALUES (?, ?)', (username, key))
        conn.commit()

def get_active_key(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, key FROM keys WHERE username = ? AND is_active = 1', (username,))
        row = c.fetchone()
        return row if row else None

def get_key_by_id(key_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT key FROM keys WHERE id = ?', (key_id,))
        row = c.fetchone()
        return row[0] if row else None
    
def insert_secret(owner, name, secret, key_id):
    try:
        with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO secrets (owner, name, secret, key_id) VALUES (?, ?, ?, ?)', (owner, name, secret, key_id))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
    
def update_secret_encryption(owner, name, new_ciphertext, new_key_id):
    with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('UPDATE secrets SET secret = ?, key_id = ? WHERE owner = ? AND name = ?', (new_ciphertext, new_key_id, owner, name))
        conn.commit()
    
def get_secret_record(owner, name):
    with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('SELECT secret, key_id FROM secrets WHERE owner = ? AND name = ?', (owner, name))
        return c.fetchone()

def delete_secret_by_name(owner, name):
    with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM secrets WHERE owner = ? AND name = ?', (owner, name))
        conn.commit()

def rotate_user_key(username, new_key):
    with sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('UPDATE keys SET is_active = 0 WHERE username = ? and is_active = 1', (username,))
        c.execute('INSERT INTO keys (username, key) VALUES (?, ?)', (username, new_key))
        conn.commit()

def rotate_old_keys(threshold_days=30):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        cutoff = datetime.now() - timedelta(days=threshold_days)
        c.execute('''SELECT username FROM keys WHERE is_active = 1 AND created_at < ?''', (cutoff,))
        usernames = [row[0] for row in c.fetchall()]

        for username in usernames:
            new_key = generate_key()
            c.execute('UPDATE keys SET is_active = 0 WHERE username = ? and is_active = 1', (username,))
            c.execute('INSERT INTO keys (username, key) VALUES (?, ?)', (username, new_key))


    

