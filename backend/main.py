from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
from supabase import create_client, Client
import os
import json

app = FastAPI(
    title="Clarity Pearl API",
    description="The Sensory Nervous System for the AI Economy",
    version="1.0.0"
)

# --- CONFIG ---
# These are loaded from the environment (Render Dashboard)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase Client
supabase: Optional[Client] = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Connected to Supabase DataVault")
    else:
        print("⚠️ SUPABASE_URL or SUPABASE_KEY missing. Running in implementation mode.")
except Exception as e:
    print(f"❌ Failed to connect to Supabase: {e}")

# --- MODELS ---
class JobRequest(BaseModel):
    query: str
    platform: str = "linkedin" # 'linkedin' or 'google_maps'
    compliance_mode: str = "standard" 

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

# --- AUTH MIDDLEWARE ---
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Decodes the JWT token from Supabase. 
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=403, detail="Invalid Auth")
    # In production, verify JWT here using python-jose
    # For now, we return a mock user logic if token is present
    return {"user_id": "mock_user_id_from_token", "token": token} 

# --- ENDPOINTS ---

@app.get("/")
def health_check():
    db_status = "connected" if supabase else "disconnected"
    return {"status": "operational", "db": db_status, "system": "Clarity Pearl Brain"}

@app.post("/api/jobs", response_model=JobResponse)
def create_job(job: JobRequest, user: dict = Depends(get_current_user)):
    """
    Receives a Job from the User/Dashboard.
    """
    if not supabase:
         return JobResponse(job_id="demo_id_no_db", status="queued", message="Demo Mode: DB not connected")

    # Insert into 'jobs' table
    try:
        data = {
            "user_id": user['user_id'], # In real usage, this must be the UUID from auth
            "target_query": job.query,
            "target_platform": job.platform,
            "compliance_mode": job.compliance_mode
        }
        # In a real run, we would execute this:
        # res = supabase.table('jobs').insert(data).execute()
        # job_id = res.data[0]['id']
        
        # Mocking ID for safety until table exists
        job_id = "job_" + os.urandom(4).hex()
        
        return JobResponse(
            job_id=job_id,
            status="queued",
            message=f"Job accepted: {job.query}"
        )
    except Exception as e:
        # In case table doesn't exist yet
        print(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database insertion failed. Did you run schema.sql?")

@app.get("/api/jobs/{job_id}")
def get_job_status(job_id: str, user: dict = Depends(get_current_user)):
    if not supabase:
        return {"job_id": job_id, "status": "simulated", "progress": "DB disconnected"}
        
    # res = supabase.table('jobs').select("*").eq('id', job_id).execute()
    return {"job_id": job_id, "status": "processing", "progress": "Hydra is hunting..."}
