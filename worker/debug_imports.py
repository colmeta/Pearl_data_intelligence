import sys
import os

print("DEBUG: Script started")
sys.stdout.flush()

try:
    print("DEBUG: Importing async_playwright...")
    from playwright.async_api import async_playwright
    print("DEBUG: Import successful")
except ImportError as e:
    print(f"DEBUG: Import failed: {e}")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("DEBUG: Importing Engines...")
    from scrapers.google_maps_engine import GoogleMapsEngine
    from scrapers.base_dork_engine import BaseDorkEngine
    print("DEBUG: Engine imports successful")
except ImportError as e:
    print(f"DEBUG: Engine import failed: {e}")

print("DEBUG: Pre-flight checks passed.")
