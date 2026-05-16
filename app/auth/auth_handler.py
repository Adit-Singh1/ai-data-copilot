import json
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username: str, password: str) -> dict:
    users = load_users()
    if username in users:
        return {"success": False, "error": "Username already exists"}
    if len(password) < 4:
        return {"success": False, "error": "Password must be at least 4 characters"}
    if len(username) < 3:
        return {"success": False, "error": "Username must be at least 3 characters"}

    users[username] = {
        "username": username,
        "password": pwd_context.hash(password)
    }
    save_users(users)
    return {"success": True, "username": username}

def login_user(username: str, password: str) -> dict:
    users = load_users()
    if username not in users:
        return {"success": False, "error": "Invalid username or password"}
    if not pwd_context.verify(password, users[username]["password"]):
        return {"success": False, "error": "Invalid username or password"}
    return {"success": True, "username": username}
