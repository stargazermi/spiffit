"""
SPIFF Agent Dashboard - Streamlit App
Interactive dashboard for autonomous SPIFF management agent
"""

import streamlit as st
from datetime import datetime, timedelta
from spiff_agent import SPIFFAgent
import os

# Page configuration
st.set_page_config(
    page_title="SPIFF Agent Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Initialize agent
@st.cache_resource
def init_agent():
    return SPIFFAgent()

agent = init_agent()

# ===== Header =====
st.title("🤖 Autonomous SPIFF Agent Dashboard")
st.caption("Time-aware AI agent that manages SPIFF recommendations and reporting")

# ===== Current Status =====
st.markdown("---")
st.subheader("📅 Current Status")

today = datetime.now()
day_of_month = today.day

# Determine current phase
if day_of_month == 1:
    phase = "Month-End Review"
    phase_emoji = "🎉"
    phase_color = "green"
    phase_action = "Generate previous month results and winner emails"
elif 15 <= day_of_month <= 20:
    phase = "Recommendation Time"
    phase_emoji = "💡"
    phase_color = "blue"
    phase_action = "Analyze data and recommend next month's SPIFFs"
elif day_of_month in [7, 14, 21, 28]:
    phase = "Progress Check"
    phase_emoji = "📊"
    phase_color = "orange"
    phase_action = "Monitor current month progress"
else:
    phase = "Monitoring"
    phase_emoji = "🔍"
    phase_color = "gray"
    phase_action = "Continuous monitoring mode"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Date", today.strftime("%B %d, %Y"))

with col2:
    st.metric("Day of Month", f"Day {day_of_month}")

with col3:
    st.metric("Agent Phase", f"{phase_emoji} {phase}")

with col4:
    # Check Genie configuration
    spaces_configured = sum(1 for space in agent.spaces.values() if space["space_id"])
    st.metric("Genie Spaces", f"{spaces_configured}/3 configured")

st.info(f"**Scheduled Action:** {phase_action}")

# ===== Configuration Section =====
st.markdown("---")
st.subheader("⚙️ Configuration")

with st.expander("Genie Space Configuration", expanded=False):
    st.write("**Configure environment variables for Genie spaces:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.code("""
# Sales Data Space
GENIE_SALES_SPACE_ID=your-sales-space-id

# Analytics Space (Data Analyst's)
GENIE_ANALYTICS_SPACE_ID=your-analytics-space-id

# Market Intelligence Space
GENIE_MARKET_SPACE_ID=your-market-space-id
        """, language="bash")
    
    with col2:
        st.write("**Current Configuration:**")
        for space_name, space_data in agent.spaces.items():
            if space_data["space_id"]:
                st.success(f"✅ {space_name}: {space_data['space_id'][:20]}...")
            else:
                st.warning(f"⚠️ {space_name}: Not configured")

# ===== Agent Timeline =====
st.markdown("---")
st.subheader("📆 Agent Timeline")

timeline_data = {
    "Day 1-5": {
        "phase": "Review Phase",
        "emoji": "🎉",
        "actions": [
            "Generate previous month results",
            "Identify SPIFF winners",
            "Create email announcements",
            "Distribute to team"
        ],
        "active": day_of_month <= 5
    },
    "Day 6-14": {
        "phase": "Monitoring Phase",
        "emoji": "📊",
        "actions": [
            "Track current month progress",
            "Alert on low performance",
            "Provide updates"
        ],
        "active": 6 <= day_of_month <= 14
    },
    "Day 15-20": {
        "phase": "Planning Phase",
        "emoji": "💡",
        "actions": [
            "Analyze historical trends",
            "Check competitor SPIFFs",
            "Recommend next month incentives",
            "Generate proposal"
        ],
        "active": 15 <= day_of_month <= 20
    },
    "Day 21-30": {
        "phase": "Execution Phase",
        "emoji": "✅",
        "actions": [
            "Finalize approved SPIFFs",
            "Communicate to sales team",
            "Set up tracking"
        ],
        "active": day_of_month >= 21
    }
}

cols = st.columns(4)

for i, (day_range, data) in enumerate(timeline_data.items()):
    with cols[i]:
        if data["active"]:
            st.markdown(f"### {data['emoji']} **{day_range}**")
            st.markdown(f"**{data['phase']}** ⬅️ *Current*")
        else:
            st.markdown(f"### {data['emoji']} {day_range}")
            st.markdown(f"*{data['phase']}*")
        
        for action in data["actions"]:
            st.caption(f"• {action}")

# ===== Agent Execution =====
st.markdown("---")
st.subheader("🚀 Execute Agent")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("""
    Click the button below to run the agent now. The agent will:
    1. Check the current date
    2. Determine the appropriate workflow
    3. Gather data from configured Genie spaces
    4. Reason about the findings
    5. Generate recommendations or reports
    """)

with col2:
    if st.button("▶️ Run Agent Now", type="primary", use_container_width=True):
        st.session_state['run_agent'] = True

# Show agent execution
if st.session_state.get('run_agent', False):
    st.markdown("---")
    st.subheader("🤖 Agent Execution Log")
    
    # Create a container for live updates
    with st.container():
        with st.spinner("🔄 Agent is reasoning..."):
            # Capture agent output
            result = agent.check_and_act()
        
        st.success("✅ Agent execution complete!")
        
        # Show results in tabs
        tab1, tab2, tab3 = st.tabs(["📋 Summary", "🔍 Investigation", "📊 Raw Data"])
        
        with tab1:
            st.subheader("Execution Summary")
            
            if result.get("phase") == "month_end_review":
                st.info(f"**Phase:** Month-End Review for {result.get('month', 'previous month')}")
                
                if result.get("email"):
                    st.markdown("### Generated Email")
                    st.markdown(result["email"])
                
                if result.get("actions"):
                    st.markdown("### Actions Taken")
                    for action in result["actions"]:
                        st.success(f"✅ {action}")
            
            elif result.get("phase") == "recommendation":
                st.info(f"**Phase:** SPIFF Recommendations for {result.get('target_month', 'next month')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Investigation Steps", result.get("investigation_steps", 0))
                with col2:
                    st.metric("Follow-ups Triggered", result.get("follow_ups_triggered", 0))
                
                if result.get("recommendations"):
                    st.markdown("### Recommendations")
                    st.markdown(result["recommendations"])
            
            else:
                st.json(result)
        
        with tab2:
            st.subheader("Investigation History")
            
            if agent.investigation_history:
                for i, step in enumerate(agent.investigation_history, 1):
                    with st.expander(f"Step {i}: Query to `{step['space']}`"):
                        st.caption(f"**Timestamp:** {step['timestamp']}")
                        st.write(f"**Question:** {step['question']}")
            else:
                st.info("No investigation steps recorded")
            
            if agent.gathered_facts:
                st.subheader("Gathered Facts")
                st.json(agent.gathered_facts)
        
        with tab3:
            st.subheader("Raw Agent Output")
            st.json(result)
    
    # Reset flag
    if st.button("🔄 Clear Results"):
        st.session_state['run_agent'] = False
        st.rerun()

# ===== Manual Testing =====
st.markdown("---")
st.subheader("🧪 Manual Testing")

with st.expander("Test Agent with Different Dates"):
    test_date = st.date_input(
        "Select a date to simulate",
        value=datetime.now()
    )
    
    test_day = test_date.day
    
    if test_day == 1:
        st.info("✅ This would trigger **Month-End Review** workflow")
    elif 15 <= test_day <= 20:
        st.info("✅ This would trigger **SPIFF Recommendation** workflow")
    elif test_day in [7, 14, 21, 28]:
        st.info("✅ This would trigger **Progress Check** workflow")
    else:
        st.info("✅ This would be in **Monitoring** mode")

with st.expander("Test Individual Genie Space Queries"):
    space_to_test = st.selectbox(
        "Select Genie Space",
        options=list(agent.spaces.keys()),
        format_func=lambda x: f"{x} - {agent.spaces[x]['description']}"
    )
    
    test_question = st.text_area(
        "Enter your question",
        placeholder="What were last month's SPIFF results?"
    )
    
    if st.button("🔍 Query Genie Space"):
        if test_question:
            with st.spinner(f"Querying {space_to_test}..."):
                result = agent._query_genie(space_to_test, test_question)
            
            st.success("Response received!")
            st.write(result)
        else:
            st.warning("Please enter a question")

# ===== Documentation =====
st.markdown("---")
st.subheader("📚 Documentation")

doc_col1, doc_col2, doc_col3 = st.columns(3)

with doc_col1:
    st.markdown("""
    **Agent Documentation**
    - [Autonomous SPIFF Agent](../AUTONOMOUS_SPIFF_AGENT.md)
    - [Agent Architecture](#)
    - [Configuration Guide](#)
    """)

with doc_col2:
    st.markdown("""
    **Related Guides**
    - [Smart Routing](../SMART_GENIE_ROUTING.md)
    - [Multi-Genie Workflows](../MULTI_GENIE_WORKFLOWS.md)
    - [AI Integration](../ai_integration_guide.md)
    """)

with doc_col3:
    st.markdown("""
    **Quick Actions**
    - View Investigation Logs
    - Export Recommendations
    - Configure Schedules
    """)

# ===== Footer =====
st.markdown("---")
st.caption("🤖 Powered by Databricks Genie + Foundation Models | Built for Hackathon 🚀")

