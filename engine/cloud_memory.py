from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def save_message(role, content):
    try:
        supabase.table("messages").insert({
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        print("Supabase error:", e)
