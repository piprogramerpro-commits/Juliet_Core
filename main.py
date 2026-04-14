from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()

# Static
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# FAVICON FIX DEFINITIVO
@app.get("/favicon.ico")
def favicon():
    return FileResponse("frontend/static/favicon.ico")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def brain(prompt):
    try:
        if not GROQ_API_KEY:
            return "IA sin API key configurada."

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=10
        )

        data = res.json()
        return data["choices"][0]["message"]["content"]

    except:
        return "Fallback activo: IA operativa."

def generate(prompt):
    response = brain(prompt)

    if not response:
        response = "Sin respuesta."

    for word in response.split():
        yield word + " "

@app.get("/", response_class=HTMLResponse)
def home():
    return open("frontend/index.html").read()

@app.get("/chat")
def chat(prompt: str):
    return StreamingResponse(generate(prompt), media_type="text/plain")
