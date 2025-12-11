# CLARITY PEARL - MVP SPECIFICATION (v2.0)
## "The Fortress of Truth" (BOOTSTRAP EDITION)

---

## 1. PRODUCT VISION
Build the **"Sensory Feed"** API and Dashboard. A system that doesn't just scrape, but **verifies** and **certifies** data for AI consumption.

**Core Philosophy:** "Better 10 verified records than 10,000 hallucinations."

**Constraint:** 512MB RAM (Render Free Tier) & Zero Budget.
**Strategy:** "Distributed Hybrid Engine" = Cloud API (Render) + Local Worker (Founder's PC).

---

## 2. THE "UNSTOPPABLE" ARCHITECTURE (FREE TIER)

### Component A: The Cloud Brain (Render - Free Tier)
*   **Role:** Orchestration & API. NO BROWSERS HERE.
*   **Tech:** FastAPI (Python) running on 512MB RAM.
*   **Function:**
    1.  Receives user request (e.g., "Get me leads").
    2.  Check Database (Supabase Free Tier) for cache.
    3.  If miss, places job in **Queue** (Redis/Upstash).
    4.  Serves the Frontend Dashboard (Static Site).

### Component B: The Hydra (Distributed)
*   **Head 1 (Local):** Founder's Laptop (High Trust, Manual).
*   **Head 2 (Cloud CI):** GitHub Actions (Zero Cost, Automated, Medium Trust).
*   **Logic:** GitHub Actions runs every 30 mins to clear small jobs. If it gets blocked (403), the Local Worker picks up the slack.

### Component C: The DataVault (Supabase - Free Tier)
*   **Role:** Storage.
*   **Limit:** 500MB Database size (plenty for text/JSON).

---

## 3. MVP FEATURE SET (The "Must Haves")

### 1. The "Compliance Shield" Portal
*   **Feature:** A public-facing URL (`privacy.clarity-pearl.com`).
*   **Function:** Allows any individual to input their email/phone and **Opt-Out** globally from our DB.
*   **Why:** This is our legal defense. "We offer an immediate opt-out."

### 2. The "Clarity Dashboard"
*   **Input:** Search Bar. "SaaS Companies in Miami."
*   **Output:** A list of records, but with a **green checkmark** (Arbiter Verified).
*   **Export:** JSON-LD (for AI Agents), CSV (for humans).

### 3. API First Design
*   **Endpoint:** `POST /api/v1/sensory/feed`
*   **Payload:** `{ "query": "Sales Leaders", "compliance_mode": "strict" }`
*   **Response:** `{ "data": [...], "provenance": [...] }`

---

## 4. TECHNICAL STACK (The "Iron Stack" - Free)

*   **Backend:** FastAPI (Python) - Render Web Service (Free).
*   **Database:** Supabase (PostgreSQL) - Free Tier.
*   **Queue:** Upstash (Serverless Redis) - Free Tier.
*   **Browser Infra:** **YOUR LOCAL MACHINE** (Acts as a self-hosted worker).
*   **Proxies:** 
    *   *Start:* Free Proxy Lists (Unstable but free).
    *   *Upgrade:* PacketStream ($1/GB - very cheap). 
    *   *Nuclear Fallback:* Use your local IP (carefully).

---

## 5. SUCCESS CRITERIA (30 Days)

1.  **Resilience:** The "Hydra" must successfully scrape LinkedIn 100 times without a hard block.
2.  **Truth:** The "Arbiter" must catch at least 20% of stale data that a normal scraper would have missed.
3.  **Speed:** < 5 seconds for a "Cached Verified" result.

---

## 6. MVP DEVELOPMENT PLAN (With Antigravity)

*   **Week 1:** Setup Render (API) + Supabase (DB) + Local Worker Script.
*   **Week 2:** Build the **Hydra Controller** (Local Python Script).
*   **Week 3:** Build the basic **Arbiter Agent** (Simple cross-reference logic).
*   **Week 4:** The **Compliance Portal**.

---

**CONFIDENTIAL - CLARITY PEARL**
**APPROVED BY:** The Godfather Strategy Office
