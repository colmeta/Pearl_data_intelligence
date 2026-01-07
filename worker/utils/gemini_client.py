import os
import requests
import json
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """
    CLARITY PEARL ARBITER - GEMINI REST INTEGRATION
    Lightweight implementation using direct HTTP API to save RAM (Render 512MB Limit).
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found in environment.")
        
        # Using Gemini 1.5 Flash for speed and cost efficiency
        self.model = 'gemini-1.5-flash' 
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def _call_api(self, prompt, image_path=None):
        """
        Internal helper to call Gemini API via HTTP.
        """
        if not self.api_key:
            print("❌ API Call Failed: No API Key")
            return None

        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        contents = []
        parts = [{"text": prompt}]

        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    b64_data = base64.b64encode(img_file.read()).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": b64_data
                    }
                })
            except Exception as e:
                print(f"⚠️ Failed to load image for vision: {e}")

        contents.append({"parts": parts})
        payload = {"contents": contents}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Extract text
            try:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            except (KeyError, IndexError):
                print(f"❌ Unexpected API Response format: {result}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Gemini API Network Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return None

    def _clean_json(self, text):
        """Helper to strip markdown code blocks from JSON response."""
        if not text: return None
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return clean.strip()

    async def analyze_visuals(self, query, image_path):
        """
        VISION-X: Analyze a screenshot using Gemini Vision.
        """
        prompt = f"""
        Analyze this screenshot for the query: {query}.
        CURRENT TIME (REFERENCE): {datetime.now().strftime('%Y-%m-%d')}
        Extract the primary data point (name, price, or social handle).
        TEMPORAL CHECK: If this is an offer/news, check for dates. Is it stale?
        Determine the 'truth_score' (0-100) based on how well it matches the query AND how fresh it is.
        Provide a short 'verdict'.
        Return ONLY a JSON object: {{"truth_score": int, "verdict": "string"}}
        """
        
        # Note: Since we are using requests (blocking), wrapping it in async logic if needed, 
        # but for this script simpler is better. The worker uses asyncio, so ideally we'd use aiohttp,
        # but requests is robust. We'll run it synchronously for now as it's quick.
        resp_text = self._call_api(prompt, image_path)
        return resp_text

    async def verify_data(self, query, data_payload, search_context=""):
        """
        Ask the AI to verify if the scraped data matches the query and feels 'Truthful'.
        """
        prompt = f"""
        You are the CLARITY PEARL ARBITER, a supreme data verification agent.
        
        TARGET SEARCH QUERY: {query}
        CURRENT TIME (REFERENCE): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        SCRAPED DATA (JSON): {data_payload}
        SEARCH RESULTS CONTEXT: {search_context}
        
        TASK:
        1. Compare the scraped data against the query and search context.
        2. Identify any hallucinations or stale information.
        3. Assign a 'Truth Score' from 0 to 100.
        4. Provide a brief 'Verdict' explaining the score.
        
        FORMAT YOUR RESPONSE AS JSON:
        {{
            "truth_score": int,
            "verdict": "string",
            "is_verified": bool (true if score > 75)
        }}
        """
        
        resp_text = self._call_api(prompt)
        if not resp_text: return None
        
        try:
            return json.loads(self._clean_json(resp_text))
        except Exception:
            return None

    async def generate_outreach(self, lead_data, platform="email"):
        """
        GHOSTWRITER: Draft personalized outreach based on verified data.
        """
        prompt = f"""
        You are THE GHOSTWRITER, a elite corporate negotiator.
        LEAD DATA: {lead_data}
        PLATFORM: {platform}
        
        TASK:
        Draft a high-conversion, hyper-personalized outreach message. 
        Refer to their specific title, company, and any signals (hiring, news, location).
        Keep it brief, professional, and slightly provocative.
        
        Return ONLY the text of the message.
        """
        
        text = self._call_api(prompt)
        return text if text else "Failed to generate personalization."

    async def dispatch_mission(self, user_prompt):
        """
        THE ORACLE: Convert NL prompt into structured mission steps.
        """
        prompt = f"""
        You are THE ORACLE, the supreme intelligence of the CLARITY PEARL.
        CURRENT TIME: {datetime.now().strftime('%Y-%m-%d')}
        USER PROMPT: "{user_prompt}"
        
        TASK:
        Decompose this prompt into a search MISSION. A perfect mission uses multiple platforms 
        in synergy to verify and enrich data.
        
        SYNERGY RULES:
        1. For B2B/People: Start with 'linkedin', verify with 'google_news'.
        2. For Local/Physical: Start with 'google_maps', enrich with 'facebook' or 'tiktok'.
        3. For Technical: Use 'reddit' and 'generic'.
        
        Supported Platforms: linkedin, google_news, amazon, real_estate, job_scout, reddit, tiktok, facebook, google_maps, generic.
        Supported Compliance Modes: standard, strict, gdpr.
        
        RETURN ONLY A JSON LIST OF JOBS:
        [
            {{
                "query": "Full search query for this step",
                "platform": "platform_name",
                "compliance_mode": "standard|strict|gdpr",
                "boost": boolean (true for high priority/initial steps),
                "reasoning": "Briefly why this platform was chosen"
            }}
        ]
        """
        
        resp_text = self._call_api(prompt)
        if not resp_text: return []
        
        try:
            cleaned = self._clean_json(resp_text)
            return json.loads(cleaned)
        except Exception as e:
            print(f"❌ Oracle Dispatch Parse Error: {e}\nResponse: {resp_text}")
            return []

gemini_client = GeminiClient()
