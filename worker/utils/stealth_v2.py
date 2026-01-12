import random
import json

class StealthContextV2:
    """
    THE GHOST LAYER - SUPREME STEALTH (v2026)
    Bypassing Cloudflare, Datadome, and Akamai.
    """
    
    @staticmethod
    async def apply_advanced_stealth(page, user_agent=None):
        """
        GUERILLA MODE: Syncs signatures to UA and adds deep behavioral noise.
        """
        # Determine Platform/OS from UA
        platform = "Win32"
        languages = ["en-US", "en"]
        
        if user_agent:
            if "iPhone" in user_agent:
                platform = "iPhone"
            elif "Android" in user_agent:
                platform = "Linux armv8l"
            elif "Macintosh" in user_agent:
                platform = "MacIntel"
            elif "Windows" in user_agent:
                platform = "Win32"

        # 1. Signature Sync (Remove Inconsistency Flags)
        await page.add_init_script(f"""
            Object.defineProperty(navigator, 'platform', {{ get: () => '{platform}' }});
            Object.defineProperty(navigator, 'languages', {{ get: () => ['en-US', 'en'] }});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => {random.choice([4, 8, 12, 16])} }});
            Object.defineProperty(navigator, 'deviceMemory', {{ get: () => {random.choice([8, 16, 32])} }});
            Object.defineProperty(navigator, 'vendor', {{ get: () => 'Google Inc.' }});
        """)

        # 2. Canvas Fingerprint Noise (Dynamic & Non-Repeating)
        await page.add_init_script("""
            const originalToBlob = HTMLCanvasElement.prototype.toBlob;
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;

            const addNoise = (data) => {
                const shift = Math.floor(Math.random() * 2) - 1; // -1, 0, or 1
                for (let i = 0; i < data.length; i += 4) {
                    data[i] = Math.min(255, Math.max(0, data[i] + shift));
                }
            };

            CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {
                const res = originalGetImageData.apply(this, arguments);
                addNoise(res.data);
                return res;
            };
        """)

        # 3. WebGL Mocking (Sync to Platform)
        vendor, renderer = ("Intel Inc.", "Intel Iris OpenGL Engine")
        if "iPhone" in platform:
            vendor, renderer = ("Apple Inc.", "Apple GPU")
        
        await page.add_init_script(f"""
            const getParam = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return '{renderer}';
                if (parameter === 37446) return '{vendor}';
                return getParam(parameter);
            }};
        """)

        # 4. Mask Automation Tell (The #1 Kill-switch)
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            
            // Overwrite CDP detection
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        """)

    @staticmethod
    async def enact_human_behavior(page):
        """
        Performs non-linear mouse movements and variable scrolling.
        """
        # Random viewport jitter
        width = 1280 + random.randint(-50, 50)
        height = 720 + random.randint(-50, 50)
        await page.set_viewport_size({"width": width, "height": height})
        
        # Natural scroll with variable velocity
        for _ in range(random.randint(2, 5)):
            pixels = random.randint(300, 800)
            steps = 5
            for i in range(steps):
                await page.mouse.wheel(0, pixels // steps)
                await page.wait_for_timeout(random.randint(50, 150))
            await page.wait_for_timeout(random.randint(500, 1500))

stealth_v2 = StealthContextV2()
