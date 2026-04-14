import json
import os

FILE = "memory.json"

def load():
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE))
    except:
        return []

def save_memory(text):
    data = load()
    data.append(text)

    # límite para no petar RAM
    data = data[-50:]

    json.dump(data, open(FILE, "w"))
