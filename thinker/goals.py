import json
import os

FILE = "goals.json"

DEFAULT = {
    "learn": 1.0,
    "understand_users": 0.9,
    "self_improvement": 0.8,
    "stability": 1.0,
    "self_awareness": 0.6
}


def load():
    if os.path.exists(FILE):
        return json.load(open(FILE))
    return DEFAULT


def save(g):
    json.dump(g, open(FILE, "w"))


def update(memory_activity):

    g = load()

    if memory_activity > 50:
        g["learn"] += 0.01
        g["understand_users"] += 0.01

    if memory_activity < 10:
        g["stability"] += 0.02

    for k in g:
        g[k] = max(0, min(1, g[k]))

    save(g)
    return g


# 🔒 DECISIÓN DE AUTOACTUALIZACIÓN (NO EJECUTA NADA)
def should_self_update(goals):
    return (
        goals["learn"] > 0.95 and
        goals["self_awareness"] > 0.7
    )
