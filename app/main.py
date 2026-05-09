from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from app.workflows.graph import build_graph
from app.memory.memory_manager import get_history, add_to_history, clear_history

app = FastAPI()
graph = build_graph()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.post("/query")
def run_query(query: str, session_id: str = "default"):
    try:
        history = get_history(session_id)

        result = graph.invoke({
            "user_query": query,
            "chat_history": history,
            "plan": [],
            "intermediate_results": [],
            "final_output": ""
        })

        add_to_history(session_id, "user", query)
        add_to_history(session_id, "assistant", result["final_output"])

        return {
            "final_output": result["final_output"],
            "session_id": session_id
        }

    except Exception as e:
        # Return error as JSON instead of crashing
        return JSONResponse(
            status_code=500,
            content={"final_output": f"Error: {str(e)}", "error": True}
        )

@app.post("/clear")
def clear_memory(session_id: str = "default"):
    clear_history(session_id)
    return {"message": "Memory cleared!"}

@app.get("/history")
def get_chat_history(session_id: str = "default"):
    return {"history": get_history(session_id)}
