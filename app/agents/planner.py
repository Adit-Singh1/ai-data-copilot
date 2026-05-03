from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile")

def create_plan(state):
    query = state["user_query"]
    prompt = f"Break this task into steps:\n{query}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"plan": response.content.split("\n")}