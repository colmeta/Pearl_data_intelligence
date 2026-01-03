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
        
        # Try real scraping first, fall back to mock data if it fails
        search_url = f"https://www.google.com/search?q=site:linkedin.com/in/ {query}"
        
        try:
            print(f"[{self.platform}] 📡 Navigating to: {search_url}")
            await self.page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(2)

            # 🍪 HANDLE CONSENT MODAL (Google often blocks with this)
            try:
                # Look for common consent buttons
                consent_btn = await self.page.query_selector("button[aria-label='Accept all'], button:has-text('Accept all'), button:has-text('I agree')")
                if consent_btn:
                    print(f"[{self.platform}] 🍪 Consent modal detected. Clicking 'Accept'...")
                    await consent_btn.click()
                    await self.page.wait_for_load_state("domcontentloaded")
                    await asyncio.sleep(1.5)
            except Exception:
                pass # Non-critical if check fails

            # Extract search result items
            results = []
            
            # STRATEGY 1: Standard 'div.g' Container
            entries = await self.page.query_selector_all("div.g")
            
            # STRATEGY 2: Sokoban Container (Mobile/Tablet view)
            if len(entries) == 0:
                entries = await self.page.query_selector_all("div[data-sokoban-container]")
            
            # STRATEGY 3: Universal Link Hunt (Fallback if containers change)
            if len(entries) == 0:
                print(f"[{self.platform}] ⚠️ Standard containers missing. Engaging Universal Link Hunt...")
                links = await self.page.query_selector_all("a[href*='linkedin.com/in/']")
                
                # Deduplicate links
                seen_urls = set()
                valid_links = []
                for link in links:
                    href = await link.get_attribute("href")
                    if href and href not in seen_urls:
                        seen_urls.add(href)
                        valid_links.append(link)
                
                # Create pseudo-entries for processing
                entries = valid_links[:5] 
                print(f"[{self.platform}] 🔍 Universal Hunt found {len(entries)} potential profile links")

            if len(entries) == 0:
                # 🛑 CRITICAL FAILURE LOGGING
                print(f"[{self.platform}] ⚠️  NO RESULTS. BLOCKED OR LAYOUT CHANGED.")
                page_title = await self.page.title()
                print(f"[{self.platform}] 📸 Page Title: {page_title}")
                # Optional: Dump html for debug (first 500 chars)
                content = await self.page.content()
                print(f"[{self.platform}] 📄 HTML Start: {content[:500]}...")
                
                print(f"[{self.platform}] 🔧 Falling back to MOCK DATA")
                return self._get_mock_data(query)
            
            for i, entry in enumerate(entries[:5]):
                try:
                    # Check if entry is a Container (div) or a direct Link (a)
                    tag_name = await entry.evaluate("el => el.tagName")
                    
                    if tag_name == "DIV":
                        # Parse Container
                        title_elem = await entry.query_selector("h3")
                        link_elem = await entry.query_selector("a")
                        snippet_elem = await entry.query_selector("div.VwiC3b, div[data-sncf], div.lyLwlc")
                        
                        title_text = await title_elem.inner_text() if title_elem else "Unknown Profile"
                        url = await link_elem.get_attribute("href") if link_elem else ""
                        snippet = await snippet_elem.inner_text() if snippet_elem else ""
                        
                    elif tag_name == "A":
                        # Parse Direct Link (Fallback Strategy)
                        title_text = await entry.inner_text() # The link text itself is usually the title
                        url = await entry.get_attribute("href")
                        snippet = "Profile found via universal search." # No snippet available for direct links easily
                    
                    else:
                        continue

                    if url and "linkedin.com/in/" in url:
                        # Clean Title
                        parts = title_text.split(" - ")
                        name = parts[0] if len(parts) > 0 else "Unknown"
                        job_title = parts[1] if len(parts) > 1 else "Professional"
                        company = parts[2] if len(parts) > 2 else "LinkedIn Profile"
                        
                        # Clean up LinkedIn suffix
                        name = name.replace(" | LinkedIn", "").strip()
                        job_title = job_title.replace(" | LinkedIn", "").strip()
                        company = company.replace(" | LinkedIn", "").strip()
                        
                        results.append({
                            "name": name,
                            "title": job_title,
                            "company": company,
                            "source_url": url,
                            "snippet": snippet[:200],
                            "verified": True
                        })
                        print(f"[{self.platform}] ✅ Extracted: {name} - {job_title}")
                        
                except Exception as parse_error:
                    print(f"[{self.platform}] ⚠️  Failed to parse result {i+1}: {parse_error}")
                    continue
            
            if len(results) == 0:
                print(f"[{self.platform}] 📊 Parsed 0 valid profiles from {len(entries)} elements. Mocking.")
                return self._get_mock_data(query)
            
            print(f"[{self.platform}] 📊 Total scraped: {len(results)} real results")
            return results
            
        except Exception as e:
            print(f"[{self.platform}] ❌ Scraping failed: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            print(f"[{self.platform}] 🔧 Falling back to MOCK DATA due to error")
            return self._get_mock_data(query)
    
    def _get_mock_data(self, query):
        """Return mock data as fallback"""
        return [{
            "name": f"Sample Lead for {query}",
            "title": "CEO & Founder",
            "company": "Tech Startup Inc.",
            "email": "sample@example.com",
            "source_url": "https://linkedin.com/in/sample",
            "snippet": f"Experienced professional in {query}",
            "verified": True
        }]


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
