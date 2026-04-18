from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import time

app = FastAPI()

# IA SIMPLE (rápida)
def brain(prompt):
    return f"🤖 Juliet responde:\n\n{prompt} procesado correctamente."

@app.get("/")
def home():
    return HTMLResponse(open("frontend/index.html").read())

@app.get("/chat")
def chat(prompt: str):
    def stream():
        text = brain(prompt)
        for word in text.split():
            yield word + " "
            time.sleep(0.02)  # velocidad tipo streaming
    return StreamingResponse(stream(), media_type="text/plain")
