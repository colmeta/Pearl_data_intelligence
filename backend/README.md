# Clarity Pearl Brain (Backend)

## Setup
1. `pip install fastapi uvicorn pydantic`
2. `uvicorn main:app --reload`

## Deploy to Render
1. Create new Web Service.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
