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
APP_VERSION = "v2.0.4-DEMO"  # Better result data formatting + performance logging
DEPLOYMENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"App starting - Version: {APP_VERSION}, Deployment: {DEPLOYMENT_TIME}")

# Page configuration
st.set_page_config(
    page_title="Spiffit Multi-Agent",
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
st.title("🤖 Spiffit Multi-Agent")
st.caption("Intelligent SPIFF analysis powered by multiple AI agents and Genie spaces")

# Create tabs for intelligence, architecture, and troubleshooting
tab1, tab2, tab3 = st.tabs(["🧠 Intelligence", "📐 Architecture & Tech Stack", "🔧 Troubleshooting"])

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
    st.markdown("**Click any example to try it:**")
    
    # Initialize input state
    if "intelligence_input" not in st.session_state:
        st.session_state.intelligence_input = None
    
    st.markdown("**🔍 Single Agent (One Genie Space):**")
    if st.button("📊 Top sales performers", use_container_width=True, key="ex1"):
        st.session_state.intelligence_input = "Show me the top performers this quarter"
    if st.button("🏆 Recent SPIFF winners", use_container_width=True, key="ex2"):
        st.session_state.intelligence_input = "Who won the last SPIFF competition?"
    
    st.markdown("**🤖 Multi-Agent (Multiple Genies + Routing):**")
    if st.button("⚔️ Internal vs Competitors", use_container_width=True, key="ex3"):
        st.session_state.intelligence_input = "Compare our top performers with AT&T's SPIFF programs"
    if st.button("💡 Strategic Recommendations", use_container_width=True, key="ex4"):
        st.session_state.intelligence_input = "Based on our sales data and competitor intel, what SPIFFs should we offer next month?"
    if st.button("📈 Market Analysis", use_container_width=True, key="ex5"):
        st.session_state.intelligence_input = "How do our incentives compare to Verizon and T-Mobile?"
    
    st.markdown("**🧠 Smart Routing (AI chooses best sources):**")
    if st.button("🎯 Comprehensive Analysis", use_container_width=True, key="ex6"):
        st.session_state.intelligence_input = "Should we increase our SPIFF budget? Consider sales performance, leaderboards, and what competitors are doing."

# Tab 1: Intelligence (Multi-Agent)
with tab1:
    st.header("🧠 Multi-Agent Intelligence")
    st.caption("Query multiple Genie spaces + web search with smart routing")
    
    # Initialize intelligence chat history
    if "intelligence_messages" not in st.session_state:
        st.session_state.intelligence_messages = []
        st.session_state.intelligence_messages.append({
            "role": "assistant",
            "content": """👋 **Welcome to Spiffit Multi-Agent!**
            
I can intelligently route your questions across:
- 🏢 **3 Genie Spaces** (Sales, Analytics, Market)
- 🌐 **Web Search** for competitor intel
- 🤖 **Foundation Models** for synthesis

**Try the examples in the sidebar →** or ask anything!

💡 **I'll show you which agents I use for each query.**
"""
        })
    
    # Display chat history
    for message in st.session_state.intelligence_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show which Genies were called
            if message["role"] == "assistant" and "genie_calls" in message:
                st.info(f"**🧠 Genies Called:** {', '.join(message['genie_calls'])}")
            
            # Show tool details if available
            if message["role"] == "assistant" and "tool_details" in message:
                with st.expander("🔧 Tools & Routing Details"):
                    st.json(message["tool_details"])
    
    # Chat input (check for programmatic input from sidebar first)
    if st.session_state.intelligence_input:
        prompt = st.session_state.intelligence_input
        st.session_state.intelligence_input = None  # Clear after use
    else:
        prompt = st.chat_input("Ask anything about SPIFFs, sales, or competitors...", key="intelligence_chat")
    
    if prompt:
        # Add user message
        st.session_state.intelligence_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with multi-tool agent
        with st.chat_message("assistant"):
            try:
                # Show progress with timing
                import time
                with st.spinner("🔍 Analyzing query and routing to best agents..."):
                    start_time = time.time()
                    result = st.session_state.multi_agent.query(prompt)
                    elapsed = time.time() - start_time
                
                # Debug: Check if answer is just the question echoed back
                if result["answer"] == prompt or len(result["answer"].strip()) == 0:
                    st.warning(f"⚠️ **Debug:** Genie returned empty or echoed response")
                    st.info(f"**Raw result object:**\n```python\n{result}\n```")
                    st.markdown("**This might mean:**")
                    st.markdown("- Genie space has no data or tables")
                    st.markdown("- SQL warehouse is stopped or has issues")
                    st.markdown("- Genie query timed out")
                    st.markdown(f"**Query took:** {elapsed:.1f}s")
                else:
                    # Display main answer with performance feedback
                    if elapsed > 15:
                        st.warning(f"⏰ Got response in {elapsed:.1f}s (slow - SQL warehouse may have been stopped)")
                        st.caption("💡 **Tip:** Keep SQL warehouse running for faster queries (~3-5s)")
                    elif elapsed > 8:
                        st.info(f"✅ Got response in {elapsed:.1f}s (normal for first query)")
                    else:
                        st.success(f"✅ Got response in {elapsed:.1f}s")
                    
                    st.markdown(result["answer"])
                
                # Determine which Genies were called
                genie_calls = []
                if "genie_sales" in result.get("tools_used", []):
                    genie_calls.append("Sales")
                if "genie_analytics" in result.get("tools_used", []):
                    genie_calls.append("Analytics")
                if "genie_market" in result.get("tools_used", []):
                    genie_calls.append("Market")
                
                # Show which Genies were used
                if genie_calls:
                    st.info(f"**🧠 Genies Called:** {', '.join(genie_calls)}")
                
                # Show routing and tools used
                with st.expander("🧠 AI Reasoning & Smart Routing"):
                    st.markdown(f"**Routing Decision:** {result['routing_reasoning']}")
                    st.markdown(f"**Tools Used:** {', '.join(result['tools_used'])}")
                    
                    # Show errors if any
                    if result.get("errors"):
                        st.warning("**⚠️ Some tools encountered errors:**")
                        for tool_name, error in result["errors"].items():
                            st.error(f"**{tool_name}:** {error[:200]}...")
                        st.info("💡 Check Troubleshooting tab for Genie connection details")
                    
                    # Show raw results from each tool
                    if result.get("raw_results"):
                        st.markdown("**📊 Raw Results from Each Agent:**")
                        for tool_name, tool_result in result["raw_results"].items():
                            st.markdown(f"**{tool_name.upper()}:**")
                            st.code(tool_result[:500] + "..." if len(tool_result) > 500 else tool_result)
                
                # Save response with metadata
                st.session_state.intelligence_messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "genie_calls": genie_calls,
                    "tool_details": {
                        "routing": result["routing_reasoning"],
                        "tools": result["tools_used"],
                        "errors": result.get("errors", {}),
                    }
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.intelligence_messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Tab 2: Architecture & Tech Stack
with tab2:
    st.header("📐 Architecture & Tech Stack")
    st.caption("Multi-agent system architecture powered by Databricks")
    
    # Architecture Overview
    st.markdown("## 🏗️ System Architecture")
    st.markdown("""
This is a **multi-agent AI system** that intelligently routes queries across multiple specialized agents:

```
User Query
    ↓
🤖 Orchestrator (Llama 3.1 70B)
    ↓
    ├─→ 🧠 Genie Agent: Sales Performance
    ├─→ 🧠 Genie Agent: Analytics & Winners  
    ├─→ 🧠 Genie Agent: Market Intelligence
    ├─→ 🌐 Web Search Agent (Competitor Intel)
    └─→ 📊 Foundation Model (Synthesis)
    ↓
🧠 AI Synthesis & Response
```

### 🔄 Smart Routing Flow

1. **Query Analysis**: LLM analyzes intent and determines best sources
2. **Parallel Execution**: Multiple agents query simultaneously
3. **Error Handling**: Graceful fallbacks if any agent fails
4. **Synthesis**: Combine results into comprehensive answer
5. **Transparency**: Show which agents were used

---
""")
    
    # Databricks Components Used
    st.markdown("## 🛠️ Databricks Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🤖 Agent Tools")
        st.markdown("""
**Genie** (Natural Language to SQL)
- 3 specialized spaces
- Real-time SQL query generation
- Data exploration via conversation

**Foundation Models** (LLM Platform)
- Meta Llama 3.1 70B (Orchestrator)
- GPT-5.1 (Synthesis)
- Claude Opus 4.1 (Available)
- Gemini 2.5 (Available)

**Databricks Apps**
- Streamlit hosting
- Secure authentication
- Auto-scaling infrastructure
""")
    
    with col2:
        st.markdown("### 📊 Data & Infrastructure")
        st.markdown("""
**Unity Catalog**
- Data governance
- Schema: `hackathon.hackathon_spiffit`
- Tables: sales, winners, competitors

**SQL Warehouse**
- Serverless compute
- Genie backend
- Real-time queries

**GitHub Integration**
- Version control
- CI/CD deployment
- Repo: `/Shared/spiffit-dev`
""")
    
    # Models Used
    st.markdown("---")
    st.markdown("## 🎯 Models in Use")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
**🧠 Orchestrator**

**Model:** Llama 3.1 70B Instruct

**Role:** Query routing, intent analysis

**Why:** Fast, capable reasoning
""")
    
    with col2:
        st.success("""
**🤖 Synthesis**

**Model:** GPT-5.1 (mock)

**Role:** Combine multi-source results

**Why:** Strong coherence, context understanding
""")
    
    with col3:
        st.warning("""
**🧠 Genie Backend**

**Model:** Databricks-tuned LLM

**Role:** SQL generation from natural language

**Why:** Optimized for data queries
""")
    
    # Genie Spaces Configuration
    st.markdown("---")
    st.markdown("## 🧠 Configured Genie Spaces")
    
    genie_sales_id = os.getenv("GENIE_SALES_SPACE_ID", "Not configured")
    genie_analytics_id = os.getenv("GENIE_ANALYTICS_SPACE_ID", "Not configured")
    genie_market_id = os.getenv("GENIE_MARKET_SPACE_ID", "Not configured")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Sales Performance")
        if genie_sales_id != "Not configured":
            st.success(f"✅ Connected")
            with st.expander("Details"):
                st.code(f"Space ID: {genie_sales_id}")
                st.markdown("""
**Data:**
- Sales performance
- AE metrics
- Deal pipeline
- Quota attainment
""")
        else:
            st.error("❌ Not configured")
    
    with col2:
        st.markdown("### 🏆 Analytics & Winners")
        if genie_analytics_id != "Not configured":
            st.success(f"✅ Connected")
            with st.expander("Details"):
                st.code(f"Space ID: {genie_analytics_id}")
                st.markdown("""
**Data:**
- SPIFF winners
- Leaderboards
- Historical results
- Incentive payouts
""")
        else:
            st.error("❌ Not configured")
    
    with col3:
        st.markdown("### 🌐 Market Intelligence")
        if genie_market_id != "Not configured":
            st.success(f"✅ Connected")
            with st.expander("Details"):
                st.code(f"Space ID: {genie_market_id}")
                st.markdown("""
**Data:**
- Competitor SPIFFs
- Market trends
- Industry benchmarks
- Pricing intelligence
""")
        else:
            st.error("❌ Not configured")
    
    # Tech Stack Summary
    st.markdown("---")
    st.markdown("## 📚 Complete Tech Stack")
    st.markdown("""
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive UI |
| **Hosting** | Databricks Apps | Secure deployment |
| **AI Orchestration** | Llama 3.1 70B | Query routing |
| **Data Query** | Genie (3 spaces) | Natural language to SQL |
| **Synthesis** | Foundation Models | Multi-source integration |
| **Data Platform** | Unity Catalog | Governance & storage |
| **Compute** | SQL Warehouse | Serverless query engine |
| **Auth** | PAT Token | API authentication |
| **Version Control** | GitHub | Code management |
| **Languages** | Python 3.11 | Application logic |

**Key Innovation:** Smart routing with graceful fallbacks ensures queries succeed even if individual agents fail.
""")
    
    # How to check Genie calls in Databricks
    st.markdown("---")
    st.markdown("## 🔍 Verify Genie Calls in Databricks")
    st.markdown("""
To see which Genie spaces are actually being called in Databricks:

1. **Navigate to your Databricks workspace:**
   - Go to: `https://dbc-4a93b454-f17b.cloud.databricks.com/`

2. **Open SQL Warehouse Query History:**
   - Click **SQL** in the left sidebar
   - Select **SQL Warehouses**
   - Find: `hackaithon_Spiffit_serverless`
   - Click **Query History** tab

3. **Filter by time:**
   - Set time range to **Last hour**
   - You'll see all SQL queries generated by Genie

4. **Identify which Genie space was used:**
   - Each query shows the **database/schema** accessed
   - Look for `hackathon.hackathon_spiffit.*` tables
   - Match to Genie space:
     - `sales_performance` → **Sales Genie**
     - `spiff_winners` → **Analytics Genie**
     - `competitor_spiffs` → **Market Genie**

5. **View in Genie UI:**
   - Go to **Genie** in the left sidebar
   - Click on each Genie space
   - View **Conversation History** to see all queries

💡 **Pro Tip:** The **Intelligence tab** above shows which Genies were called directly in the UI!
""")

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

