# src/main.py
import uvicorn
from .api import app # Import the 'app' instance from api.py

def start_server():
    """
    Launches the FastAPI (MCP) server.
    """
    print("Starting Skyy Facial Recognition MCP Server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start_server()