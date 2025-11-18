"""
Spiffit AI Calculator - Streamlit App
Natural language interface for incentive calculations
"""

# Load environment variables from .env file (for local testing)
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import logging
from datetime import datetime
from io import StringIO
from ai_helper import IncentiveAI
from query_parser import QueryParser
from multi_tool_agent import MultiToolAgent
from web_search_tool import CompetitorSearchTool

# Configure logging to capture in memory
log_stream = StringIO()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(log_stream),  # Capture to string
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger(__name__)

# Version and deployment tracking
APP_VERSION = "v1.4.2"  # Added authentication logging
DEPLOYMENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"App starting - Version: {APP_VERSION}, Deployment: {DEPLOYMENT_TIME}")

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
    
    # Initialize multi-tool agent for competitor intelligence
    multi_agent = MultiToolAgent(
        genie_sales_id=os.getenv("GENIE_SALES_SPACE_ID"),
        genie_analytics_id=os.getenv("GENIE_ANALYTICS_SPACE_ID"),
        genie_market_id=os.getenv("GENIE_MARKET_SPACE_ID"),
        orchestrator_model="databricks-gpt-5-1"  # Use GPT-5.1 from serving endpoints
    )
    
    return ai, parser, multi_agent

# Only initialize if we're past the config page
if 'ai' not in st.session_state:
    st.session_state.ai, st.session_state.parser, st.session_state.multi_agent = init_ai()

# Main app
st.title("🤖 Spiffit AI Calculator")
st.caption("Ask me anything about incentives in plain English!")

# Create tabs for main app, competitor intel, and troubleshooting
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🌐 Competitor Intel", "🔧 Troubleshooting"])

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

# Tab 2: Competitor Intelligence
with tab2:
    st.header("🌐 Competitor Intelligence")
    st.caption("Multi-tool agent: Genie spaces + web search for comprehensive market intelligence")
    
    # Initialize competitor chat history
    if "competitor_messages" not in st.session_state:
        st.session_state.competitor_messages = []
        st.session_state.competitor_messages.append({
            "role": "assistant",
            "content": """👋 **Welcome to Competitor Intelligence!**
            
I can help you research competitor SPIFF programs and compare them with our internal data.

**Try asking:**
- "What SPIFFs is AT&T offering in Q4?"
- "Compare our top performers with Verizon's programs"
- "How do our incentives stack up against competitors?"
- "What are the common themes in competitor promotions?"

💡 **Behind the scenes:** I'll automatically route your query to the right tools:
- 🏢 **Genie spaces** for internal data
- 🌐 **Web search** for competitor intel
- 🤖 **GPT-5.1** for synthesis and recommendations
"""
        })
    
    # Show example queries
    st.markdown("### 📋 Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Search AT&T Programs", key="att_btn"):
            st.session_state.competitor_input = "What SPIFF programs is AT&T offering in Q4 2024?"
        if st.button("📊 Compare All Competitors", key="compare_btn"):
            st.session_state.competitor_input = "Compare SPIFF programs across AT&T, Verizon, and T-Mobile"
    
    with col2:
        if st.button("⚔️ Our SPIFFs vs Competitors", key="vs_btn"):
            st.session_state.competitor_input = "How do our SPIFF programs compare to competitor offerings?"
        if st.button("💡 Get Recommendations", key="rec_btn"):
            st.session_state.competitor_input = "Based on competitor analysis, what SPIFFs should we offer?"
    
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.competitor_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show tool details if available
            if message["role"] == "assistant" and "tool_details" in message:
                with st.expander("🔧 Tools Used"):
                    st.json(message["tool_details"])
    
    # Chat input (check for programmatic input first)
    if "competitor_input" in st.session_state and st.session_state.competitor_input:
        prompt = st.session_state.competitor_input
        st.session_state.competitor_input = None  # Clear after use
    else:
        prompt = st.chat_input("Ask about competitor intelligence...", key="competitor_chat")
    
    if prompt:
        # Add user message
        st.session_state.competitor_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with multi-tool agent
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching across data sources..."):
                try:
                    result = st.session_state.multi_agent.query(prompt)
                    
                    # Display main answer
                    st.markdown(result["answer"])
                    
                    # Show routing and tools used
                    with st.expander("🧠 AI Reasoning & Tools"):
                        st.markdown(f"**Routing Decision:** {result['routing_reasoning']}")
                        st.markdown(f"**Tools Used:** {', '.join(result['tools_used'])}")
                        
                        # Show errors if any
                        if result.get("errors"):
                            st.warning("**⚠️ Some tools encountered errors:**")
                            for tool_name, error in result["errors"].items():
                                st.error(f"**{tool_name}:** {error[:200]}...")
                            st.info("💡 See GENIE_PERMISSIONS_FIX.md for troubleshooting Genie access issues")
                        
                        # Show raw results from each tool
                        if result.get("raw_results"):
                            st.markdown("**📊 Raw Results:**")
                            for tool_name, tool_result in result["raw_results"].items():
                                st.markdown(f"**{tool_name.upper()}:**")
                                st.text(tool_result[:500] + "..." if len(tool_result) > 500 else tool_result)
                    
                    # Save response with metadata
                    st.session_state.competitor_messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "tool_details": {
                            "tools_used": result["tools_used"],
                            "routing_reasoning": result["routing_reasoning"]
                        }
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error querying multi-tool agent: {str(e)}"
                    st.error(error_msg)
                    st.session_state.competitor_messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Tab 3: Troubleshooting & Environment
