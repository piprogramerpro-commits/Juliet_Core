import json
import os

FILE = "memory.json"

def load_memory():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except:
        return []

def save_memory(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_message(role, content):
    data = load_memory()

    if not isinstance(data, list):
        data = []

    data.append({
        "role": role,
        "content": content
    })

    data = data[-50:]
    save_memory(data)
