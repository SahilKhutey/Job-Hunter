import sys
import os
import uvicorn

# Ensure the backend directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    print("--- Starting HunterOS Backend Wrapper ---")
    uvicorn.run(app, host="127.0.0.1", port=8000)
