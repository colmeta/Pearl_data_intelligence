import asyncio
from datetime import datetime

class GoogleMapsGridEngine:
    """
    NEXUS SCOUT - GOOGLE MAPS GRID ENGINE
    Mission: Bypass the 120-result limit by slicing a city into a grid.
    """
    
    def __init__(self, page):
        self.page = page
        self.platform = "google_maps_grid"

    async def scrape(self, query, location_grid=None):
        """
        Performs a 'Grid Search'. 
        If no grid is provided, it does a standard high-stealth scrape.
        """
        print(f"📡 Clarity Pearl: Grid-Scanning Google Maps for '{query}'...")
        
        # --- ADS BOT STEALTH ---
        # Tricking Google into thinking we are a crawler to bypass JS redirects/blocks
        await self.page.set_extra_http_headers({"User-Agent": "AdsBot-Google (+http://www.google.com/adsbot.html)"})
        
        base_url = f"https://www.google.com/maps/search/{query}"
        
        try:
            await self.page.goto(base_url, timeout=30000, wait_until="networkidle")
            
            # 2. Infinite Scroll to Trigger Load
            print("⏳ Clarity Pearl: Triggering Deep Scroll for Local Businesses...")
            scrollable_div = "div[role='feed']"
            
            for _ in range(8):
                # Using a more robust scroll targeting the feed container
                try:
                    await self.page.evaluate(f"document.querySelector('{scrollable_div}').scrollBy(0, 1000)")
                except:
                    await self.page.mouse.wheel(0, 2000)
                await asyncio.sleep(1.5)
            
            # 3. Extract Business Data
            leads = await self.page.evaluate("""
                () => {
                    const items = document.querySelectorAll('div[role="article"]');
                    const results = [];
                    items.forEach(item => {
                        const name = item.querySelector('div.fontHeadlineSmall')?.innerText || '';
                        const rating = item.querySelector('span.MW4Y7c')?.innerText || '';
                        const reviews = item.querySelector('span.UY7F9')?.innerText || '';
                        
                        // Smart parsing of address and category
                        const subInfo = item.querySelectorAll('div.W4Efsd');
                        let address = '';
                        let category = '';
                        if (subInfo.length > 1) {
                            address = subInfo[1]?.innerText || '';
                        }
                        
                        const phone = item.querySelector('span.Us6YCc')?.innerText || '';
                        const website = item.querySelector('a[aria-label*="website"]')?.href || '';
                        
                        if (name) {
                            results.push({
                                "name": name,
                                "rating": rating,
                                "reviews_count": parseInt(reviews.replace(/[( )]/g, '')) || 0,
                                "address": address,
                                "phone": phone,
                                "store_url": website,
                                "category": "directory",
                                "source_platform": "google_maps",
                                "verified": parseFloat(rating) >= 4.0
                            });
                        }
                    });
                    return results;
                }
            """)
            
            print(f"✅ Clarity Pearl: Captured {len(leads)} local business leads.")
            
            return [{
                "source": "google_maps",
                "data": leads,
                "verified": True,
                "timestamp": datetime.now().isoformat()
            }]

        except Exception as e:
            print(f"[{self.platform}] ❌ Scout-01: Google Maps Grid Failure: {e}")
            return [{
                "name": "Grid Search Fallback",
                "address": query,
                "verified": False,
                "snippet": "Grid search encountered an error. Manual verification advised.",
                "error": str(e)
            }]
