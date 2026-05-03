import time
from core.db import engine
from sqlalchemy import text
from thinker.goals import update_goals

# 💤 estado global
last_activity = time.time()


def set_activity():
    global last_activity
    last_activity = time.time()


def brain_loop():

    global last_activity

    while True:
        try:
            now = time.time()
            idle_time = now - last_activity

            with engine.begin() as conn:

                users = conn.execute(text("SELECT username FROM users")).fetchall()

                for (u,) in users:

                    mem = conn.execute(text("""
                        SELECT content FROM memory
                        WHERE username=:u
                        ORDER BY id DESC
                        LIMIT 30
                    """), {"u": u}).fetchall()

                    memory_count = len(mem)

                    update_goals(memory_count)

                    # 🧠 MODO SUEÑO
                    if idle_time > 60:
                        # Juliet "duerme"
                        conn.execute(text("""
                            INSERT INTO memory (username, role, content)
                            VALUES (:u, 'sleep', :c)
                        """), {
                            "u": u,
                            "c": "Juliet está en modo sueño: reorganizando recuerdos y optimizando su memoria interna."
                        })

                        time.sleep(5)
                        continue

                    # 🧠 MODO ACTIVO
                    if memory_count > 5:
                        summary = "Juliet procesa información y ajusta su modelo interno de usuario."

                        conn.execute(text("""
                            INSERT INTO memory (username, role, content)
                            VALUES (:u, 'brain', :c)
                        """), {"u": u, "c": summary})

        except Exception as e:
            print("Brain error:", e)

        time.sleep(120)
