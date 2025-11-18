"""
Multi-Tool Agent with Smart Routing
Orchestrates between Genie spaces and web search for comprehensive intelligence
"""

import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from typing import Dict, List, Tuple
from ai_helper import IncentiveAI
from web_search_tool import CompetitorSearchTool
import json


class MultiToolAgent:
    """
    Intelligent agent that routes queries to appropriate tools:
    - Internal data → Genie spaces
    - Competitor data → Web search
    - Synthesis → Foundation Model
    """
    
    def __init__(
        self,
        genie_sales_id: str = None,
        genie_analytics_id: str = None,
        genie_market_id: str = None,
        genie_voice_activations_id: str = None,
        orchestrator_model: str = "databricks-gpt-5-1"  # GPT-5.1 default (latest OpenAI)
    ):
        """
        Initialize multi-tool agent
        
        Args:
            genie_sales_id: Sales performance Genie space
            genie_analytics_id: Analytics/winners Genie space
            genie_market_id: Internal market data Genie space
            genie_voice_activations_id: Voice Activations incentive calculations (cross-workspace)
            orchestrator_model: Model for routing and synthesis
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
        
        # Initialize tools
        self.genie_sales = IncentiveAI(genie_space_id=genie_sales_id) if genie_sales_id else None
        self.genie_analytics = IncentiveAI(genie_space_id=genie_analytics_id) if genie_analytics_id else None
        self.genie_market = IncentiveAI(genie_space_id=genie_market_id) if genie_market_id else None
        
        # Voice Activations uses alternate workspace token (cross-workspace access)
        voice_alt_token = os.getenv("DATABRICKS_VOICE_WORKSPACE_TOKEN")
        if genie_voice_activations_id:
            if voice_alt_token:
                # Use alternate token for cross-workspace access
                self.genie_voice_activations = IncentiveAI(
                    genie_space_id=genie_voice_activations_id,
                    alt_workspace_token=voice_alt_token
                )
            else:
                # Fallback to default token (if in same workspace)
                self.genie_voice_activations = IncentiveAI(genie_space_id=genie_voice_activations_id)
        else:
            self.genie_voice_activations = None
        
        self.web_search = CompetitorSearchTool()
        
        self.orchestrator_model = orchestrator_model
        
        # Tool descriptions for routing
        self.tools = {
            "genie_sales": {
                "description": "Internal sales performance data - use for queries about AE performance, quotas, deals, MRR",
                "enabled": bool(genie_sales_id)
            },
            "genie_analytics": {
                "description": "Internal SPIFF winners and analytics - use for leaderboards, top performers, historical SPIFF data",
                "enabled": bool(genie_analytics_id)
            },
            "genie_market": {
                "description": "Internal market intelligence - use for our own historical market data",
                "enabled": bool(genie_market_id)
            },
            "genie_voice_activations": {
                "description": "Voice Activations incentive calculations - use for VOIP MRR, opportunity owner payouts, incremental sales incentives (NOTE: cross-workspace, being fine-tuned by data analyst)",
                "enabled": bool(genie_voice_activations_id)
            },
            "web_search": {
                "description": "External competitor intelligence - use for competitor SPIFF programs, promotions, market trends",
                "enabled": True
            }
        }
    
    def query(self, user_question: str) -> Dict:
        """
        Process user query with intelligent routing
        
        Args:
            user_question: User's natural language question
            
        Returns:
            Dict with results, tools used, and reasoning
        """
        # Step 1: Route to appropriate tool(s)
        routing_decision = self._route_query(user_question)
        
        # Step 2: Execute tool calls
        tool_results = {}
        tool_errors = {}
        
        for tool_name in routing_decision["tools"]:
            try:
                if tool_name == "genie_sales" and self.genie_sales:
                    result = self.genie_sales.ask_question(user_question)
                    # Check if result is an error message
                    if "Genie error:" in result or "Unable to get space" in result:
                        tool_errors["genie_sales"] = result
                    else:
                        tool_results["genie_sales"] = result
                        
                elif tool_name == "genie_analytics" and self.genie_analytics:
                    result = self.genie_analytics.ask_question(user_question)
                    if "Genie error:" in result or "Unable to get space" in result:
                        tool_errors["genie_analytics"] = result
                    else:
                        tool_results["genie_analytics"] = result
                        
                elif tool_name == "genie_market" and self.genie_market:
                    result = self.genie_market.ask_question(user_question)
                    if "Genie error:" in result or "Unable to get space" in result:
                        tool_errors["genie_market"] = result
                    else:
                        tool_results["genie_market"] = result
                        
                elif tool_name == "genie_voice_activations" and self.genie_voice_activations:
                    result = self.genie_voice_activations.ask_question(user_question)
                    if "Genie error:" in result or "Unable to get space" in result:
                        tool_errors["genie_voice_activations"] = result
                    else:
                        tool_results["genie_voice_activations"] = result
                        
                elif tool_name == "web_search":
                    tool_results["web_search"] = self.web_search.search_competitor_programs(user_question)
                    
            except Exception as e:
                tool_errors[tool_name] = f"Error executing {tool_name}: {str(e)}"
        
        # Step 3: Handle errors and synthesize results
        if tool_errors and not tool_results:
            # All tools failed
            error_summary = "\n\n".join([f"**{tool}:** {error}" for tool, error in tool_errors.items()])
            final_answer = f"""⚠️ **All data sources encountered errors:**

