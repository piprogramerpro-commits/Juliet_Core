from personality.personality import style_response

def process_input(user_input: str, user="default"):

    if not user_input:
        return "Juliet: No he recibido nada."

    text = user_input.lower()

    if "hola" in text:
        return style_response("Hola. Estoy contigo.", None)

    if "qué eres" in text:
        return style_response("Soy Juliet, un sistema en evolución controlada.", None)

    return style_response(f"He entendido: {user_input}", None)
