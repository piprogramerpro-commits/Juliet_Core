import json
import os

FILE = "users.json"

def load_users():
    if not os.path.exists(FILE):
        return {}
    return json.load(open(FILE))

def save_users(data):
    json.dump(data, open(FILE, "w"))

def create_user(username, password):
    users = load_users()
    if username in users:
        return False

    users[username] = {
        "password": password,
        "plan": "free",
        "messages": 0,
        "chats": []
    }

    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

def can_use(username):
    users = load_users()
    user = users[username]

    if user["plan"] == "pro":
        return True

    return user["messages"] < 10

def add_message(username):
    users = load_users()
    users[username]["messages"] += 1
    save_users(users)

def upgrade_user(username):
    users = load_users()
    users[username]["plan"] = "pro"
    save_users(users)

def save_chat(username, message):
    users = load_users()
    users[username]["chats"].append(message)
    users[username]["chats"] = users[username]["chats"][-50:]
    save_users(users)

def get_chats(username):
    return load_users()[username]["chats"]
