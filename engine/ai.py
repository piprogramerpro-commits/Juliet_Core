from groq import Groq
import requests
import os

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

AI_MODE = os.getenv("AI_MODE", "fast")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def ask_groq(prompt):
    res = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Eres Juliet, IA clara, profesional y útil."},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content


def ask_ollama(prompt):
    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "deepseek-coder",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        return res.json().get("response", "Error Ollama")
    except:
        return None


def ask_ai(prompt):
    # PRODUCCIÓN → Groq
    if AI_MODE == "fast":
        return ask_groq(prompt)

    # LOCAL → intenta Ollama primero
    if AI_MODE == "local":
        local = ask_ollama(prompt)
        if local:
            return local

    # fallback siempre
    return ask_groq(prompt)
