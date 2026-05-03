from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.workflows.graph import build_graph

app = FastAPI()
graph = build_graph()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.post("/query")
def run_query(query: str):
    result = graph.invoke({"user_query": query})
    return result
