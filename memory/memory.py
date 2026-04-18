import json
import os

FILE = "memory/memory.json"

def load():
    if not os.path.exists(FILE):
        return []
    return json.load(open(FILE))

def save_memory(user, ai):
    data = load()
    data.append({"user": user, "ai": ai})
    data = data[-100:]
    json.dump(data, open(FILE, "w"))

def get_memory():
    return load()
