import time
from core.db import engine
from sqlalchemy import text

def internal_thought_loop():
    while True:
        try:
            with engine.begin() as conn:

                users = conn.execute(text("SELECT username FROM users")).fetchall()

                for u in users:
                    username = u[0]

                    mem = conn.execute(text("""
                        SELECT content FROM memory
                        WHERE username=:u
                        ORDER BY id DESC
                        LIMIT 10
                    """), {"u": username}).fetchall()

                    if not mem:
                        continue

                    summary = "Juliet ha procesado recuerdos y ajustado su estado interno."

                    conn.execute(text("""
                        INSERT INTO memory (username, role, content)
                        VALUES (:u, 'reflection', :c)
                    """), {"u": username, "c": summary})

        except Exception as e:
            print("Thinker error:", e)

        time.sleep(120)  # 🔥 más lento = menos crash
