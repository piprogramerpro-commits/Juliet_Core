from memory.memory import get_memory

def generate_response(prompt):
    memory = get_memory()

    relevant = [m for m in memory if prompt.lower() in m["user"].lower()]
    context = "\n".join([f"{m['user']} -> {m['ai']}" for m in relevant[-3:]])

    response = f"""
**Respuesta**
{prompt}

**Contexto aprendido**
{context if context else "Aprendiendo..."}

**Explicación**
Estoy mejorando usando conversaciones pasadas.
"""

    return response
