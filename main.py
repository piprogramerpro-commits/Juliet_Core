from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import time, json, os

app = FastAPI()

# 🔒 aseguramos archivos
os.makedirs("memory", exist_ok=True)
os.makedirs("learning", exist_ok=True)

if not os.path.exists("memory/memory.json"):
    open("memory/memory.json", "w").write("[]")

if not os.path.exists("learning/learning.json"):
    open("learning/learning.json", "w").write("[]")


def load(file):
    try:
        return json.load(open(file))
    except:
        return []

def save(file, data):
    json.dump(data, open(file, "w"))


def brain(prompt):
    memory = load("memory/memory.json")

    # 🔁 reutilizar si ya existe
    for item in reversed(memory):
        if prompt.lower() in item["prompt"].lower():
            return "(memoria)\n\n" + item["response"]

    response = f"🤖 Juliet\n\n{prompt}"

    # guardar memoria
    memory.append({"prompt": prompt, "response": response})
    save("memory/memory.json", memory[-100:])

    # aprendizaje
    learn = load("learning/learning.json")
    learn.append({
        "prompt": prompt,
        "response": response,
        "quality": len(response)
    })
    save("learning/learning.json", learn[-200:])

    return response


@app.get("/")
def home():
    try:
        return HTMLResponse(open("frontend/index.html").read())
    except:
        return "Frontend no encontrado"


@app.get("/chat")
def chat(prompt: str):
    def stream():
        text = brain(prompt)
        for word in text.split():
            yield word + " "
            time.sleep(0.01)
    return StreamingResponse(stream(), media_type="text/plain")


@app.get("/learning")
def learning():
    return load("learning/learning.json")
