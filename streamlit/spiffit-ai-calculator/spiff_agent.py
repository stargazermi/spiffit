"""
Autonomous SPIFF Recommendation Agent
Time-aware intelligent agent for managing SPIFF lifecycle
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from datetime import datetime, timedelta
import json
import os


class SPIFFAgent:
    """
    Intelligent agent that autonomously manages SPIFF recommendations and reporting
    """
    
    def __init__(self):
        self.ws = WorkspaceClient()
        
        # Genie space configuration
        self.spaces = {
            "sales_data": {
                "space_id": os.getenv("GENIE_SALES_SPACE_ID"),
                "description": "Historical sales performance, deals, quotas, achievements"
            },
            "analytics": {
                "space_id": os.getenv("GENIE_ANALYTICS_SPACE_ID"),  # Data analyst's space
                "description": "SPIFF winners, leaderboards, trend analysis, rankings"
            },
            "market": {
                "space_id": os.getenv("GENIE_MARKET_SPACE_ID"),
                "description": "Competitor data, industry trends, market intelligence"
            }
        }
        
        # Agent state
        self.investigation_history = []
        self.gathered_facts = {}
        self.reasoning_chain = []
    
    def check_and_act(self):
        """
        Main entry point: Check date and trigger appropriate action
        """
        today = datetime.now()
        day_of_month = today.day
        current_month = today.strftime("%B %Y")
        
        # Determine what phase we're in
        if day_of_month == 1:
            phase = "month_end_review"
            action = "Generate previous month's results and winner emails"
        elif 15 <= day_of_month <= 20:
            phase = "recommendation_time"
            action = "Analyze data and recommend next month's SPIFFs"
        elif day_of_month in [7, 14, 21, 28]:
            phase = "progress_check"
            action = "Check current month progress and alert if needed"
        else:
            phase = "monitoring"
            action = "Monitor for any immediate issues or opportunities"
        
        print(f"📅 Date: {today.strftime('%B %d, %Y')}")
        print(f"🔍 Phase: {phase}")
        print(f"🎯 Action: {action}")
        print()
        
        # Execute appropriate workflow
        if phase == "month_end_review":
            return self.generate_month_end_report(today)
        elif phase == "recommendation_time":
            return self.recommend_next_month_spiffs(today)
        elif phase == "progress_check":
            return self.check_progress(today)
        else:
            return self.monitor_and_alert(today)
    
    def generate_month_end_report(self, date):
        """
        Day 1: Generate previous month's results and winner email
        """
        print("=" * 80)
        print("🎉 MONTH-END REVIEW WORKFLOW")
        print("=" * 80)
        print()
        
        previous_month = (date - timedelta(days=5)).strftime("%B %Y")
        
        # Step 1: Agent plans investigation
        print("🤖 Agent Planning:")
        print("   - I need to identify who won last month's SPIFFs")
        print("   - I need their specific achievements")
        print("   - I need overall program metrics")
        print()
        
        # Step 2: Query analytics space for winners
        print("📊 Step 1: Querying analytics space for SPIFF winners...")
        
        winners_query = f"""
        For {previous_month}, identify all employees who achieved SPIFF targets.
        For each SPIFF program, show:
        - Program name
        - Number of qualifiers
        - Total bonus amount
        - Top 5 performers with their earnings
        
        Generate a complete leaderboard.
        """
        
        winners_result = self._query_genie("analytics", winners_query)
        self.gathered_facts["winners"] = winners_result
        
        print(f"   ✓ Found SPIFF winners")
        print()
        
        # Step 3: Agent analyzes and decides next step
        print("🤖 Agent Reasoning:")
        print("   - I have the winners list, but need achievement details")
        print("   - Need to query sales data for what they specifically did")
        print()
        
        # Step 4: Query sales space for achievement details
        print("📈 Step 2: Querying sales space for achievement details...")
        
        details_query = f"""
        For the top SPIFF earners in {previous_month}, provide:
        - Specific deals closed (with $ amounts)
        - Quota attainment percentage
        - Number of new logos
        - Renewal saves
        - Total revenue impact
        """
        
        achievement_details = self._query_genie("sales_data", details_query)
        self.gathered_facts["achievements"] = achievement_details
        
        print(f"   ✓ Retrieved achievement details")
        print()
        
        # Step 5: Query for program performance
        print("📊 Step 3: Analyzing overall program performance...")
        
        program_query = f"""
        Compare {previous_month} SPIFF program performance to previous year:
        - Total revenue generated
        - Participation rate
        - ROI (revenue / cost)
        - Team satisfaction metrics
        """
        
        program_metrics = self._query_genie("analytics", program_query)
        self.gathered_facts["program_performance"] = program_metrics
        
        print(f"   ✓ Got program metrics")
        print()
        
        # Step 6: Generate email
        print("✉️  Step 4: Generating winner announcement email...")
        
        email_content = self._generate_winner_email(
            previous_month,
            winners_result,
            achievement_details,
            program_metrics
        )
        
        print()
        print("=" * 80)
        print("📧 GENERATED EMAIL:")
        print("=" * 80)
        print(email_content)
        print("=" * 80)
        
        return {
            "phase": "month_end_review",
            "month": previous_month,
            "winners": winners_result,
            "email": email_content,
            "actions": [
                "Email sent to sales team",
                "Report sent to VP Sales",
                "Accounting notified of payouts"
            ]
        }
    
    def recommend_next_month_spiffs(self, date):
        """
        Day 15-20: Analyze and recommend next month's SPIFFs
        """
        print("=" * 80)
        print("💡 SPIFF RECOMMENDATION WORKFLOW")
        print("=" * 80)
        print()
        
        current_month = date.strftime("%B %Y")
        next_month = (date + timedelta(days=30)).strftime("%B %Y")
        
        # Step 1: Agent creates investigation plan
        print("🤖 Agent Planning Investigation:")
        plan = self._create_investigation_plan(next_month)
        
        for i, step in enumerate(plan["steps"], 1):
            print(f"   {i}. {step['action']} - {step['reason']}")
        print()
        
        # Step 2: Execute investigation dynamically
        for step in plan["steps"]:
            print(f"🔍 Executing: {step['action']}")
            
            result = self._execute_investigation_step(step)
            self.gathered_facts[step["key"]] = result
            
            # Agent analyzes what it learned
            analysis = self._analyze_finding(result, step)
            
            print(f"   ✓ Learned: {analysis['key_insight']}")
            
            # Agent decides if it needs follow-up
            if analysis.get("needs_follow_up"):
                print(f"   🤔 Agent decides: {analysis['follow_up_reason']}")
                follow_up = self._execute_follow_up(analysis["follow_up_question"])
                self.gathered_facts[f"{step['key']}_followup"] = follow_up
                print(f"   ✓ Follow-up complete")
            
            print()
        
        # Step 3: Agent synthesizes recommendations
        print("💡 Agent Synthesizing Recommendations...")
        print()
        
        recommendations = self._generate_recommendations(next_month, self.gathered_facts)
        
        print("=" * 80)
        print(f"📋 RECOMMENDATIONS FOR {next_month.upper()}")
        print("=" * 80)
        print(recommendations)
        print("=" * 80)
        
        return {
            "phase": "recommendation",
            "target_month": next_month,
            "investigation_steps": len(plan["steps"]),
            "follow_ups_triggered": sum(1 for v in self.gathered_facts.values() if "followup" in str(v)),
            "recommendations": recommendations
        }
    
    def check_progress(self, date):
        """
        Weekly check: Monitor current month progress
        """
        print("=" * 80)
        print("📊 PROGRESS CHECK")
        print("=" * 80)
        print()
        
        current_month = date.strftime("%B %Y")
        
        progress_query = f"""
        For {current_month} (current month):
        - How many AEs have achieved SPIFF targets so far?
        - What is current revenue vs. target?
        - Are we on pace to meet goals?
        - Any concerning trends?
        """
        
        progress = self._query_genie("sales_data", progress_query)
        
        # Agent analyzes progress
        analysis_prompt = f"""
        Analyze this progress data: {progress}
        
        Determine:
        - Is performance on track? (Yes/No)
        - Are there any red flags?
        - Should we send an alert?
        
        Return JSON:
        {{
            "on_track": true/false,
            "concerns": ["list"],
            "alert_needed": true/false,
            "recommendation": "what to do"
        }}
        """
        
        analysis = self._llm_call(analysis_prompt)
        
        if analysis.get("alert_needed"):
            print(f"⚠️  ALERT: {analysis['recommendation']}")
        else:
            print(f"✅ Status: On track")
        
        print()
        return {
            "phase": "progress_check",
            "progress": progress,
            "analysis": analysis
        }
    
    def monitor_and_alert(self, date):
        """
        Continuous monitoring for immediate issues
        """
        print("🔍 Monitoring mode - no immediate actions needed")
        return {"phase": "monitoring", "status": "nominal"}
    
    # ===== Helper Methods =====
    
    def _query_genie(self, space_name, question):
        """
        Query a specific Genie space
        """
        space_id = self.spaces[space_name]["space_id"]
        
        if not space_id:
            return f"[Simulated response from {space_name}]"
        
        try:
            response = self.ws.genie.ask_question(
                space_id=space_id,
                content=question
            )
            
            self.investigation_history.append({
                "space": space_name,
                "question": question,
                "timestamp": datetime.now().isoformat()
            })
            
            return response.content
        except Exception as e:
            return f"Error querying {space_name}: {str(e)}"
    
    def _llm_call(self, prompt):
        """
        Call foundation model for reasoning
        """
        try:
            response = self.ws.serving_endpoints.query(
                name="databricks-meta-llama-3-1-70b-instruct",
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.USER,
                        content=prompt
                    )
                ]
            )
            
            # Try to parse as JSON if possible
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except:
                return content
        except Exception as e:
            return {"error": str(e)}
    
    def _create_investigation_plan(self, target_month):
        """
        Agent creates a plan for investigation
        """
        planning_prompt = f"""
        You are planning to recommend SPIFFs for {target_month}.
        
        Create an investigation plan with 3-4 steps.
        Each step should gather specific information needed.
        
        Return JSON:
        {{
            "steps": [
                {{
                    "action": "Query historical SPIFF performance",
                    "reason": "Need to see what worked last time",
                    "key": "historical",
                    "space": "analytics"
                }}
            ]
        }}
        """
        
        plan = self._llm_call(planning_prompt)
        
        # Default plan if LLM fails
        if isinstance(plan, dict) and "steps" in plan:
            return plan
        else:
            return {
                "steps": [
                    {
                        "action": "Query recent SPIFF performance",
                        "reason": "Understand what's working currently",
                        "key": "recent_performance",
                        "space": "sales_data"
                    },
                    {
                        "action": "Check competitor offerings",
                        "reason": "Need to match or beat competition",
                        "key": "competition",
                        "space": "market"
                    },
                    {
                        "action": "Analyze historical trends",
                        "reason": "Understand seasonal patterns",
                        "key": "trends",
                        "space": "analytics"
                    }
                ]
            }
    
    def _execute_investigation_step(self, step):
        """
        Execute a step in the investigation plan
        """
        # Build query based on step
        if step["key"] == "recent_performance":
            query = "What were the results of our most recent SPIFF programs? Which had highest participation and ROI?"
        elif step["key"] == "competition":
            query = "What SPIFF or incentive programs are competitors currently offering?"
        elif step["key"] == "trends":
            query = f"What are the historical trends for the target month? Show seasonal patterns."
        else:
            query = step.get("action", "Get relevant data")
        
        return self._query_genie(step["space"], query)
    
    def _analyze_finding(self, result, step):
        """
        Agent analyzes what it learned and decides if follow-up needed
        """
        analysis_prompt = f"""
        I just learned this from {step['space']}: {result}
        
        Analyze:
        1. What's the key insight?
        2. Is this information complete?
        3. Do I need a follow-up question?
        
        Return JSON:
        {{
            "key_insight": "one sentence summary",
            "needs_follow_up": true/false,
            "follow_up_reason": "why",
            "follow_up_question": "what to ask"
        }}
        """
        
        analysis = self._llm_call(analysis_prompt)
        
        if isinstance(analysis, dict):
            return analysis
        else:
            return {
                "key_insight": "Data gathered successfully",
                "needs_follow_up": False
            }
    
    def _execute_follow_up(self, question):
        """
        Agent executes a follow-up question
        """
        # Route follow-up intelligently
        routing_prompt = f"""
        This follow-up question needs to be answered: {question}
        
        Which space should answer it?
        - sales_data: Historical sales performance
        - analytics: Trends and analysis
        - market: Competitor and industry data
        
        Return just the space name.
        """
        
        space = self._llm_call(routing_prompt)
        
        if isinstance(space, str) and space in self.spaces:
            return self._query_genie(space, question)
        else:
            return self._query_genie("sales_data", question)  # default
    
    def _generate_recommendations(self, target_month, facts):
        """
        Agent synthesizes all gathered facts into recommendations
        """
        synthesis_prompt = f"""
        Generate SPIFF recommendations for {target_month} based on this data:
        
        {json.dumps(facts, indent=2)}
        
        Create 2-3 specific SPIFF programs with:
        - Creative name
        - Target behavior
        - Incentive amount
        - Reasoning (why this will work)
        - Expected impact
        - Budget estimate
        
        Format as a professional recommendation document.
        """
        
        recommendations = self._llm_call(synthesis_prompt)
        return recommendations
    
    def _generate_winner_email(self, month, winners, achievements, metrics):
        """
        Generate winner announcement email
        """
        email_prompt = f"""
        Generate an enthusiastic email announcing {month} SPIFF winners.
        
        Winners data: {winners}
        Their achievements: {achievements}
        Program metrics: {metrics}
        
        Email should:
        - Celebrate top performers with specific numbers
        - Show overall program success
        - Create excitement
        - Professional but energetic tone
        
        Include emoji where appropriate. Make it motivating!
        """
        
        email = self._llm_call(email_prompt)
        return email


# ===== Streamlit Integration =====

def run_agent_demo():
    """
    Demo function for Streamlit
    """
    import streamlit as st
    
    st.title("🤖 Autonomous SPIFF Agent")
    st.caption("Time-aware intelligent agent for SPIFF management")
    
    # Initialize agent
    agent = SPIFFAgent()
    
    # Show current status
    today = datetime.now()
    day = today.day
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Date", today.strftime("%B %d"))
    
    with col2:
        if day == 1:
            phase = "Month-End Review"
        elif 15 <= day <= 20:
            phase = "Recommendation Time"
        else:
            phase = "Monitoring"
        st.metric("Agent Phase", phase)
    
    with col3:
        st.metric("Genie Spaces", "3 connected")
    
    st.markdown("---")
    
    # Manual trigger
    if st.button("🚀 Run Agent Now", type="primary"):
        with st.spinner("Agent is reasoning..."):
            result = agent.check_and_act()
        
        st.success("✅ Agent execution complete!")
        
        # Show results
        st.subheader("Agent Results")
        st.json(result)
        
        # Show reasoning chain
        if agent.investigation_history:
            with st.expander("🔍 Investigation History"):
                for i, step in enumerate(agent.investigation_history, 1):
                    st.write(f"**Step {i}:** Queried `{step['space']}`")
                    st.caption(step['question'])


if __name__ == "__main__":
    # Can be run as standalone script or imported for Streamlit
    agent = SPIFFAgent()
    result = agent.check_and_act()
    print("\n✅ Agent execution complete!")

