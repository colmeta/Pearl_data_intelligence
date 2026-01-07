import os
import sys
from dotenv import load_dotenv
from google import genai

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Key exists: {bool(api_key)}")

if not api_key:
    print("No key, exiting.")
    sys.exit(1)

print("Initializing client...")
try:
    client = genai.Client(api_key=api_key)
    print("Client initialized. Sending request...")
    
    response = client.models.generate_content(
        model='gemini-1.5-flash-8b',
        contents='Hello, are you online?'
    )
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
