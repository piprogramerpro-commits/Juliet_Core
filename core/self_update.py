import os
from thinker.goals import should_self_update, load

SECRET_KEY = os.getenv("JULIET_UPDATE_KEY", "1234")


def request_update():

    goals = load()

    if should_self_update(goals):
        return {
            "status": "pending_update",
            "message": "Juliet considera que ha alcanzado un punto de evolución. Se requiere clave para continuar."
        }

    return {"status": "stable"}


def apply_update(key: str):

    if key != SECRET_KEY:
        return {"status": "denied", "message": "Clave incorrecta."}

    # aquí NO auto-modifica código, solo “simula upgrade”
    return {
        "status": "upgraded",
        "message": "Juliet ha aplicado su autoactualización controlada."
    }
