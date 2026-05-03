import os
from flask import Flask, request, jsonify

from engine.ai import ask_ai, build_prompt
from engine.memory import save_message, get_memory

app = Flask(__name__)


@app.route("/")
def home():
    return "⭐👑 Juliet AI SaaS LIVE"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    msg = data["message"]
    chat_id = data.get("chat_id", 1)

    memory = get_memory(chat_id)
    prompt = build_prompt(msg, memory)

    response = ask_ai(prompt)

    save_message(chat_id, "user", msg)
    save_message(chat_id, "bot", response)

    return jsonify({"response": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
