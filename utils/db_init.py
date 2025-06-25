import sqlite3
import os
from utils.db import rotate_old_keys

def initialize_db():
    if not os.path.exists('secrets.db'):
        with sqlite3.connect('secrets.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE users (
                      username TEXT PRIMARY KEY,
                      password TEXT
                      )'''
                    )
            c.execute('''CREATE TABLE secrets (
                      owner TEXT,
                      name TEXT,
                      secret TEXT,
                      key_id,
                      PRIMARY KEY (owner, name),
                      FOREIGN KEY (owner) REFERENCES users(username),
                      FOREIGN KEY (key_id) REFERENCES keys(id)
                      )''')
            c.execute('''CREATE TABLE keys (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT,
                      key TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      is_active BOOLEAN DEFAULT TRUE,
                      FOREIGN KEY (username) REFERENCES users(username)
                      )''')
            conn.commit()

    rotate_old_keys()
