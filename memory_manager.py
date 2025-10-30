import json, os, time

MEMORY_FILE = "memory.json"

def load_memories():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memories(memories):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

def decay_memories(memories):
    new_memories = []
    for m in memories:
        m["intensity"] *= 0.97
        if m["intensity"] > 0.15:
            new_memories.append(m)
    return new_memories

def add_memory(content, emotion, intensity):
    memories = load_memories()
    memories.append({
        "content": content,
        "emotion": emotion,
        "intensity": intensity,
        "timestamp": time.time()
    })
    memories = decay_memories(memories)
    save_memories(memories)
