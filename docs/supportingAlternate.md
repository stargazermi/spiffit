help me create a custom gpt that browses the web for SMB internet offers from frontier's competitors.
ChatGPT said:
 
Thought for 14s
Great — I’ll lay out a complete, practical plan and ready-to-paste content you can use to create a custom GPT that browses the web and collects SMB internet offers from Frontier’s competitors (AT&T Business, Spectrum/Charter, Comcast Business, Verizon Business, Cox Business, etc.). I’ll include:
how to configure the Custom GPT (system instructions + browsing settings),
a target list (pages / signals to watch),
reliable monitoring approaches (browsing, change-detection, scraping, APIs) with pros/cons,
legal / security guardrails,
a sample extraction schema + example prompts the GPT can use to return structured offers,
a small Python scraper example you can use as a fallback/verification tool,
and next steps you can ask me to do now (I can generate the config and prompt text).
I used current docs and practical sources while preparing this (OpenAI docs on creating GPTs; guides on competitor monitoring and scraping; Visualping for page-change monitoring; recent ISP comparisons). Sources are cited inline for the most important claims. HighSpeedInternet.com+4OpenAI Help Center+4OpenAI+4
1) High-level design — how your Custom GPT will work
Goal: Automatically browse and extract SMB internet offers from Frontier competitors (plans for businesses — speeds, price, promo, term, eligibility, dedicated/business fiber, SLAs).
Mode: A Custom GPT with Browsing enabled for interactive lookups (user asks “show me current SMB offers near ZIP 12345” → GPT visits target provider pages, extracts offers, returns structured results and links). This is supported in OpenAI’s Custom GPT builder. OpenAI Help Center+1
Where continuous monitoring is needed: Because ChatGPT/GPTs don’t run in the background continuously for you, schedule an external watchdog (cron job, serverless function) to hit the GPT via API or use site-change monitors (Visualping, Distill, etc.) to trigger queries when a page changes. (I’ll show alternatives below.) Visualping
2) Who to monitor (Frontier competitors — SMB / business pages)
Start with these business-facing pages (each has business plans, promos, or dedicated pages):
AT&T Business (Business Fiber & Dedicated Internet) — business pages and local availability lookup. HighSpeedInternet.com
Spectrum Business (Charter) — Business plans & promotions. Deliberate Directions
Comcast Business — Business Internet and Xfinity Business pages. The Network Installers
Verizon Business — fiber and business plans. HighSpeedInternet.com
Cox Business — regional business ISPs and offers. The Network Installers
(You can add regional ISPs where Frontier competes locally.)
3) Where the GPT should look on each site (targets / signals)
For each provider, instruct the GPT to check (in order):
Official business plan page(s) — product pages that list speeds/prices/promos.
Local availability / address-lookup pages — often contain localized offers and pricing by ZIP.
Promotions / deals / specials pages or banners — may be site-wide or time-limited.
Support/FAQ and SLA pages — to capture service-level guarantees and professional add-ons.
Press releases / blog / newsroom — new offers sometimes announced there.
Third-party aggregator pages (only as supplemental signals — they sometimes copy offers).
Change-detection results (Visualping, Distill, RSS) — detect new promotions.
4) Implementation approaches (pros / cons)
A. Custom GPT with browsing enabled (interactive queries)
Pros: Easier to maintain; user-friendly; can be asked follow-ups; uses built-in browsing in GPT builder. OpenAI Help Center
Cons: Not a replacement for continuous scheduled scraping; browsing sessions cost tokens; extraction can be brittle if pages change.
B. Change-detection services + GPT for summarization
Use Visualping/Distill to watch pages and trigger the GPT to fetch and summarize when a change appears. Good for promotions. Visualping
C. Dedicated scraper + structured database + GPT summarizer
Scraper (Scrapy/Requests + BeautifulSoup or commercial scraping services) stores structured offers; GPT converts raw fields into human-friendly summaries & competitive analysis. More robust for large-scale monitoring. Scrapfly+1
D. APIs / partner data
If any provider or a third-party aggregator offers an API, use it — stable and less brittle. (This is rare for ISP retail promos but check local aggregator partners.)
5) Legal & safety / operational guardrails (important)
Respect robots.txt and terms of service. Scraping pages that explicitly disallow bots may be unlawful or breach terms. Use official APIs where possible. Scrapfly
Do not collect or store PII (customer names, account numbers) — only public offer data.
Rate-limit and use polite crawling (delay between requests, identify agent). Use proxies responsibly. Soax
Security of custom GPT content: Don’t upload secret keys or proprietary internal docs into the GPT configuration — there have been reported risks of custom GPTs leaking setup instructions if not hardened. Keep sensitive logic on your server and only pass non-sensitive prompts. WIRED
6) Concrete Custom-GPT configuration (copy/paste friendly)
Name: SMB ISP Offer Scout
Description: Browses major ISP business pages and extracts current SMB/business internet offers (speed, price, promo, term, eligibility, link). Returns results in a structured table and short plain-language summary.
Capabilities to enable: Browsing / web access (enable in the Create GPT UI). OpenAI Help Center
System / Instruction prompt (paste into the "Instructions" / system field):
Plain Text
You are "SMB ISP Offer Scout", an assistant that finds and extracts small/medium-business internet offers from business pages of major ISPs. When given a ZIP code or city, you should:
1. Visit the official "Business Internet", "Business Plans", "Promotions", and local-availability pages for AT&T Business, Spectrum Business, Comcast Business, Verizon Business, Cox Business (and other competitor domains provided).2. For each offer found, extract these fields:
   - provider
   - plan_name
   - download_speed
   - upload_speed
   - price (promo price and regular price if shown)
   - promo_description (short)
   - promo_start_date (if present)
   - promo_end_date (if present)
   - contract_term (months/term)
   - eligibility (business-only, new customers, location restrictions)
   - SLA_or_guarantee (if any)
   - page_url (source link)3. Return results as:
   a) a short summary paragraph ("At ZIP 12345, top 3 offers: ...")
   b) a JSON array containing objects with the fields above
   c) a short action recommendation (e.g., "Call provider X for custom quote", "Confirm availability via address lookup")4. When browsing, follow only publicly accessible pages and do not attempt to bypass login or paywalls.5. If a page shows only "Contact us for pricing", mark price as "contact for price" and include the page_url.6. If there is contradictory information (two pages with different prices), return both entries and add a note indicating the discrepancy.7. Always include the page_url for traceability.
