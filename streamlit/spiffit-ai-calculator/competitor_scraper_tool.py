"""
Competitor Scraper Tool
Scrapes ISP competitor websites for business internet offers
Based on supportingAlternate.md recommendations
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import time
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class CompetitorScraperTool:
    """
    Scrapes competitor ISP websites for business internet offers
    """
    
    # Competitor targets with their business pages
    COMPETITORS = {
        "AT&T Business": {
            "base_url": "https://business.att.com",
            "plans_path": "/plans/internet",
            "selectors": {
                "plan_card": ".plan-card, .offer-card",
                "plan_name": ".plan-title, .offer-title, h3",
                "price": ".price, .pricing, .cost",
                "speed": ".speed, .bandwidth",
                "promo": ".promo, .promotion, .special-offer"
            }
        },
        "Spectrum Business": {
            "base_url": "https://business.spectrum.com",
            "plans_path": "/internet",
            "selectors": {
                "plan_card": ".product-card, .plan",
                "plan_name": ".product-name, h3",
                "price": ".price, .pricing-amount",
                "speed": ".speed-info, .bandwidth",
                "promo": ".promo-text, .offer-details"
            }
        },
        "Comcast Business": {
            "base_url": "https://business.comcast.com",
            "plans_path": "/internet/business-internet",
            "selectors": {
                "plan_card": ".plan-card, .product",
                "plan_name": ".plan-name, h2",
                "price": ".price, .monthly-price",
                "speed": ".speed, .download-speed",
                "promo": ".promotion, .special"
            }
        },
        "Verizon Business": {
            "base_url": "https://www.verizon.com",
            "plans_path": "/business/products/internet/business-fios/",
            "selectors": {
                "plan_card": ".plan, .product-card",
                "plan_name": ".plan-title, h3",
                "price": ".price, .cost",
                "speed": ".speed-info",
                "promo": ".promo-banner, .offer"
            }
        },
        "Cox Business": {
            "base_url": "https://www.cox.com",
            "plans_path": "/business/internet.html",
            "selectors": {
                "plan_card": ".plan, .product",
                "plan_name": ".plan-name, h2",
                "price": ".pricing, .price",
                "speed": ".speed",
                "promo": ".promotion"
            }
        }
    }
    
    def __init__(self):
        """Initialize scraper with proper headers"""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Spiffit-Competitor-Bot/1.0 (Frontier Hackathon; +spg1461@ftr.com)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })
        
    def scrape_provider(self, provider_name: str) -> List[Dict]:
        """
        Scrape business internet offers from a single provider
        
        Args:
            provider_name: Name of provider (e.g., "AT&T Business")
            
        Returns:
            List of offer dictionaries
        """
        if provider_name not in self.COMPETITORS:
            logger.warning(f"Unknown provider: {provider_name}")
            return []
        
        config = self.COMPETITORS[provider_name]
        url = config["base_url"] + config["plans_path"]
        
        logger.info(f"🔍 Scraping {provider_name} at {url}")
        
        try:
            # Respect rate limiting
            time.sleep(2)
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            offers = []
            
            # Find all plan cards
            plan_cards = soup.select(config["selectors"]["plan_card"])
            logger.info(f"📦 Found {len(plan_cards)} potential plan cards")
            
            for i, card in enumerate(plan_cards[:5]):  # Limit to first 5
                try:
                    offer = self._extract_offer(card, config["selectors"], provider_name, url)
                    if offer:
                        offers.append(offer)
                        logger.info(f"✅ Extracted offer {i+1}: {offer.get('plan_name', 'Unknown')}")
                except Exception as e:
                    logger.warning(f"⚠️ Error extracting offer {i+1}: {str(e)}")
                    continue
            
            return offers
            
        except requests.RequestException as e:
            logger.error(f"❌ Error scraping {provider_name}: {str(e)}")
            return []
    
    def _extract_offer(self, card, selectors: Dict, provider: str, page_url: str) -> Optional[Dict]:
        """Extract offer details from a plan card"""
        
        # Extract plan name
        plan_name = None
        for selector in selectors["plan_name"].split(", "):
            elem = card.select_one(selector)
            if elem:
                plan_name = elem.get_text(strip=True)
                break
        
        if not plan_name:
            return None  # Skip if no plan name
        
        # Extract price
        price_display = "Contact for pricing"
        for selector in selectors["price"].split(", "):
            elem = card.select_one(selector)
            if elem:
                price_display = elem.get_text(strip=True)
                break
        
        # Extract speed
        speed = None
        for selector in selectors["speed"].split(", "):
            elem = card.select_one(selector)
            if elem:
                speed = elem.get_text(strip=True)
                break
        
        # Extract promo
        promo_description = None
        for selector in selectors["promo"].split(", "):
            elem = card.select_one(selector)
            if elem:
                promo_description = elem.get_text(strip=True)
                break
        
        return {
            "provider": provider,
            "plan_name": plan_name,
            "download_speed": speed or "Unknown",
            "upload_speed": speed or "Unknown",  # Often same or derived
            "price_display": price_display,
            "promo_description": promo_description,
            "contract_term": "12 months",  # Default, would need parsing
            "eligibility": "New business customers",  # Default
            "sla_guarantee": None,
            "page_url": page_url,
            "scraped_at": datetime.now().isoformat(),
            "data_quality": "complete" if price_display != "Contact for pricing" else "contact_only"
        }
    
    def scrape_all(self) -> List[Dict]:
        """
        Scrape all configured competitors
        
        Returns:
            List of all offers from all providers
        """
        all_offers = []
        
        for provider_name in self.COMPETITORS.keys():
            logger.info(f"🔍 Starting scrape for {provider_name}")
            offers = self.scrape_provider(provider_name)
            all_offers.extend(offers)
            logger.info(f"✅ Got {len(offers)} offers from {provider_name}")
        
        logger.info(f"🎉 Total offers scraped: {len(all_offers)}")
        return all_offers
    
    def format_as_markdown(self, offers: List[Dict]) -> str:
        """Format offers as markdown for display"""
        if not offers:
            return "No competitor offers found."
        
        md = f"**Competitor Intelligence:** Found {len(offers)} business internet offers\n\n"
        
        for offer in offers:
            md += f"### {offer['provider']} - {offer['plan_name']}\n"
            md += f"- **Speed:** {offer['download_speed']}\n"
            md += f"- **Price:** {offer['price_display']}\n"
            if offer.get('promo_description'):
                md += f"- **Promo:** {offer['promo_description']}\n"
            md += f"- **Source:** {offer['page_url']}\n"
            md += f"- **Scraped:** {offer['scraped_at']}\n\n"
        
        return md


# Singleton instance
_scraper_tool = None

def get_scraper_tool() -> CompetitorScraperTool:
    """Get or create scraper tool singleton"""
    global _scraper_tool
    if _scraper_tool is None:
        _scraper_tool = CompetitorScraperTool()
    return _scraper_tool

