from worker.utils.gemini_client import gemini_client
from backend.services.supabase_client import get_supabase
from backend.dependencies import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

router = APIRouter(prefix="/api/outreach", tags=["Outreach Automation"])

@router.post("/send/{result_id}/")
async def send_automated_outreach(result_id: str, user: dict = Depends(get_current_user)):
    """
    PREMIUM OUTREACH ENGINE: Fetch lead data, draft, and config, then dispatch.
    Supports Resend and Custom SMTP.
    """
    supabase = get_supabase()
    org_id = user.get("org_id")
    
    # 1. Fetch Lead Result and Organization Config
    res = supabase.table('results').select('*, jobs(org_id)').eq('id', result_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Lead result not found")
    
    lead_result = res.data[0]
    draft = lead_result.get('outreach_draft')
    data = lead_result.get('data_payload', {})
    target_email = data.get('email')
    
    if not target_email or not draft:
        raise HTTPException(status_code=400, detail="Missing target email or outreach draft")

    # 2. Fetch Org Settings
    org_res = supabase.table('organizations').select('outreach_config, name').eq('id', org_id).execute()
    if not org_res.data:
         raise HTTPException(status_code=404, detail="Organization not found")
         
    config = org_res.data[0].get('outreach_config', {})
    org_name = org_res.data[0].get('name', 'Clarity Pearl User')
    provider = config.get('provider', 'smtp') # default to smtp if not set
    
    print(f"📧 Dispatching Outreach for {target_email} via {provider}...")
    
    status = "failed"
    error_msg = None
    
    # 3. Provider Logic
    try:
        if provider == 'resend':
            import httpx
            resend_key = config.get('api_key')
            if not resend_key: raise Exception("Missing Resend API Key")
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {resend_key}", "Content-Type": "application/json"},
                    json={
                        "from": config.get('from_email', f"outreach@datavault.app"),
                        "to": target_email,
                        "subject": f"Inquiry from {org_name}",
                        "text": draft
                    }
                )
                if resp.status_code >= 400:
                    raise Exception(f"Resend Error: {resp.text}")
                status = "sent"
        
        elif provider == 'smtp':
            smtp_host = config.get('smtp_host')
            smtp_port = int(config.get('smtp_port', 587))
            smtp_user = config.get('smtp_user')
            smtp_pass = config.get('smtp_pass')
            
            if not all([smtp_host, smtp_user, smtp_pass]):
                raise Exception("Missing SMTP credentials in Org Settings")
                
            msg = MIMEMultipart()
            msg['From'] = config.get('from_email', smtp_user)
            msg['To'] = target_email
            msg['Subject'] = f"Regarding {data.get('company', 'your company')}"
            msg.attach(MIMEText(draft, 'plain'))
            
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            status = "sent"
        else:
            raise Exception(f"Unknown provider: {provider}")

    except Exception as e:
        print(f"❌ Outreach Failed: {e}")
        status = "failed"
        error_msg = str(e)

    # 4. Log and Update Status
    supabase.table('outreach_logs').insert({
        "org_id": org_id,
        "result_id": result_id,
        "target_email": target_email,
        "provider": provider,
        "status": status,
        "error_message": error_msg
    }).execute()
    
    supabase.table('results').update({"outreach_status": status}).eq('id', result_id).execute()
    
    return {"status": status, "provider": provider, "error": error_msg}
@router.post("/ghostwrite/{result_id}/")
async def ghostwrite_lead(result_id: str, platform: str = "email", user: dict = Depends(get_current_user)):
    """
    GHOSTWRITER: Generate a personalized draft for a specific lead.
    """
    supabase = get_supabase()
    res = supabase.table('results').select('*').eq('id', result_id).execute()
    
    if not res.data:
        raise HTTPException(status_code=404, detail="Lead result not found")
        
    lead_data = res.data[0]['data_payload']
    
    draft = await gemini_client.generate_outreach(lead_data, platform)
    
    # Save the draft to the database (optional, for persistence)
    supabase.table('results').update({"outreach_draft": draft}).eq('id', result_id).execute()
    
    return {"draft": draft}
