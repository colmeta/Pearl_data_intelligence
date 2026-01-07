import asyncio
import os
import sys
from dotenv import load_dotenv

# Add current dir to path
sys.path.append(os.getcwd())

load_dotenv()

print("--- ORACLE DEBUGGER ---")

# 1. Check Env Vars
print(f"GEMINI_API_KEY Present: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"SUPABASE_URL Present: {bool(os.getenv('SUPABASE_URL'))}")
print(f"SUPABASE_KEY Present: {bool(os.getenv('SUPABASE_KEY'))}")

async def test_oracle():
    print("\n--- Testing Gemini Client ---")
    try:
        from worker.utils.gemini_client import gemini_client
        prompt = "CEO in Austin"
        print(f"Dispatching prompt: '{prompt}'")
        
        jobs = await gemini_client.dispatch_mission(prompt)
        print(f"Result (Jobs): {jobs}")
        
        if not jobs:
            print("❌ FAILURE: Gemini returned empty list. Likely API Key issue or model error.")
            return

        print("✅ SUCCESS: Gemini produced a mission plan.")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR (Gemini): {e}")

    print("\n--- Testing Supabase Connection ---")
    try:
        from backend.services.supabase_client import get_supabase
        supabase = get_supabase()
        
        if not supabase:
             print("❌ FAILURE: Supabase client is None.")
             return

        # Try a simple select to verify connection
        print("Attempting to list organizations (limit 1)...")
        # Note: This might fail if RLS prevents anonymous read, but let's see.
        # In the backend, this runs with the service role (usually). 
        # But 'supabase_client.py' uses SUPABASE_KEY which is usually the anon key?
        # Let's check what key is being used.
        res = supabase.table('organizations').select('id, name').limit(1).execute()
        print(f"Supabase Response: {res.data}")
        print("✅ SUCCESS: Supabase connection verified.")

    except Exception as e:
         print(f"❌ CRITICAL ERROR (Supabase): {e}")

if __name__ == "__main__":
    asyncio.run(test_oracle())
