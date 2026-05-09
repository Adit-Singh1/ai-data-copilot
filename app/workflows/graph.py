from langgraph.graph import StateGraph
from app.agents.planner import create_plan
from app.agents.executor import execute_plan
from app.agents.summarizer import summarize
from app.memory.state import AgentState

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", create_plan)
    graph.add_node("executor", execute_plan)
    graph.add_node("summarizer", summarize)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "summarizer")

    return graph.compile()
