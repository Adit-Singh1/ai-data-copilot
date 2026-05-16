from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from app.workflows.graph import build_graph
from app.memory.memory_manager import get_history, add_to_history, clear_history
from app.tools.chart_tool import chart_traffic_over_time, chart_zero_traffic_cells, chart_cell_comparison
from app.tools.csv_tool import process_csv
from app.auth.auth_handler import register_user, login_user
from pydantic import BaseModel
import os

# Load env variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
graph = build_graph()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

class AuthRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return FileResponse("app/static/login.html")

@app.get("/app")
def main_app():
    return FileResponse("app/static/index.html")

@app.post("/auth/register")
def register(req: AuthRequest):
    return register_user(req.username, req.password)

@app.post("/auth/login")
def login(req: AuthRequest):
    return login_user(req.username, req.password)

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
        return JSONResponse(
            status_code=500,
            content={"final_output": f"Error: {str(e)}", "error": True}
        )

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = process_csv(contents, file.filename)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/charts/traffic")
def get_traffic_chart():
    return {"chart": chart_traffic_over_time()}

@app.get("/charts/zero")
def get_zero_chart():
    return {"chart": chart_zero_traffic_cells()}

@app.get("/charts/comparison")
def get_comparison_chart():
    return {"chart": chart_cell_comparison()}

@app.post("/clear")
def clear_memory(session_id: str = "default"):
    clear_history(session_id)
    return {"message": "Memory cleared!"}

@app.get("/history")
def get_chat_history(session_id: str = "default"):
    return {"history": get_history(session_id)}
