import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(msg, memory):
    context = "\n".join([m["content"] for m in memory[-12:]])

    return f"""
Eres Juliet AI, una IA nivel empresa.

REGLAS:
- Respuestas claras
- Títulos en **negrita**
- Código siempre en bloques ```
- Explica como experto humano
- No relleno innecesario

Contexto:
{context}

Usuario: {msg}
"""


def ask_ai(prompt):
    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
