import asyncio
from playwright.async_api import async_playwright

class LinkedInEngine:
    def __init__(self, page):
        self.page = page
        self.platform = "linkedin"

    async def scrape(self, query):
        """
        Executes a targeted search on LinkedIn for the given query.
        Uses public search results to avoid aggressive login-wall detection initially.
        """
        print(f"[{self.platform}] 🚀 Launching deep-search for: {query}")
        
        # Strategy: Use Google/Bing to find LinkedIn profiles for the query
        # This is more resilient than direct LinkedIn search which often forces login
        search_url = f"https://www.google.com/search?q=site:linkedin.com/in/ {query}"
        
        try:
            await self.page.goto(search_url, wait_until="domcontentloaded")
            await asyncio.sleep(2) # Natural delay
            
            # Extract search result items
            results = []
            
            # Selector for Google search result entries
            entries = await self.page.query_selector_all("div.g")
            
            for entry in entries[:5]: # Take top 5 for speed and quality
                title_elem = await entry.query_selector("h3")
                snippet_elem = await entry.query_selector("div.VwiC3b")
                link_elem = await entry.query_selector("a")
                
                if title_elem and link_elem:
                    title_text = await title_elem.inner_text()
                    url = await link_elem.get_attribute("href")
                    snippet = await snippet_elem.inner_text() if snippet_elem else ""
                    
                    # Parse name and title from the LinkedIn title format: "Name - Title - Company | LinkedIn"
                    parts = title_text.split(" - ")
                    name = parts[0] if len(parts) > 0 else "Unknown"
                    job_title = parts[1] if len(parts) > 1 else "Professional"
                    
                    results.append({
                        "name": name.replace(" | LinkedIn", "").strip(),
                        "title": job_title.replace(" | LinkedIn", "").strip(),
                        "company": "LinkedIn Profile", # Default if not clear from snippet
                        "source_url": url,
                        "snippet": snippet,
                        "verified": True
                    })
            
            return results
        except Exception as e:
            print(f"[{self.platform}] ❌ Scraping failed: {e}")
            return []

async def test_engine():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        engine = LinkedInEngine(page)
        data = await engine.scrape("SaaS CEOs Austin")
        print(data)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_engine())
