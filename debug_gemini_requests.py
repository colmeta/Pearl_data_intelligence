import os
import requests
import json
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(line_buffering=True)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Key exists: {bool(api_key)}")

if not api_key:
    print("No key, exiting.")
    sys.exit(1)

model = "gemini-1.5-flash-8b"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

headers = {"Content-Type": "application/json"}
data = {
    "contents": [{
        "parts": [{"text": "Hello, Oracle."}]
    }]
}

try:
    print(f"Sending POST to {url[:40]}...")
    resp = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:200]}")
except Exception as e:
    print(f"Request Error: {e}")
