from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import os, json, time

app = FastAPI()

# --- setup seguro ---
os.makedirs("memory", exist_ok=True)
os.makedirs("learning", exist_ok=True)

def safe_load(file):
    try:
        return json.load(open(file))
    except:
        return []

def safe_save(file, data):
    json.dump(data, open(file, "w"))

# --- IA REAL (Groq) ---
def call_ai(prompt):
    try:
        import requests

        API_KEY = os.getenv("GROQ_API_KEY")

        if not API_KEY:
            return None

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        return res.json()["choices"][0]["message"]["content"]

    except:
        return None

# --- cerebro ---
def brain(prompt):
    memory = safe_load("memory/memory.json")

    # memoria
    for item in reversed(memory):
        if prompt.lower() in item["prompt"].lower():
            return "(memoria)\n\n" + item["response"]

    # IA real
    response = call_ai(prompt)

    # fallback si falla
    if not response:
        response = f"🤖 Juliet\n\nEstoy funcionando en modo local.\n\nHas dicho: {prompt}"

    # guardar memoria
    memory.append({"prompt": prompt, "response": response})
    safe_save("memory/memory.json", memory[-100:])

    # aprendizaje
    learn = safe_load("learning/learning.json")
    learn.append({
        "prompt": prompt,
        "response": response,
        "quality": len(response)
    })
    safe_save("learning/learning.json", learn[-200:])

    return response

# --- rutas ---
@app.get("/")
def home():
    return HTMLResponse(open("frontend/index.html").read())

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
    return safe_load("learning/learning.json")
