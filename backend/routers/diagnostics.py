from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies import get_current_user
from worker.utils.gemini_client import gemini_client
import time

router = APIRouter(prefix="/api/diagnostics", tags=["Diagnostics"])

@router.get("/health")
async def check_ai_health(user: dict = Depends(get_current_user)):
    """
    Checks the heartbeat and token status of Gemini and Groq.
    """
    status = {
        "gemini": {"active": False, "latency": 0, "error": None},
        "groq": {"active": False, "latency": 0, "error": None}
    }
    
    # 1. Check Gemini
    start = time.time()
    try:
        res = gemini_client._call_gemini("Ping")
        if res:
            status["gemini"]["active"] = True
            status["gemini"]["latency"] = round(time.time() - start, 2)
    except Exception as e:
        status["gemini"]["error"] = str(e)

    # 2. Check Groq
    start = time.time()
    try:
        res = gemini_client._call_groq("Ping")
        if res:
            status["groq"]["active"] = True
            status["groq"]["latency"] = round(time.time() - start, 2)
    except Exception as e:
        status["groq"]["error"] = str(e)
        
    return {
        "status": "online" if (status["gemini"]["active"] or status["groq"]["active"]) else "degraded",
        "details": status
    }
