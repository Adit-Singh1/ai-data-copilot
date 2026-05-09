from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile")

def create_plan(state):
    query = state["user_query"]
    history = state.get("chat_history", [])

    # Build context from history
    context = ""
    if history:
        context = "Previous conversation:\n"
        for msg in history[-4:]:  # last 4 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        context += "\n"

    prompt = f"""
{context}
Current user query: {query}

Based on the conversation history above (if any), break this task into steps.
If the user refers to something from earlier (like 'those cells' or 'the same data'),
use the context to understand what they mean.

List the steps clearly, one per line.
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"plan": response.content.split("\n")}
