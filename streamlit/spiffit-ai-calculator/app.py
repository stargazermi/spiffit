"""
Spiffit AI Calculator - Streamlit App
Natural language interface for incentive calculations
"""

# Load environment variables from .env file (for local testing)
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from ai_helper import IncentiveAI
from query_parser import QueryParser

# Page configuration
st.set_page_config(
    page_title="Spiffit AI Calculator",
    page_icon="🤖",
    layout="wide"
)

# Initialize AI components
@st.cache_resource
def init_ai():
    """Initialize AI helper and parser (cached)"""
    # Read Genie space ID from environment variable
    genie_space_id = os.getenv("GENIE_SPACE_ID")
    
    if genie_space_id:
        # Use Genie if space ID is configured
        ai = IncentiveAI(genie_space_id=genie_space_id)
        st.success(f"✅ Connected to Genie Space: {genie_space_id}")
    else:
        # Fall back to Foundation Model
        ai = IncentiveAI(model_name="databricks-meta-llama-3-1-70b-instruct")
        st.warning("""
        ⚠️ **Genie Space ID not configured**
        
        The app is using Foundation Model API as a fallback.
        
        **To use Genie (recommended):**
        1. Set environment variable: `GENIE_SPACE_ID=your-space-id`
        2. Or add to Databricks App secrets
        3. Restart the app
        
        **For local testing:**
        ```bash
        export GENIE_SPACE_ID=your-space-id
        streamlit run app.py --server.port 8000
        ```
        
        **For Databricks deployment:**
        Add `GENIE_SPACE_ID` to your app.yaml env section.
        """)
    
    parser = QueryParser(ai)
    return ai, parser

# Only initialize if we're past the config page
if 'ai' not in st.session_state:
    st.session_state.ai, st.session_state.parser = init_ai()

# Main app
st.title("🤖 Spiffit AI Calculator")
st.caption("Ask me anything about incentives in plain English!")

# Create tabs for main app and troubleshooting
tab1, tab2 = st.tabs(["💬 Chat", "🔧 Troubleshooting"])

# Sidebar with configuration and examples
with st.sidebar:
    st.header("⚙️ Configuration")
    
    use_genie = st.checkbox("Use Genie", value=False)
    if use_genie:
        genie_space_id = st.text_input("Genie Space ID", placeholder="Enter your space ID")
        if genie_space_id:
            st.session_state.ai.genie_space_id = genie_space_id
    else:
        model_choice = st.selectbox(
            "Foundation Model",
            [
                "databricks-meta-llama-3-1-70b-instruct",
                "databricks-dbrx-instruct",
                "anthropic-claude-3-sonnet",
                "openai-gpt-4"
            ]
        )
        st.session_state.ai.model_name = model_choice
    
    st.markdown("---")
    st.header("📝 Example Questions")
    st.markdown("""
    **Basic Queries:**
    - "What's my incentive?"
    - "Show John Smith's total payout"
    
    **Top Performers:**
    - "Show me the top 10 performers"
    - "Who has the highest MRR?"
    
    **What-If Scenarios:**
    - "What if I close $50K more?"
    - "What if I add $25K in renewals?"
    
    **Comparisons:**
    - "Compare my performance to average"
    - "How do I rank in my region?"
    """)

# Tab 1: Chat Interface
with tab1:
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "👋 Hi! I'm here to help with incentive questions. Try asking me something like 'What's my Q4 incentive?' or 'Show top performers'"
        })
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about incentives..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process the question
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Parse the question
                parsed = st.session_state.parser.parse_question(prompt)
                
                # For demo purposes, show what was understood
                with st.expander("🔍 What I understood"):
                    st.json(parsed)
                
                # Route based on intent
                if parsed['intent'] == "calculate_incentive":
                    if parsed['employee_name']:
                        response = f"""
I would calculate the incentive for **{parsed['employee_name']}** here.

**Next steps to complete this:**
1. Connect to your Delta Lake tables (from cursor/prototypes)
2. Import IncentiveCalculator class
3. Call: `calculator.calculate_total_incentive("{parsed['employee_name']}")`
4. Format the results with the AI helper

**For now, this is a demo showing the query parsing works!**
"""
                    else:
                        response = "I'd love to help! Could you tell me whose incentive you want to calculate?"
                
                elif parsed['intent'] == "what_if":
                    if parsed['employee_name'] and parsed['additional_amount']:
                        response = f"""
I would run a what-if scenario for **{parsed['employee_name']}** 
adding **${parsed['additional_amount']:,.0f}** to their {parsed['metric']}.

**Next steps:**
1. Call: `calculator.calculate_what_if_scenario("{parsed['employee_name']}", {parsed['additional_amount']})`
2. Show the projection with tier changes
"""
                    else:
                        response = "For what-if scenarios, I need a name and amount. Try: 'What if John Smith closes $50K more?'"
                
                elif parsed['intent'] == "show_top":
                    response = f"""
I would show the top performers by **{parsed['metric']}** here.

**Next steps:**
1. Call: `calculator.get_top_performers(metric="{parsed['metric']}", limit=10)`
2. Format as a leaderboard
"""
                
                elif parsed['intent'] == "compare":
                    response = "Comparison queries are coming soon! For now, try asking about specific employee incentives."
                
                else:
                    # Fall back to AI
                    response = st.session_state.ai.ask_question(prompt)
                
                st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

