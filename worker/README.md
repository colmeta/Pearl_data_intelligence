# The Hydra (Local Worker)

## Mission
To scrape data using YOUR local internet connection and IP address, bypassing cloud blocklists.

## Setup
1.  **Install Python 3.10+**
2.  **Install Dependencies:**
    ```bash
    pip install playwright supabase
    playwright install chromium
    ```

## Usage
Run the controller:
```bash
python hydra_controller.py
```

## Architecture
*   `hydra_controller.py`: Connects to Supabase, asks "Are there queued jobs?", and directs the engines.
*   `scrapers/engines.py`: Contains the actual Playwright logic (currently simulated) to browser the web.

## Why Local?
*   **0 Cost:** Uses your existing internet.
*   **High Trust:** Residential IPs (your home Wi-Fi) are trusted by LinkedIn/Google much more than AWS IPs.
