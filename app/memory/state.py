from typing import TypedDict, List

class AgentState(TypedDict):
    user_query: str
    plan: List[str]
    intermediate_results: List[str]
    final_output: str