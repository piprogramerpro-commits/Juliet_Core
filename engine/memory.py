from engine.db import get_conn

def save_message(chat_id, role, content):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO messages (chat_id, role, content)
        VALUES (%s, %s, %s)
    """, (chat_id, role, content))

    conn.commit()
    conn.close()


def get_memory(chat_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, content FROM messages
        WHERE chat_id=%s
        ORDER BY id ASC
    """, (chat_id,))

    rows = cur.fetchall()
    conn.close()

    return [{"role": r[0], "content": r[1]} for r in rows]
