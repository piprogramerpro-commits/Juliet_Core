def build_prompt(user_msg, memory, mode="general"):
    context = "\n".join(
        m.get("content", "")
        for m in memory[-6:]
    )

    if mode == "dev":
        system = "Arregla código y responde claro con ```"
    elif mode == "creator":
        system = "Genera contenido creativo corto"
    elif mode == "study":
        system = "Explica fácil como profesor"
    else:
        system = "Responde claro"

    return system + "\n" + context + "\nUsuario: " + user_msg
