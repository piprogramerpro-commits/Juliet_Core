from sqlalchemy import create_engine, text
import os

engine = create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True)


def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            personality JSONB
        )
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS memory (
            id SERIAL PRIMARY KEY,
            username TEXT,
            role TEXT,
            content TEXT
        )
        """))
