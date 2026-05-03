from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile")

def summarize(state):
    results = "\n\n".join(state["intermediate_results"])

    prompt = f"""
You are a network analysis expert. Based on the data analysis results below, 
produce a clean professional report with these exact sections:

1. CRITICAL CELLS (zero traffic detected)
2. TRAFFIC TRENDS (which cells are healthy vs problematic)
3. ROOT CAUSE POSSIBILITIES 
4. RECOMMENDATIONS

Keep each section concise and factual. Use the actual cell names and numbers from the data.

DATA:
{results}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_output": response.content}
