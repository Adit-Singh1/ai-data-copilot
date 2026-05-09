from typing import List

# In-memory store (persists during server session)
conversation_store = {}

def get_history(session_id: str) -> List[dict]:
    return conversation_store.get(session_id, [])

def add_to_history(session_id: str, role: str, content: str):
    if session_id not in conversation_store:
        conversation_store[session_id] = []
    conversation_store[session_id].append({
        "role": role,
        "content": content
    })
    # Keep last 10 messages only to avoid token limits
    conversation_store[session_id] = conversation_store[session_id][-10:]

def clear_history(session_id: str):
    conversation_store[session_id] = []

def format_history_for_prompt(session_id: str) -> str:
    history = get_history(session_id)
    if not history:
        return "No previous conversation."
    formatted = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted += f"{role}: {msg['content']}\n"
    return formatted.strip()