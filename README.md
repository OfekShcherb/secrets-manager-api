# Secrets Manager API

A secure Flask-based API for managing user secrets with JWT authentication, encrypted storage, and key rotation.

## Features

- User registration and login with JWT stored in secure HTTP-only cookies
- Password hashing using bcrypt
- Secrets encrypted using symmetric keys (Fernet) stored per user
- Key rotation support to enhance security
- CRUD operations on secrets
- Designed for API clients (CLI, scripts, mobile apps), not browsers

## Getting Started

### Prerequisites

- Python 3.10+
- SQLite (default, included) or adapt for another database
- `pip` package manager

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/secrets-manager-api.git
   cd secrets-manager-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:

   ```bash
   flask run
   ```

# Configuration

The app configuration is in config.py:

- JWT_TOKEN_LOCATION = ["cookies"] - store JWT in cookies
- JWT_COOKIE_CSRF_PROTECT = False - disables CSRF for easier API usage (disable if serving browsers)
- Secret key for JWT and encryption keys generated per user
- Adjust database connection in utils/db.py if needed

# Testing

A test.py script is included for testing common workflows:

```bash
python tests/test.py
```

This script demonstrates user registration, login, adding, retrieving, updating, and deleting secrets.

# Automatic Key Rotation

This project supports secure, automated key rotation for encryption keys used to store secrets.

- Each user is assigned a unique Fernet key used to encrypt their secrets.

- Secrets are stored with a reference to the key (key_id) that encrypted them.

- The app compares this key_id with the user’s current key:

  - If the keys match, nothing happens.

  - If not → the secret is decrypted, re-encrypted with the new key, and updated.

A dedicated script, `rotate_keys.py`, is included to rotate keys manually or on a schedule.

# Security Notes

- Passwords are hashed with bcrypt before storage.
- Secrets are encrypted with symmetric keys using Fernet.
- JWT tokens are stored in secure HTTP-only cookies.
- CSRF protection is disabled for non-browser clients; enable if you expose the API to browsers.
- Implement key rotation and re-encryption for enhanced security.

# License

MIT License
