"""
Web Search Tool for Competitor Intelligence
Uses Foundation Models to search and summarize competitor information
"""

import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from typing import List, Dict
import json


class CompetitorSearchTool:
    """
    Tool for searching competitor promotions and SPIFF programs
    """
    
    def __init__(self, model_name: str = "databricks-gpt-5-1"):
        """
        Initialize web search tool
        
        Args:
            model_name: Foundation model for search/summarization
        """
        # Get authentication credentials
        host = os.getenv("DATABRICKS_HOST")
        token = os.getenv("DATABRICKS_TOKEN")
        profile = os.getenv("DATABRICKS_PROFILE")
        
        # Initialize with priority: PAT token > CLI profile > automatic OAuth
        if host and token:
            # PAT token authentication (explicitly set auth_type to avoid conflict with OAuth M2M)
            self.workspace = WorkspaceClient(host=host, token=token, auth_type='pat')
        elif profile:
            self.workspace = WorkspaceClient(profile=profile)
        else:
            # Automatic OAuth M2M (Databricks Apps default)
            self.workspace = WorkspaceClient()
        
        self.model_name = model_name
        
        # Priority competitor business internet pages (from supportingAlternate.md)
        self.competitor_targets = {
            "AT&T Business": "https://business.att.com",
            "Spectrum Business": "https://business.spectrum.com",
            "Comcast Business": "https://business.comcast.com",
            "Verizon Business": "https://www.verizon.com/business",
            "Cox Business": "https://www.cox.com/business"
        }
        
        # Mock competitor data for demo (replace with real API in production)
        self.mock_competitor_data = {
            "AT&T": {
                "q4_2024": {
                    "programs": [
                        "Holiday Mega Bonus: $10K for deals > $200K",
                        "New Logo Push: Triple commission on new enterprise customers",
                        "Year-End Accelerator: 150% payout for Q4 quota achievement"
                    ],
                    "business_offers": [
                        "Business Fiber 300: $199.99/mo (promo 12 months)",
                        "Business Internet 500: $249.99/mo with 99.99% SLA",
                        "Dedicated Internet: Contact for enterprise pricing"
                    ]
                },
                    "focus": "Enterprise deals, new customer acquisition"
                }
            },
            "Spectrum": {
                "q4_2024": {
                    "programs": [
                        "Winter Blitz: $15K bonus on MDU/bulk deals",
                        "Fiber Expansion Rewards: 2x comm on new fiber markets",
                        "Q4 Sweep: Top 10 reps win Hawaii trip"
                    ],
                    "business_offers": [
                        "Business Internet 500: $249.99/mo (promo 24 months)",
                        "Business Internet Gig: $299.99/mo with 99.9% uptime guarantee",
                        "Managed WiFi: Add $50/mo to any plan"
                    ]
                },
                "focus": "Bulk properties, small business expansion"
            },
            "Verizon": {
                "q4_2024": {
                    "programs": [
                        "5G Expansion Bonus: $5K per new 5G deployment",
                        "Retention Champion: Double commission on renewals > $100K",
                        "End of Year Sprint: 200% commission last 2 weeks of December"
                    ],
                    "business_offers": [
                        "Business Fios Gigabit: $349.99/mo (promo 12 months)",
                        "Business Internet 500/500: $299.99/mo with 99.99% reliability",
                        "Dedicated Internet Access: Custom pricing for enterprise"
                    ]
                },
                    "focus": "5G deployments, retention"
                }
            },
            "T-Mobile": {
                "q4_2024": {
                    "programs": [
                        "Business Unlimited Bonus: $3K per unlimited business plan sale",
                        "Switcher Incentive: $2K per customer switched from competitor",
                        "Holiday Close Bonus: $7.5K for deals closed by Dec 20"
                    ],
                    "focus": "SMB market, customer acquisition"
                }
            },
            "Comcast Business": {
                "q4_2024": {
                    "programs": [
                        "Large Deal Accelerator: 200% commission on deals > $150K",
                        "Bundle Master: $4K bonus for 3+ service bundles",
                        "Q4 Blitz: Progressive bonus tiers (110%, 125%, 150% of quota)"
                    ],
                    "focus": "Bundled services, large enterprise deals"
                }
            }
        }
    
    def search_competitor_programs(self, query: str) -> str:
        """
        Search for competitor SPIFF programs
        
        Args:
            query: Search query (e.g., "AT&T Q4 promotions")
            
        Returns:
            Formatted competitor intelligence
        """
        try:
            # For hackathon demo: Use mock data + LLM to generate natural response
            # In production: Replace with real search API (SerpAPI, Bing, etc.)
            
            # Extract competitor name from query
            competitor = self._extract_competitor(query)
            
            if competitor and competitor in self.mock_competitor_data:
                data = self.mock_competitor_data[competitor]
                return self._format_competitor_data(competitor, data)
            else:
                # Use LLM to generate summary from all competitors
                return self._llm_search(query)
        
        except Exception as e:
            return f"Web search error: {str(e)}"
    
    def _extract_competitor(self, query: str) -> str:
        """Extract competitor name from query"""
        query_lower = query.lower()
        for competitor in self.mock_competitor_data.keys():
            if competitor.lower() in query_lower:
                return competitor
        return None
    
    def _format_competitor_data(self, competitor: str, data: Dict) -> str:
        """Format competitor data into readable response"""
        result = f"## {competitor} - Competitor Intelligence\n\n"
        
        for period, info in data.items():
            result += f"**{period.upper()}**\n\n"
            result += f"**Focus Areas:** {info['focus']}\n\n"
            result += "**SPIFF Programs:**\n"
            for i, program in enumerate(info['programs'], 1):
                result += f"{i}. {program}\n"
            result += "\n"
        
        return result
    
    def _llm_search(self, query: str) -> str:
        """
        Use LLM to search and summarize competitor data
        """
        # Prepare context with all competitor data
        context = json.dumps(self.mock_competitor_data, indent=2)
        
        prompt = f"""You are a competitive intelligence analyst for a telecom sales team.

User query: {query}

Available competitor data:
{context}

Based on the query and available data, provide a concise summary of relevant competitor SPIFF programs and promotions. 
Focus on actionable insights that would help our sales team compete effectively.

If the query asks for a comparison, compare multiple competitors. 
If the query asks about trends, identify patterns across competitors.
Format your response clearly with competitor names and program details.
"""

        try:
            response = self.workspace.serving_endpoints.query(
                name=self.model_name,
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.USER,
                        content=prompt
                    )
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"LLM search error: {str(e)}"
    
    def get_all_competitors(self) -> List[str]:
        """Get list of tracked competitors"""
        return list(self.mock_competitor_data.keys())
    
    def compare_competitors(self, competitors: List[str] = None) -> str:
        """
        Compare SPIFF programs across competitors
        
        Args:
            competitors: List of competitor names (None = all)
        """
        if not competitors:
            competitors = self.get_all_competitors()
        
        prompt = f"""Compare the Q4 2024 SPIFF programs across these telecom competitors:

{json.dumps({k: v for k, v in self.mock_competitor_data.items() if k in competitors}, indent=2)}

Provide a strategic analysis:
1. Which competitor is offering the most aggressive incentives?
2. What are the common themes/focus areas?
3. What gaps or opportunities exist for our team?
4. Recommendations for competitive SPIFF programs

Format as a brief executive summary.
"""

        try:
            response = self.workspace.serving_endpoints.query(
                name=self.model_name,
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.USER,
                        content=prompt
                    )
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Comparison error: {str(e)}"


# Quick test
if __name__ == "__main__":
    tool = CompetitorSearchTool()
    print("Testing competitor search...")
    result = tool.search_competitor_programs("What are AT&T's Q4 promotions?")
    print(result)

