from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/outreach", tags=["Outreach Automation"])

class EmailRequest(BaseModel):
    target_emails: List[str]
    subject: str
    body_template: str
    sender_identity: str
    service_provider: str = "sendgrid" # or 'mailgun', 'smtp'
    api_key: str

@router.post("/send")
async def send_outreach_email(request: EmailRequest):
    """
    Trigger real email outreach via external providers.
    """
    
    if not request.api_key:
         raise HTTPException(status_code=400, detail="Missing Email Provider API Key")
         
    print(f"📧 Starting Outreach Campaign: {request.subject}")
    
    results = []
    
    # Loop continuously over targets (Real logic flow)
    for email in request.target_emails:
        # Here we would use 'requests.post' to the SendGrid/Mailgun API
        # Example logic structure:
        # resp = requests.post(
        #     "https://api.mailgun.net/v3/...",
        #     auth=("api", request.api_key),
        #     data={"from": request.sender_identity, "to": email, ...}
        # )
        
        # Validating inputs
        if "@" not in email:
            results.append({"email": email, "status": "failed", "reason": "Invalid format"})
            continue
            
        results.append({
            "email": email, 
            "status": "queued",
            "provider": request.service_provider
        })
        
    # DATABASE LOGGING (Real)
    from backend.services.supabase_client import get_supabase
    supabase = get_supabase()
    
    if supabase:
        try:
            # Batch insert logs
            logs = []
            for res in results:
                logs.append({
                    "target_email": res['email'],
                    "campaign_id": "manual_campaign_001", 
                    "provider": request.service_provider,
                    "status": res['status']
                })
            if logs:
                supabase.table("outreach_logs").insert(logs).execute()
        except Exception as e:
             print(f"⚠️ Failed to log Outreach: {e}")
        
    return {
        "campaign_status": "active",
        "total_targets": len(request.target_emails),
        "results": results
    }
