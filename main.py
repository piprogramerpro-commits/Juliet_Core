from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def groq(prompt):
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return res.json()["choices"][0]["message"]["content"]
    except:
        return "Error en Groq"

def generate(prompt):
    response = groq(prompt)
    for w in response.split():
        yield w + " "

@app.get("/", response_class=HTMLResponse)
def home():
    return open("frontend/index.html").read()

@app.get("/chat")
def chat(prompt: str):
    return StreamingResponse(generate(prompt), media_type="text/plain")
