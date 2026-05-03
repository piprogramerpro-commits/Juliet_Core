from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import os, json, time

app = FastAPI()

os.makedirs("memory", exist_ok=True)
os.makedirs("learning", exist_ok=True)

def load(file):
    try:
        return json.load(open(file))
    except:
        return []

def save(file, data):
    json.dump(data, open(file, "w"))

# 🔥 prompt profesional
SYSTEM_PROMPT = """
Eres Juliet, una IA avanzada experta en programación.

Reglas:
- Responde SIEMPRE claro, estructurado y útil
- Usa títulos en negrita
- Explica primero brevemente
- Luego da el código
- Luego da mejoras

Ciberseguridad:
- SOLO defensiva (detección, protección, buenas prácticas)
- Nunca generes código ofensivo o ilegal

Especialidades:
- Python, APIs, IA, automatización
- optimización y debugging
"""

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
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            }
        )

        return res.json()["choices"][0]["message"]["content"]

    except:
        return None

def brain(prompt):
    memory = load("memory/memory.json")

    # memoria inteligente
    for item in reversed(memory):
        if prompt.lower() in item["prompt"].lower():
            return "(memoria)\n\n" + item["response"]

    response = call_ai(prompt)

    if not response:
        response = f"🤖 Juliet\n\nModo local activo.\n\nPregunta: {prompt}"

    # guardar
    memory.append({"prompt": prompt, "response": response})
    save("memory/memory.json", memory[-100:])

    # aprendizaje
    learn = load("learning/learning.json")
    learn.append({
        "prompt": prompt,
        "response": response,
        "score": len(response)
    })
    save("learning/learning.json", learn[-200:])

    return response

@app.get("/")
def home():
    return HTMLResponse(open("frontend/index.html").read())

@app.get("/chat")
def chat(prompt: str):
    def stream():
        text = brain(prompt)
        for chunk in text.split():
            yield chunk + " "
            time.sleep(0.01)
    return StreamingResponse(stream(), media_type="text/plain")
