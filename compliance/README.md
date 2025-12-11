# The Shield (Compliance)

## Mission
To allow "White Hat" scraping by giving users control over their data.

## Features
1.  **Opt-Out Portal:** A static HTML site hosted on `privacy.clarity-pearl.com` (or Netlify/Vercel).
2.  **Hasher:** A script to turn "ceo@example.com" into `a1b2...` so we can check against it without storing the actual banned email list in plaintext.
3.  **Provenance:** (To Be Implemented) A system to sign every JSON result with a "Legal Ticket".

## Usage
*   Host the `opt_out_portal` folder on any static host.
*   Integrate `hasher.py` into the Backend API during record insertion.
