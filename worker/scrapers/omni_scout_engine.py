import asyncio
import re
import urllib.parse
from datetime import datetime
from scrapers.base_dork_engine import BaseDorkEngine

class OmniScoutEngine:
    """
    CLARITY PEARL - OMNI-PLATFORM SCOUT
    Unified engine for Product Hunt, TikTok, Amazon, and Shopify.
    """
    def __init__(self, page):
        self.page = page
        self.dork_engine = BaseDorkEngine(page, "omni_scout")

    async def scrape_product_hunt(self, query):
        """
        Deep Scrape for Product Hunt: Finds products and MIKER/DEVELOPER links.
        """
        print(f"📡 Clarity Pearl: Scouring Product Hunt for '{query}'...")
        # Strategy: Dork for the post, then visit and extract makers if possible or dork for makers
        dork_results = await self.dork_engine.run_dork_search(f'"{query}"', "producthunt.com/posts")
        
        enriched_results = []
        for res in dork_results[:5]: # Top 5 for performance
            try:
                # Attempt to find the "Maker" via a secondary dork to avoid heavy JS on PH direct
                # site:producthunt.com "Post Title" maker
                maker_dork = await self.dork_engine.run_dork_search(f'"{res["name"]}" maker', "producthunt.com")
                if maker_dork:
                    res["maker_details"] = maker_dork[0]["name"]
                    res["snippet"] += f" | Maker: {maker_dork[0]['name']}"
                
                res["category"] = "marketplace"
                enriched_results.append(res)
            except:
                enriched_results.append(res)
        
        return enriched_results

    async def scrape_tiktok_bio(self, query):
        """
        TikTok Bio Hunter: Finds influencers/brands and extracts emails from bios.
        """
        print(f"📡 Clarity Pearl: Hunting TikTok Bios for '{query}'...")
        # site:tiktok.com "@" email "query"
        dork_query = f'site:tiktok.com "@{query}" email'
        results = await self.dork_engine.run_dork_search(dork_query, "tiktok.com")
        
        for r in results:
            r["category"] = "social"
            # Regex for email in snippet
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', r["snippet"])
            if emails:
                r["email"] = emails[0]
                r["snippet"] += " | [EMAIL EXTRACTED]"
        
        return results

    async def scrape_ecommerce_discovery(self, query):
        """
        Shopify & Amazon Store Scout.
        """
        print(f"📡 Clarity Pearl: Discovering E-commerce Hubs for '{query}'...")
        # Shopify dork: site:myshopify.com "query"
        shopify_results = await self.dork_engine.run_dork_search(query, "myshopify.com")
        
        # Amazon Seller dork: site:amazon.com "seller profile" "query"
        amazon_results = await self.dork_engine.run_dork_search(f'"seller profile" {query}', "amazon.com")
        
        all_res = shopify_results + amazon_results
        for r in all_res:
            r["category"] = "ecommerce"
        
        return all_res

    async def unified_scout(self, query, platforms=["ph", "tiktok", "ecomm"]):
        """
        Runs all requested scouts in parallel.
        """
        tasks = []
        if "ph" in platforms: tasks.append(self.scrape_product_hunt(query))
        if "tiktok" in platforms: tasks.append(self.scrape_tiktok_bio(query))
        if "ecomm" in platforms: tasks.append(self.scrape_ecommerce_discovery(query))
        
        results = await asyncio.gather(*tasks)
        # Flattening
        return [item for sublist in results for item in sublist]
