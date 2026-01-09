from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
from backend.services.supabase_client import get_supabase

router = APIRouter(prefix="/api/billing/flutterwave", tags=["Billing"])

class PaymentRequest(BaseModel):
    org_id: str
    amount: float
    currency: str = "USD"
    email: str

@router.post("/checkout")
async def create_flutterwave_checkout(request: PaymentRequest):
    """
    CLARITY PEARL: Flutterwave Credit Forge (Sandbox Draft)
    Returns a mock checkout URL for testing.
    """
    # IN PRODUCTION: This would call Flutterwave's /payments endpoint
    # to get a link. For now, we simulate.
    
    print(f"💳 Flutterwave Forge: Initiating {request.amount} {request.currency} payment for {request.org_id}")
    
    # Simulate a link
    mock_link = f"https://checkout.flutterwave.com/v3/hosted/pay/mock_{request.org_id}"
    
    return {
        "status": "success",
        "checkout_url": mock_link,
        "message": "Flutterwave checkout draft generated (Status: DISCONNECTED per directive)"
    }

@router.post("/webhook")
async def flutterwave_webhook(request: Request):
    """
    Handles payment verification and credit provisioning.
    """
    # IN PRODUCTION: Verify Flutterwave Signature
    payload = await request.json()
    
    # 1. Check status
    if payload.get('status') == 'successful':
        tx_ref = payload.get('tx_ref') # Should contain org_id_credits_amount
        # Simulate extraction
        # org_id = tx_ref.split('_')[0]
        # credits = int(tx_ref.split('_')[2])
        
        print("💰 Flutterwave Webhook: Payment Verified. Provisioning credits...")
        
        # 2. Update DB (Mocked for now)
        # supabase = get_supabase()
        # supabase.rpc('fn_add_credits', {'p_org_id': org_id, 'p_amount': credits}).execute()
        
    return {"status": "received"}

# NOTE: This router is NOT yet included in main.py per user directive "dont connect it"
