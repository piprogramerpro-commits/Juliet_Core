import time
from core.db import engine
from sqlalchemy import text

def run_thought_loop():
    while True:
        try:
            with engine.begin() as conn:
                users = conn.execute(text("SELECT username FROM users")).fetchall()

                for u in users:
                    username = u[0]

                    conn.execute(text("""
                    UPDATE users
                    SET personality = jsonb_set(
                        personality,
                        '{mood}',
                        ((personality->>'mood')::float + 0.01)::text::jsonb
                    )
                    WHERE username=:u
                    """), {"u": username})

        except:
            pass

        time.sleep(30)