# Tab 2: Troubleshooting & Environment
with tab2:
    st.header("🔧 Troubleshooting & Environment Info")
    
    st.markdown("### 🔍 Environment Variables")
    env_vars = {
        "GENIE_SPACE_ID": os.getenv("GENIE_SPACE_ID"),
        "GENIE_SALES_SPACE_ID": os.getenv("GENIE_SALES_SPACE_ID"),
        "GENIE_ANALYTICS_SPACE_ID": os.getenv("GENIE_ANALYTICS_SPACE_ID"),
        "GENIE_MARKET_SPACE_ID": os.getenv("GENIE_MARKET_SPACE_ID"),
        "DATABRICKS_PROFILE": os.getenv("DATABRICKS_PROFILE"),
    }
    
    st.json(env_vars)
    
    st.markdown("### ✅ Connection Status")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.ai.genie_space_id:
            st.success(f"**Genie Connected:** {st.session_state.ai.genie_space_id}")
        else:
            st.error("**Genie:** Not connected")
    
    with col2:
        st.info(f"**Model:** {st.session_state.ai.model_name}")
    
    st.markdown("### 📊 Configuration")
    config_info = {
        "Using Genie": bool(st.session_state.ai.genie_space_id),
        "Genie Space ID": st.session_state.ai.genie_space_id or "Not configured",
        "Foundation Model": st.session_state.ai.model_name,
        "Workspace Client": "Connected" if st.session_state.ai.workspace else "Not connected"
    }
    st.json(config_info)
    
    st.markdown("### 🎯 Expected Genie Space IDs")
    st.markdown("""
    Based on your `app.yaml` configuration, these space IDs should be loaded:
    
    - **Sales:** `01f0c403c3cf184e9b7f1f6c9ee45905` (spg-mocking-bird-sales)
    - **Analytics:** `01f0c404048613b3b494b1a64a1bca84` (spg-mocking-bird-analytics)
    - **Market:** `01f0c4043acf19dc936c37fd2a8bced3` (spg-mocking-bird-market)
    
    **If these are `None` above**, the environment variables from `app.yaml` are not loading.
    """)
    
    st.markdown("### 💡 Troubleshooting Steps")
    
    if not os.getenv("GENIE_SPACE_ID"):
        st.warning("""
        **⚠️ GENIE_SPACE_ID not found in environment**
        
        **Possible causes:**
        1. Git push didn't include latest `app.yaml`
        2. App needs to be redeployed after `app.yaml` changes
        3. Environment variables syntax issue in `app.yaml`
        
        **To fix:**
        1. Verify `app.yaml` has env section with space IDs
        2. Stop the app in Databricks
        3. Redeploy or restart the app
        4. Check this tab again after restart
        """)
    else:
        st.success("✅ Environment variables are loading correctly!")
    
    st.markdown("### 🔄 Quick Actions")
    if st.button("Test Databricks Connection"):
        try:
            # Try a simple operation
            st.session_state.ai.workspace.current_user.me()
            st.success("✅ Successfully connected to Databricks!")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
    
    if st.button("Test Genie Query"):
        if st.session_state.ai.genie_space_id:
            try:
                response = st.session_state.ai.ask_question("Show me the top performers")
                st.success("✅ Genie query successful!")
                with st.expander("Response"):
                    st.write(response)
            except Exception as e:
                st.error(f"❌ Genie query failed: {str(e)}")
        else:
            st.warning("⚠️ Genie Space ID not configured. Cannot test Genie query.")

# Footer
st.markdown("---")
st.caption("💡 **Next steps:** Connect this to your calculator (cursor/prototypes/02_incentive_calculator.py) to get real results!")

