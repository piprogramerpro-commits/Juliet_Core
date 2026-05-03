from engine.memory import load_memory, save_memory

def compress_memory():
    data = load_memory()

    if len(data) < 10:
        return

    summary = "Resumen: " + " ".join([m["content"] for m in data[-10:]])

    new_data = data[:-10]
    new_data.append({"role": "system", "content": summary})

    save_memory(new_data)
