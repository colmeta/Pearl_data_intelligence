import os
import sys
from dotenv import load_dotenv
from google import genai

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Critical: GEMINI_API_KEY not found in .env")
    sys.exit(1)

print(f"🔍 Diagnosing available models for key: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    
    print("\n--- Available Models ---")
    models = client.models.list()
    for m in models:
        print(f"✅ {m.name}")
    
    print("\n--- Testing Content Generation (8b) ---")
    try:
        resp = client.models.generate_content(
            model='gemini-1.5-flash-8b',
            contents='Hi'
        )
        print(f"🚀 Success (8b): {resp.text}")
    except Exception as e:
        print(f"❌ Failed (8b): {e}")

except Exception as e:
    print(f"❌ Diagnostic Failed: {e}")
