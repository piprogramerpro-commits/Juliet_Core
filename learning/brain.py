import json, os, time

MEMORY_FILE = "memory/memory.json"
LEARN_FILE = "learning/learning.json"

def load_json(file):
    if not os.path.exists(file):
        return []
    return json.load(open(file))

def save_json(file, data):
    json.dump(data, open(file, "w"))

def remember(prompt, response):
    data = load_json(MEMORY_FILE)
    data.append({"prompt": prompt, "response": response})
    save_json(MEMORY_FILE, data[-100:])

def learn(prompt, response):
    learn_data = load_json(LEARN_FILE)

    entry = {
        "prompt": prompt,
        "response": response,
        "timestamp": time.time(),
        "quality": evaluate(response)
    }

    learn_data.append(entry)
    save_json(LEARN_FILE, learn_data[-200:])

def evaluate(text):
    score = 0
    if len(text) > 20:
        score += 1
    if "." in text:
        score += 1
    if "\n" in text:
        score += 1
    return score

def improve(prompt):
    memory = load_json(MEMORY_FILE)

    for item in reversed(memory):
        if prompt.lower() in item["prompt"].lower():
            return item["response"]

    return None
