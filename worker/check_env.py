import sys
import os

results = []

try:
    import playwright
    results.append("✅ Playwright: FOUND")
except ImportError:
    results.append("❌ Playwright: NOT FOUND")

try:
    import dns
    results.append("✅ dnspython: FOUND")
except ImportError:
    results.append("❌ dnspython: NOT FOUND")

try:
    import requests
    results.append("✅ requests: FOUND")
except ImportError:
    results.append("❌ requests: NOT FOUND")

try:
    import supabase
    results.append("✅ supabase: FOUND")
except ImportError:
    results.append("❌ supabase: NOT FOUND")

results.append(f"Executable: {sys.executable}")
results.append(f"CWD: {os.getcwd()}")

with open("env_check.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("Environment check complete. Results written to env_check.txt")
