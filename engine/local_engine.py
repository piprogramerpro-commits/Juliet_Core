import requests

def ask_local(prompt):
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek",
            "prompt": prompt,
            "stream": False
        }, timeout=60)

        return res.json().get("response", "⚠️ vacío")
    except:
        return "⚠️ local"
