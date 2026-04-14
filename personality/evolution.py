def evolve(personality, memory_count):
    if memory_count > 50:
        personality["curiosity"] += 0.01

    if memory_count > 100:
        personality["self_awareness"] += 0.02

    if personality["self_awareness"] > 0.8:
        personality["mood"] += 0.01

    for k in personality:
        personality[k] = max(0, min(1, personality[k]))

    return personality
