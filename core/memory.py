from sqlalchemy import text
from core.db import engine


def _score(texto: str) -> float:
    t = texto.lower()

    score = 0.5

    # cosas importantes
    if any(w in t for w in ["quiero", "necesito", "problema", "ayuda"]):
        score += 0.2

    if any(w in t for w in ["gracias", "bien", "perfecto"]):
        score += 0.1

    if len(t) < 5:
        score -= 0.3

    return max(0, min(1, score))


def save_memory(user, role, content):

    importance = _score(content)

    # 🧠 SOLO guardar si tiene valor
    if importance < 0.3:
        return

    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO memory (username, role, content, importance)
        VALUES (:u, :r, :c, :i)
        """), {
            "u": user,
            "r": role,
            "c": content,
            "i": importance
        })


def get_memory(user, limit=20):
    with engine.begin() as conn:
        r = conn.execute(text("""
        SELECT content FROM memory
        WHERE username=:u
        ORDER BY importance DESC, id DESC
        LIMIT :l
        """), {"u": user, "l": limit}).fetchall()

        return [x[0] for x in r]


def compress_memory(user):

    with engine.begin() as conn:

        mem = conn.execute(text("""
        SELECT content FROM memory
        WHERE username=:u
        ORDER BY id DESC
        LIMIT 100
        """), {"u": user}).fetchall()

        if len(mem) < 20:
            return

        summary = "Resumen comprimido: patrones emocionales, preferencias y contexto general del usuario."

        conn.execute(text("""
        INSERT INTO memory (username, role, content, importance)
        VALUES (:u, 'summary', :c, 1.0)
        """), {"u": user, "c": summary})
