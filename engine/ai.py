import os
import requests
from groq import Groq

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

AI_MODE = os.getenv("AI_MODE", "fast")


# 🧠 DETECTOR DE INTENCIÓN
def detect_mode(text):
    t = text.lower()

    if any(x in t for x in ["código", "programa", "bug", "error", "python", "js"]):
        return "dev"
    if any(x in t for x in ["tarea", "explica", "resume"]):
        return "study"
    if any(x in t for x in ["idea", "historia", "crear"]):
        return "creator"
    return "general"


# 🧠 PROMPT MAESTRO
def build_prompt(msg, memory, mode):
    context = "\n".join([m["content"] for m in memory[-8:]])

    base = """
Eres Juliet, una IA nivel experto.

REGLAS:
- Usa títulos en **negrita**
- Respuestas cortas y claras
- Divide en párrafos
- Código siempre en bloques ```
- Explica como humano, no como robot
- Si es complejo: estructura completa
"""

    extra = {
        "dev": "Modo programador: código completo, limpio y funcional.",
        "study": "Modo estudio: simplifica y explica paso a paso.",
        "creator": "Modo creativo: ideas potentes y organizadas."
    }.get(mode, "")

    return base + extra + "\n" + context + "\nUsuario: " + msg


# 🚀 IA REAL (GROQ)
def ask_groq(prompt):
    r = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content


# 🧠 ROUTER FINAL
def ask_ai(msg, memory):
    mode = detect_mode(msg)
    prompt = build_prompt(msg, memory, mode)
    return ask_groq(prompt)