Conversation starter examples for users:
“Check SMB offers near 10001 (ZIP).”
“Compare AT&T vs. Spectrum business plans for ZIP 85004.”
“Show me new promotions for business internet from Comcast and Verizon.”
7) Example user prompt -> expected GPT response format
Prompt (user):
Find current SMB business internet offers for ZIP 98101 from AT&T, Spectrum, Comcast, Verizon, and Cox.
GPT Response (format):
Short summary (2–3 sentences).
JSON array (structured offers).
One-line recommendation for next steps.
(Example JSON object):
Plain Text
[{"provider": "AT&T Business","plan_name": "Business Fiber 300","download_speed": "300 Mbps","upload_speed": "300 Mbps","price": "$199.99/mo (promo 12 months)","promo_description": "First 12 months discounted","promo_start_date": "2025-07-01","promo_end_date": "2026-06-30","contract_term": "12 months","eligibility": "New business customers only; available in select ZIPs","SLA_or_guarantee": "99.99% uptime SLA (business tier)","page_url": "https://business.att.com/plans/..."} ] 
(If price is not shown) "price": "contact for price"
8) Example extraction logic / selectors & sample Python snippet
(Use this as a fallback verification scraper. Respect robots.txt and provider TOS.)
Plain Text
# simple example: fetch a business plan page and parse for price/plan name import requestsfrom bs4 import BeautifulSoup
url = "https://www.example-isp.com/business/plans"headers = {"User-Agent":"SMB-Offer-Scout-Bot/1.0 (+your-email@example.com)"}
r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")
# naive examples: find plan cardsplans = []for card in soup.select(".plan-card"):   # site-specific selector    name = card.select_one(".plan-title").get_text(strip=True)
    price = card.select_one(".price").get_text(strip=True) if card.select_one(".price") else "contact for price"    speed = card.select_one(".speed").get_text(strip=True) if card.select_one(".speed") else ""    plans.append({"name":name, "price":price, "speed":speed, "url": url})
print(plans)
Notes:
Real sites use different markup, dynamic loading, or JavaScript — use a headless browser (Playwright/Selenium) if content is JS-rendered.
Use a small crawl-delay (e.g., 5–10s between requests) and rotate IPs responsibly if you scale. Scrapfly+1
9) Monitoring options and automation pattern (practical recipe)
Ad-hoc interactive queries: Use the Custom GPT for on-demand lookups (sales reps ask “what’s live in ZIP X?”).
Change-detection trigger: Configure Visualping/watchers for provider promo pages → when change occurs, a webhook triggers a serverless function to call the Custom GPT (or run your scraper) to extract & store updated offers. Visualping
Nightly scrape & DB: Run a nightly scraper that populates a small DB (provider, ZIP, timestamp). Use GPT to create human summaries and alerts.
Alerting: Send Slack/email alerts when new promos appear or prices change.
10) Security & privacy checklist (short)
Don’t include API keys or confidential data in the GPT prompts or uploaded files. WIRED
Log only public offer data and page URLs.
Protect scraped data at rest (encrypt DB).
Keep rate-limits moderate; include a user-agent and contact email.
11) What I can do for you right now (pick any, I’ll do it in this chat)
Draft the exact system prompt + conversation-starter text file ready to paste into OpenAI’s Create-a-GPT UI (I already wrote the main system prompt above; I can expand or tighten it).
Create an action checklist and folder structure for a lightweight scraper (files: scraper.py, scheduler config, database schema).
Prepare a Visualping / Distill watcher plan listing exact pages to monitor for the 5 competitors.
Produce a sample JSON output from a pretend ZIP so you can see the final format.
Walk you step-by-step through the OpenAI Custom GPT Create flow (I can produce the exact text you paste into fields).
Say which one you want first and I’ll produce it right here — e.g., “Draft the exact Create-GPT fields and prompt content” or “Make the Visualping watchlist with links.” (If you want me to build the watchlist, I’ll include the key URLs to monitor and the recommended watch frequency.)
If you want, I’ll immediately produce a ready-to-paste Create-GPT configuration file (system prompt, description, conversation starters, and the exact browsing instructions), plus a Visualping watchlist (with direct URLs) for the five competitors. Which would you like first?