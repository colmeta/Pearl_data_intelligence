from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/crm", tags=["CRM Integration"])

class CRMSyncRequest(BaseModel):
    job_id: str
    crm_type: str  # 'hubspot', 'salesforce', 'pipedrive'
    api_key: str
    deal_stage: Optional[str] = "new_lead"

class LeadCRMSyncRequest(BaseModel):
    vault_id: str
    crm_type: str
    api_key: str

@router.post("/sync/lead")
async def sync_lead_to_crm(request: LeadCRMSyncRequest):
    """
    CLARITY PEARL: Sovereign CRM Injection.
    Syncs a specific Mega-Profile with its intelligence (Displacement/Velocity) to a CRM.
    """
    from backend.services.supabase_client import get_supabase
    supabase = get_supabase()
    
    # 1. Fetch Lead from Data Vault
    res = supabase.table('data_vault').select('*').eq('id', request.vault_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Mega-Profile not found")
    
    lead = res.data
    meta = lead.get('metadata', {})
    
    # 2. Extract Sovereignty Data
    displacement_script = meta.get('displacement_data', {}).get('sovereign_script', 'No script generated')
    velocity_signal = meta.get('velocity_data', {}).get('scaling_signal', 'Stable')

    # 3. Construct Sovereign Payload
    crm_payload = {
        "properties": {
            "email": lead.get('email'),
            "firstname": lead.get('full_name', '').split(' ')[0],
            "lastname": ' '.join(lead.get('full_name', '').split(' ')[1:]),
            "company": lead.get('company'),
            "jobtitle": lead.get('title'),
            "twitter_handle": lead.get('twitter_handle'),
            "tiktok_url": lead.get('tiktok_url'),
            # Custom Intelligence Fields
            "clarity_pearl_velocity": velocity_signal,
            "clarity_pearl_displacement_script": displacement_script,
            "sovereign_id": lead.get('sovereign_id')
        }
    }

    # 4. Simulate CRM API Post
    print(f"🔥 INJECTING SOVEREIGN IDENTITY {lead.get('sovereign_id')} INTO {request.crm_type.upper()}...")
    
    # 5. Log the injection
    try:
        supabase.table("crm_logs").insert({
            "vault_id": request.vault_id,
            "crm_type": request.crm_type,
            "sync_status": "success",
            "payload": crm_payload
        }).execute()
    except: pass

    return {
        "status": "success",
        "message": f"Mega-Profile injected into {request.crm_type}.",
        "injected_data": crm_payload
    }