{error_summary}

**Possible causes:**
- Genie spaces may need permissions (see GENIE_PERMISSIONS_FIX.md)
- Network connectivity issues
- Data sources temporarily unavailable

💡 **Tip:** Check the 🔧 Troubleshooting tab for connection status and environment variables.
"""
            tools_used = list(tool_errors.keys())
            
        elif tool_errors:
            # Some tools failed, some succeeded
            warning = "\n".join([f"⚠️ {tool} failed: {error[:100]}..." for tool, error in tool_errors.items()])
            
            if len(tool_results) > 1:
                final_answer = self._synthesize_results(user_question, tool_results, routing_decision["reasoning"])
                final_answer = f"{warning}\n\n---\n\n{final_answer}\n\n_Note: Answer based on available sources only._"
            else:
                final_answer = list(tool_results.values())[0]
                final_answer = f"{warning}\n\n---\n\n{final_answer}\n\n_Note: Some data sources were unavailable._"
            
            tools_used = list(tool_results.keys())
            
        elif len(tool_results) > 1:
            # Multiple tools succeeded - synthesize
            final_answer = self._synthesize_results(user_question, tool_results, routing_decision["reasoning"])
            tools_used = list(tool_results.keys())
            
        elif len(tool_results) == 1:
            # Single tool succeeded
            final_answer = list(tool_results.values())[0]
            tools_used = list(tool_results.keys())
            
        else:
            # No tools configured or called
            final_answer = "No tools were able to answer this question."
            tools_used = []
        
        return {
            "answer": final_answer,
            "tools_used": tools_used,
            "routing_reasoning": routing_decision["reasoning"],
            "raw_results": tool_results,
            "errors": tool_errors if tool_errors else None
        }
    
    def _route_query(self, question: str) -> Dict:
        """
        Use LLM to determine which tool(s) to call
        """
        # Build available tools list
        available_tools = {k: v for k, v in self.tools.items() if v["enabled"]}
        
        tools_description = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in available_tools.items()
        ])
        
        routing_prompt = f"""You are a query router for a sales intelligence system.

Available tools:
{tools_description}

User question: "{question}"

Analyze the question and determine which tool(s) should be called. Consider:
1. Sales performance/quota/deals → genie_sales
2. SPIFF winners/leaderboards/top performers → genie_analytics  
3. Historical market data → genie_market
4. Voice Activations/VOIP incentives/MRR payouts → genie_voice_activations
5. Competitor programs/promotions → web_search
6. Comprehensive/strategic questions → Call ALL relevant tools (prefer calling multiple)

