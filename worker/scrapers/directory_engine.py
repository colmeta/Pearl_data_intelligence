from scrapers.base_dork_engine import BaseDorkEngine
import asyncio

class DirectoryEngine:
    """
    CLARITY PEARL - GLOBAL DIRECTORY ENGINE
    Mission: Extract business data from Yellow Pages, Yelp, and niche industry directories.
    """
    def __init__(self, page):
        self.page = page
        self.dork_engine = BaseDorkEngine(page, "directory")

    async def scrape(self, query):
        """
        Unified directory search using targeted dorking.
        """
        print(f"📡 Clarity Pearl: Crawling Global Directories for '{query}'...")
        
        # 1. Yellow Pages Dork
        yp_results = await self.dork_engine.run_dork_search(f'"{query}"', "yellowpages.com")
        
        # 2. Yelp / Local Dork
        yelp_results = await self.dork_engine.run_dork_search(f'"{query}"', "yelp.com")
        
        # 3. Industry Specific (e.g., Angi, Houzz if applicable)
        # We use a broad "GMB" helper dork
        gmb_results = await self.dork_engine.run_dork_search(f'"{query}" listing', "business.site")
        
        all_results = yp_results + yelp_results + gmb_results
        
        for r in all_results:
            r["category"] = "directory"
            r["source_platform"] = "directory_hub"
            
        print(f"✅ Clarity Pearl: Found {len(all_results)} directory listings.")
        return all_results
