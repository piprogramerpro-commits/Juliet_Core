from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import time
import json

from learning.brain import remember, learn, improve

app = FastAPI()

def base_brain(prompt):
    return f"🤖 Juliet\n\nHe procesado tu mensaje:\n\n{prompt}"

def brain(prompt):
    improved = improve(prompt)

    if improved:
        return f"🧠 (memoria)\n\n{improved}"

    response = base_brain(prompt)

    remember(prompt, response)
    learn(prompt, response)

    return response

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
def learning_data():
    try:
        return json.load(open("learning/learning.json"))
    except:
        return []
