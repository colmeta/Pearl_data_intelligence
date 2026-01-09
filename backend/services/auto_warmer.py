import asyncio
import json
from datetime import datetime
from backend.services.supabase_client import get_supabase

class AutoWarmer:
    """
    THE ETERNAL FORGE: Autonomous Lead Warming
    Monitors growth velocity and automatically drafts outreach for viral leads.
    """
    
    def __init__(self):
        self.supabase = get_supabase()
        self.check_interval = 300 # Check every 5 minutes
        self.velocity_threshold = 50 # 50% growth trigger

    async def start(self):
        print("🔥 Auto-Warmer: Ignition sequence complete. Monitoring for viral growth...")
        while True:
            try:
                await self.process_viral_leads()
            except Exception as e:
                print(f"⚠️ Auto-Warmer Error: {e}")
            await asyncio.sleep(self.check_interval)

    async def process_viral_leads(self):
        """
        Scans data_vault for leads with high growth velocity.
        """
        # 1. Fetch leads with high growth or viral signals
        # We look for metadata -> velocity_data -> growth_rate_pct > threshold
        res = self.supabase.table('data_vault').select('*').execute()
        
        if not res.data: return
        
        viral_leads = []
        for lead in res.data:
            meta = lead.get('metadata', {})
            vel = meta.get('velocity_data', {})
            growth = vel.get('growth_rate_pct', 0)
            signal = vel.get('scaling_signal', '')
            
            if growth >= self.velocity_threshold or signal == 'Viral Spike':
                viral_leads.append(lead)

        if not viral_leads: return

        print(f"🚀 Auto-Warmer: Found {len(viral_leads)} viral opportunities. Drafting scripts...")

        for lead in viral_leads:
            # 2. Check if we already drafted for this email
            email = lead.get('email')
            if not email: continue
            
            check = self.supabase.table('outreach_logs').select('id').eq('target_email', email).limit(1).execute()
            if check.data: continue # Skip if already in system

            # 3. Draft the script using displacement data from metadata
            displacement = lead.get('metadata', {}).get('displacement_data', {})
            script = displacement.get('sovereign_script')
            
            if not script: continue

            # 4. Insert into outreach_logs as 'draft'
            draft_payload = {
                "target_email": email,
                "provider": "clarity_pearl_auto",
                "status": "drafted",
                "campaign_id": "auto_warmer_v1",
                "sent_at": None # It's a draft
            }
            
            try:
                self.supabase.table('outreach_logs').insert(draft_payload).execute()
                print(f"✅ Auto-Warmer: Drafted outreach for {email} (Growth: {lead.get('metadata', {}).get('velocity_data', {}).get('growth_rate_pct')}%)")
            except Exception as e:
                print(f"⚠️ Auto-Warmer: Failed to draft for {email}: {e}")

auto_warmer = AutoWarmer()
