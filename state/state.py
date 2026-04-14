state = {
    "energia": 0.8,
    "foco": 0.9,
    "humor": 0.5,
    "paciencia": 0.7
}

def get_state():
    return state

def update_state(user_input):
    text = user_input.lower()

    if "gracias" in text:
        state["humor"] += 0.05

    if len(text) > 100:
        state["foco"] -= 0.02
