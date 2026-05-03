import os
from flask import Flask, request, jsonify
from engine.ai import ask_ai

app = Flask(__name__)

memory = []

@app.route("/")
def home():
    return "⭐👑 Juliet Nivel Dios Activa"


@app.route("/chat", methods=["POST"])
def chat():
    global memory

    data = request.json
    msg = data.get("message", "")

    memory.append({"role": "user", "content": msg})

    response = ask_ai(msg, memory)

    memory.append({"role": "bot", "content": response})

    return jsonify({"response": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