with tab3:
    st.header("🔧 Troubleshooting & Environment Info")
    
    # Version and Deployment Info
    st.markdown("### 📦 Deployment Info")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Version:** {APP_VERSION}")
    with col2:
        st.info(f"**Deployed:** {DEPLOYMENT_TIME}")
    
    st.caption("💡 **Tip:** If you just redeployed, refresh the page and check if the timestamp updated")
    st.markdown("---")
    
    st.markdown("### 🔍 Environment Variables")
    
    # Authentication variables
    st.markdown("#### 🔐 Authentication")
    auth_vars = {
        "DATABRICKS_HOST": os.getenv("DATABRICKS_HOST") or "Not set",
        "DATABRICKS_TOKEN": "***" + os.getenv("DATABRICKS_TOKEN", "")[-4:] if os.getenv("DATABRICKS_TOKEN") else "Not set",
        "DATABRICKS_PROFILE": os.getenv("DATABRICKS_PROFILE") or "Not set",
    }
    st.json(auth_vars)
    
    # Genie space variables
    st.markdown("#### 🧠 Genie Spaces")
    genie_vars = {
        "GENIE_SPACE_ID": os.getenv("GENIE_SPACE_ID") or "Not set",
        "GENIE_SALES_SPACE_ID": os.getenv("GENIE_SALES_SPACE_ID") or "Not set",
        "GENIE_ANALYTICS_SPACE_ID": os.getenv("GENIE_ANALYTICS_SPACE_ID") or "Not set",
        "GENIE_MARKET_SPACE_ID": os.getenv("GENIE_MARKET_SPACE_ID") or "Not set",
    }
    st.json(genie_vars)
    
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
    
    # Test Genie Query Section
    test_col1, test_col2 = st.columns([1, 3])
    with test_col1:
        test_genie = st.button("Test Genie Query", key="test_genie_btn", use_container_width=True)
    with test_col2:
        refresh_logs = st.button("🔄 Refresh Logs", key="refresh_logs_btn", use_container_width=True)
    
    # Display results in a persistent container
    test_results = st.container()
    
    if test_genie:
        with test_results:
            if st.session_state.ai.genie_space_id:
                with st.spinner("Testing Genie connection..."):
                    try:
                        logger.info("User clicked 'Test Genie Query' button")
                        response = st.session_state.ai.ask_question("Show me the top performers")
                        st.success("✅ Genie query successful!")
                        st.markdown("**📄 Response:**")
                        st.info(response)
                    except Exception as e:
                        st.error(f"❌ Genie query failed: {str(e)}")
            else:
                st.warning("⚠️ Genie Space ID not configured. Cannot test Genie query.")
    
    st.markdown("---")
    st.markdown("### 📜 Authentication & API Logs")
    st.caption("Shows authentication method and Genie API calls")
    
    # Get current logs
    log_contents = log_stream.getvalue()
    
    if log_contents:
        # Show last 100 lines
        log_lines = log_contents.split('\n')
        recent_logs = '\n'.join(log_lines[-100:])
        
        st.text_area(
            "Recent Logs",
            value=recent_logs,
            height=400,
            key="log_viewer"
        )
        
        st.caption(f"📊 Showing last 100 log entries (Total: {len(log_lines)} lines)")
    else:
        st.info("No logs yet. Click 'Test Genie Query' or interact with the app to generate logs.")

# Footer
st.markdown("---")
st.caption("💡 **Next steps:** Connect this to your calculator (cursor/prototypes/02_incentive_calculator.py) to get real results!")

