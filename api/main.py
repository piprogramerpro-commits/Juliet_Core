from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def home():
    return {"status": "Juliet V7 online"}


# 🔥 STREAMING REAL
@app.get("/chat")
def chat(q: str):

    def stream():

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [
                {"role": "system", "content": "Eres Juliet, una IA concisa, útil y con personalidad propia."},
                {"role": "user", "content": q}
            ],
            "stream": True
        }

        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True
        )

        for line in r.iter_lines():
            if line:
                yield f"data: {line.decode('utf-8')}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