**IMPORTANT:** For comprehensive questions asking about "performance AND winners AND competitors", call ALL applicable tools.

Respond in JSON format:
{{
    "tools": ["tool_name1", "tool_name2"],
    "reasoning": "Brief explanation of why these tools were selected"
}}

Examples:
- "Who are our top performers?" → {{"tools": ["genie_sales", "genie_analytics"], "reasoning": "Need both sales data and leaderboard"}}
- "What is AT&T offering?" → {{"tools": ["web_search"], "reasoning": "Competitor intelligence query"}}
- "Compare our SPIFFs to Verizon" → {{"tools": ["genie_sales", "genie_analytics", "web_search"], "reasoning": "Need internal data + competitor intel"}}
- "Should we increase budget?" → {{"tools": ["genie_sales", "genie_analytics", "genie_market", "web_search"], "reasoning": "Strategic decision needs all data sources"}}
"""

        try:
            response = self.workspace.serving_endpoints.query(
                name=self.orchestrator_model,
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.USER,
                        content=routing_prompt
                    )
                ]
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            routing_decision = json.loads(content)
            return routing_decision
            
        except Exception as e:
            # Fallback: Simple keyword-based routing
            return self._fallback_routing(question)
    
    def _fallback_routing(self, question: str) -> Dict:
        """Simple keyword-based routing fallback"""
        question_lower = question.lower()
        tools = []
        
        # Check for competitor keywords
        competitor_keywords = ["competitor", "at&t", "verizon", "t-mobile", "comcast", "versus", "compare to"]
        if any(kw in question_lower for kw in competitor_keywords):
            tools.append("web_search")
        
        # Check for internal data keywords
        internal_keywords = ["our", "my", "top performer", "leaderboard", "winner", "performance"]
        if any(kw in question_lower for kw in internal_keywords):
            if "winner" in question_lower or "top" in question_lower:
                tools.append("genie_analytics")
            else:
                tools.append("genie_sales")
        
        # Default to sales if nothing matched
        if not tools and self.genie_sales:
            tools.append("genie_sales")
        
        return {
            "tools": tools,
            "reasoning": "Fallback keyword-based routing"
        }
    
    def _synthesize_results(self, question: str, tool_results: Dict, routing_reasoning: str) -> str:
        """
        Use LLM to synthesize results from multiple tools
        """
        results_text = "\n\n".join([
            f"**{tool_name.upper()} Results:**\n{result}"
            for tool_name, result in tool_results.items()
        ])
        
        synthesis_prompt = f"""You are a sales intelligence analyst synthesizing data from multiple sources.

Original question: "{question}"

Data gathered:
{results_text}

Provide a comprehensive answer that:
1. Directly answers the user's question
2. Integrates insights from all data sources
3. Highlights key comparisons or patterns
4. Provides actionable recommendations

Be concise but thorough. Use bullet points and formatting for readability.
"""

        try:
            response = self.workspace.serving_endpoints.query(
                name=self.orchestrator_model,
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.USER,
                        content=synthesis_prompt
                    )
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback: Just concatenate results
            return f"**Combined Results:**\n\n{results_text}\n\n_(Note: Automatic synthesis unavailable)_"


# Quick test
if __name__ == "__main__":
    # Test with environment variables
    agent = MultiToolAgent(
        genie_sales_id=os.getenv("GENIE_SALES_SPACE_ID"),
        genie_analytics_id=os.getenv("GENIE_ANALYTICS_SPACE_ID"),
        genie_market_id=os.getenv("GENIE_MARKET_SPACE_ID")
    )
    
    print("Testing multi-tool agent...")
    result = agent.query("How do our Q4 SPIFFs compare to AT&T's programs?")
    print(json.dumps(result, indent=2))

