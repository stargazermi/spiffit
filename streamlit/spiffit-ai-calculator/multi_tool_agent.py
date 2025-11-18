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
        orchestrator_model: str = "databricks-gpt-5-1"
    ):
        """
        Initialize multi-tool agent
        
        Args:
            genie_sales_id: Sales performance Genie space
            genie_analytics_id: Analytics/winners Genie space
            genie_market_id: Internal market data Genie space
            orchestrator_model: Model for routing and synthesis
        """
        profile = os.getenv("DATABRICKS_PROFILE")
        
        if profile:
            self.workspace = WorkspaceClient(profile=profile)
        else:
            self.workspace = WorkspaceClient()
        
        # Initialize tools
        self.genie_sales = IncentiveAI(genie_space_id=genie_sales_id) if genie_sales_id else None
        self.genie_analytics = IncentiveAI(genie_space_id=genie_analytics_id) if genie_analytics_id else None
        self.genie_market = IncentiveAI(genie_space_id=genie_market_id) if genie_market_id else None
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
        for tool_name in routing_decision["tools"]:
            if tool_name == "genie_sales" and self.genie_sales:
                tool_results["genie_sales"] = self.genie_sales.ask_question(user_question)
            elif tool_name == "genie_analytics" and self.genie_analytics:
                tool_results["genie_analytics"] = self.genie_analytics.ask_question(user_question)
            elif tool_name == "genie_market" and self.genie_market:
                tool_results["genie_market"] = self.genie_market.ask_question(user_question)
            elif tool_name == "web_search":
                tool_results["web_search"] = self.web_search.search_competitor_programs(user_question)
        
        # Step 3: Synthesize results
        if len(tool_results) > 1:
            # Multiple tools - need synthesis
            final_answer = self._synthesize_results(user_question, tool_results, routing_decision["reasoning"])
        elif len(tool_results) == 1:
            # Single tool - return directly
            final_answer = list(tool_results.values())[0]
        else:
            final_answer = "No tools were able to answer this question."
        
        return {
            "answer": final_answer,
            "tools_used": list(tool_results.keys()),
            "routing_reasoning": routing_decision["reasoning"],
            "raw_results": tool_results
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
1. Does it ask about internal performance? → Use genie_sales or genie_analytics
2. Does it ask about competitors? → Use web_search
3. Does it need both internal and external data? → Use multiple tools

Respond in JSON format:
{{
    "tools": ["tool_name1", "tool_name2"],
    "reasoning": "Brief explanation of why these tools were selected"
}}

Examples:
- "Who are our top performers?" → {{"tools": ["genie_analytics"], "reasoning": "Internal leaderboard query"}}
- "What is AT&T offering?" → {{"tools": ["web_search"], "reasoning": "Competitor intelligence query"}}
- "How do our SPIFFs compare to Verizon?" → {{"tools": ["genie_analytics", "web_search"], "reasoning": "Need both internal and competitor data"}}
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

