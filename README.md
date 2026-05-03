# AI Data Copilot 🤖

A multi-agent AI system for automated network data analysis, built with LangGraph, FastAPI, and Groq LLM.

## Architecture
## Tech Stack

- **FastAPI** - REST API server
- **LangGraph** - Multi-agent workflow orchestration
- **Groq + Llama 3.3** - LLM inference (free tier)
- **SQLite + Pandas** - Data storage and analysis
- **HTML/CSS/JS** - Chat UI

## Features

- Multi-agent system with planning and execution separation
- Real SQL database queries
- Pandas statistical analysis
- Professional report generation
- Clean chat UI with typing animation

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-data-copilot.git
cd ai-data-copilot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn langchain langgraph langchain-groq langchain-core pandas sqlalchemy aiofiles

# Set API key
export GROQ_API_KEY="your-groq-key-here"

# Run the app
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Sample Queries

- Analyze zero traffic cells for last 7 days
- Which cells have the highest traffic?
- Show me cells that recently dropped to zero
- Give me a full network health report
