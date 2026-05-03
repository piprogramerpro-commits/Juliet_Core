import json, os

FILE="memory/memory.json"

def load():
    if not os.path.exists(FILE):
        return []
    return json.load(open(FILE))

def save(text):
    data = load()
    data.append(text)
    json.dump(data[-50:], open(FILE,"w"))
