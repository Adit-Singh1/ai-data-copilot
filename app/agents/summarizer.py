from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile")

def is_followup(query: str, history: list) -> bool:
    if not history:
        return False
    followup_words = ["those", "that", "it", "them", "which", "what should", 
                      "how", "why", "tell me more", "explain", "about it",
                      "most critical", "what to do", "fix", "resolve"]
    query_lower = query.lower()
    return any(word in query_lower for word in followup_words)

def summarize(state):
    results = "\n\n".join(state["intermediate_results"])
    history = state.get("chat_history", [])
    query = state["user_query"]

    # Build conversation history text
    context = ""
    if history:
        context = "Previous conversation:\n"
        for msg in history[-6:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            # Only include first 300 chars of assistant messages to save tokens
            content = msg["content"][:300] + "..." if msg["role"] == "assistant" and len(msg["content"]) > 300 else msg["content"]
            context += f"{role}: {content}\n"
        context += "\n"

    if is_followup(query, history):
        # Conversational answer for follow-up questions
        prompt = f"""
You are a network analysis expert in a conversation.

{context}
Current question: {query}

Answer this follow-up question DIRECTLY and CONCISELY.
- Do NOT generate a full report
- Do NOT repeat all the previous findings
- Just answer the specific question asked
- Reference specific cell names and numbers
- Keep it to 3-5 sentences maximum
- Be direct like a human expert would be

Fresh data if needed:
{results[:500]}
"""
    else:
        # Full report for new analysis questions
        prompt = f"""
You are a network analysis expert.

{context}
Current query: {query}

Based on the data below, produce a structured report with:
1. CRITICAL CELLS (zero traffic detected)
2. TRAFFIC TRENDS (healthy vs problematic)
3. ROOT CAUSE POSSIBILITIES
4. RECOMMENDATIONS

Use actual cell names and numbers. Be concise.

DATA:
{results}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_output": response.content}
