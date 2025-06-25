import requests

BASE_URL = "http://localhost:5000"

def register(session, username, password):
    print("Registering user...")
    resp = session.post(
        f"{BASE_URL}/register",
        json={"username": username, "password": password}
    )
    print("Register response:", resp.status_code, resp.json())

def login(session, username, password):
    print("Logging in user...")
    resp = session.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password}
    )
    print("Login response:", resp.status_code, resp.json())
    if "access_token_cookie" in session.cookies:
        print("Access token cookie set!")
    else:
        print("No access token cookie found.")

def add_secret(session, name, secret):
    print(f"Adding secret '{name}'...")
    resp = session.post(
        f"{BASE_URL}/secrets",
        json={"name": name, "secret": secret}
    )
    print("Add secret response:", resp.status_code, resp.json())

def update_secret(session, name, secret):
    print(f"Updating secret '{name}'...")
    resp = session.patch(
        f"{BASE_URL}/secrets/{name}",
        json={"secret": secret}
    )
    print("Update secret response:", resp.status_code, resp.json())

def get_secret(session, name):
    print(f"Getting secret '{name}'...")
    resp = session.get(f"{BASE_URL}/secrets/{name}")
    print("Get secret response:", resp.status_code, resp.json())

def delete_secret(session, name):
    print(f"Deleting secret '{name}'...")
    resp = session.delete(f"{BASE_URL}/secrets/{name}")
    print("Delete secret response:", resp.status_code, resp.json())

def test_cases():
    with requests.Session() as session:
        username = "testuser"
        password = "testpass"

        # Register new user
        register(session, username, password)

        # Try registering again to test error
        register(session, username, password)

        # Try adding secret without login - should fail
        add_secret(session, "google", "nopassword")

        # Login wrong credentials username
        login(session, username + "1", password)

        # Login wrong credentials password
        login(session, username, password + "1")

        # Login
        login(session, username, password)

        # Add secret
        add_secret(session, "facebook", "mypassword123")

        # Get secret
        get_secret(session, "facebook")

        # Get secret not existing
        get_secret(session, "instagram")

        # Update secret
        update_secret(session, "facebook", "newpassword456")

        # Get updated secret
        get_secret(session, "facebook")

        # Update secret not existing
        update_secret(session, "instagram", "newpassword456")

        # Delete secret 
        delete_secret(session, "facebook")

        # Try getting deleted secret
        get_secret(session, "facebook")

        # Delete secret not existing
        delete_secret(session, "instagram")

if __name__ == "__main__":
    test_cases()