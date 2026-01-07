import asyncio
import os
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

print("INIT: Starting Engine Verification Script...")

try:
    from playwright.async_api import async_playwright
    print("INIT: Playwright imported successfully.")
except ImportError:
    print("CRITICAL: Playwright not installed.")
    sys.exit(1)

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scrapers.google_maps_engine import GoogleMapsEngine
    from scrapers.base_dork_engine import BaseDorkEngine
    print("INIT: Engine classes imported.")
except ImportError as e:
    print(f"CRITICAL: Engine import failed: {e}")
    sys.exit(1)

async def verify_google_maps():
    print("\n--- TEST 1: Verifying Google Maps Engine ---")
    async with async_playwright() as p:
        print("BROWSER: Launching Chromium (Headless)...")
        try:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            print("BROWSER: Launched.")
            page = await browser.new_page()
            
            engine = GoogleMapsEngine(page)
            query = "coffee shops in San Francisco"
            print(f"ACTION: Scraping '{query}'...")
            
            results = await engine.scrape(query)
            if results and len(results) > 0:
                print(f"✅ SUCCESS: Retrieved {len(results)} results")
                print(f"SAMPLE DATA: {results[0]}")
            else:
                print("❌ FAILURE: Zero results returned")
                # Dump content to see why
                content_len = len(await page.content())
                print(f"DEBUG: Page Content Length: {content_len} bytes")
                
            await browser.close()
        except Exception as e:
            print(f"❌ EXECUTION ERROR: {e}")

async def verify_dork_engine():
    print("\n--- TEST 2: Verifying Base Dork Engine ---")
    async with async_playwright() as p:
        print("BROWSER: Launching Chromium...")
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        
        engine = BaseDorkEngine(page, "linkedin_test")
        query = "software engineer"
        site_filter = "linkedin.com/in/" 
        
        print(f"ACTION: Searching '{query}' on {site_filter}...")
        
        try:
            results = await engine.run_dork_search(query, site_filter)
            if results and len(results) > 0:
                print(f"✅ SUCCESS: Retrieved {len(results)} results")
                print(f"SAMPLE DATA: {results[0]}")
            else:
                print("❌ FAILURE: Zero results returned")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
        await browser.close()

async def main():
    print("MAIN: Starting tests...")
    await verify_google_maps()
    await verify_dork_engine()
    print("MAIN: All tests completed.")

if __name__ == "__main__":
    print("SCRIPT: Calling main()")
    asyncio.run(main())

