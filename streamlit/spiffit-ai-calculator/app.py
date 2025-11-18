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
import re
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
APP_VERSION = "v2.7.1-SPIFFIT"  # 🔐 Separate PAT Token for Cross-Workspace Auth
DEPLOYMENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"App starting - Version: {APP_VERSION}, Deployment: {DEPLOYMENT_TIME}")
logger.info("🎸 When a problem comes along... you must Spiff It! 🎸")

# Page configuration
st.set_page_config(
    page_title="Spiffit - Spiff It Good!",
    page_icon="⚡",
    layout="wide"
)

# Helper function to format data for email
def format_for_email(answer_text):
    """
    Format query results for email copying
    Returns (is_copyable, formatted_text, csv_data, headers, data_rows) tuple
    """
    # Detect if this looks like winner/SPIFF data
    keywords = ['winner', 'spiff', 'earned', 'employee', 'november', 'october', 'september', 'month']
    has_data_keywords = any(keyword in answer_text.lower() for keyword in keywords)
    has_table = '|' in answer_text and '---' in answer_text
    
    if not (has_data_keywords and has_table):
        return False, None, None, None, None
    
    # Extract table from markdown
    lines = answer_text.split('\n')
    table_lines = []
    in_table = False
    
    for line in lines:
        if '|' in line:
            in_table = True
            table_lines.append(line)
        elif in_table and line.strip() == '':
            break  # End of table
    
    if len(table_lines) < 3:  # Need at least header, separator, and one data row
        return False, None, None, None, None
    
    # Parse table
    header_line = table_lines[0].strip('|').strip()
    headers = [h.strip() for h in header_line.split('|')]
    
    # Skip separator line (---), get data rows
    data_rows = []
    for line in table_lines[2:]:  # Skip header and separator
        if '---' not in line and '|' in line:
            row = line.strip('|').strip()
            cells = [c.strip() for c in row.split('|')]
            if cells and cells[0]:  # Has data
                data_rows.append(cells)
    
    if not data_rows:
        return False, None, None, None, None
    
    # Format for email (text)
    email_lines = []
    email_lines.append("SPIFF Winners")
    email_lines.append("=" * 60)
    email_lines.append("")
    
    # Determine column widths
    col_widths = [max(len(h), 15) for h in headers]
    for row in data_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Format header
    header_formatted = "  ".join([h.ljust(col_widths[i]) for i, h in enumerate(headers)])
    email_lines.append(header_formatted)
    email_lines.append("-" * len(header_formatted))
    
    # Format data rows
    for row in data_rows:
        row_formatted = "  ".join([str(cell).ljust(col_widths[i]) for i, cell in enumerate(row) if i < len(col_widths)])
        email_lines.append(row_formatted)
    
    email_lines.append("")
    email_lines.append(f"Total: {len(data_rows)} recipients")
    
    email_text = "\n".join(email_lines)
    
    # Create CSV format for download
    csv_lines = []
    csv_lines.append(",".join([f'"{h}"' for h in headers]))  # CSV header
    for row in data_rows:
        csv_lines.append(",".join([f'"{cell}"' for cell in row]))  # CSV rows
    csv_data = "\n".join(csv_lines)
    
    return True, email_text, csv_data, headers, data_rows

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
        genie_voice_activations_id=os.getenv("GENIE_VOICE_ACTIVATIONS_SPACE_ID"),
        orchestrator_model="databricks-gpt-5-1"  # Use GPT-5.1 from serving endpoints
    )
    
    return ai, parser, multi_agent

# Only initialize if we're past the config page
if 'ai' not in st.session_state:
    st.session_state.ai, st.session_state.parser, st.session_state.multi_agent = init_ai()

# Main app - "Spiff It" theme!
st.title("⚡ Spiffit - When SPIFFs Get Tough, You Must Spiff It!")
st.markdown("### 🎸 *Spiff it good!* - AI-powered sales incentive intelligence")
st.caption("💪 Powered by multi-agent AI + Databricks Genie + 100% pure hackathon energy!")

# Create tabs: Chat (demo), Intelligence (debug), Architecture, Troubleshooting
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🧠 Intelligence", "📐 Architecture & Tech Stack", "🔧 Troubleshooting"])

# Sidebar with configuration and examples
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Foundation Model for the orchestrator/agent brain
    model_choice = st.selectbox(
        "🤖 Agent Brain (Orchestrator)",
        [
            # 🏆 Tier 1: Best Overall (Recommended)
            "databricks-gpt-5-1",                           # ⭐ GPT-5.1 (Latest OpenAI)
            "databricks-claude-sonnet-4-5",                 # ⭐ Claude Sonnet 4.5 (Latest Anthropic)
            "databricks-meta-llama-3-3-70b-instruct",       # ⭐ Llama 3.3 70B (Newest Meta)
            "databricks-llama-4-maverick",                  # ⭐ Llama 4 Maverick (Cutting edge)
            
            # 💎 Tier 2: Premium (Most Powerful)
            "databricks-claude-opus-4-1",                   # Most powerful reasoning
            "databricks-gpt-5",                             # GPT-5
            "databricks-meta-llama-3-1-405b-instruct",      # Largest model (405B)
            "databricks-gemini-2-5-pro",                    # Google Gemini 2.5 Pro
            "databricks-gpt-oss-120b",                      # Custom GPT 120B
            
            # ⚡ Tier 3: Fast & Efficient
            "databricks-gpt-5-mini",                        # GPT-5 Mini
            "databricks-gpt-5-nano",                        # GPT-5 Nano (Fastest)
            "databricks-gemini-2-5-flash",                  # Gemini Flash (Fast)
            "databricks-meta-llama-3-1-8b-instruct",        # Llama 8B (Budget)
            
            # 🎨 Other Options
            "databricks-claude-opus-4",                     # Claude Opus 4
            "databricks-claude-sonnet-4",                   # Claude Sonnet 4
            "databricks-claude-3-7-sonnet",                 # Claude 3.7 Sonnet
            "databricks-gpt-oss-20b",                       # Custom GPT 20B
            "databricks-gemma-3-12b",                       # Gemma 3 12B
        ],
        help="Which LLM the multi-agent uses for routing & synthesis (15 models available!)"
    )
    st.session_state.ai.model_name = model_choice
    
    st.caption("🧠 **Multi-Agent Always Active:**")
    st.caption("✅ 4 Genie Spaces (1 cross-workspace)  \n✅ Web Search  \n✅ Smart Routing")
    
    st.markdown("---")
    st.header("🎸 Spiff It Examples")
    st.markdown("**🎵 When a problem comes along... you must Spiff It!**")
    st.markdown("*Click any example to try it:*")
    
    # Initialize input state (for programmatic button clicks)
    if "chat_input_from_button" not in st.session_state:
        st.session_state.chat_input_from_button = None
    if "intelligence_input" not in st.session_state:
        st.session_state.intelligence_input = None
    
    st.markdown("**⚡ Quick Hits (Single Genie):**")
    if st.button("📊 Top performers", use_container_width=True, key="ex1"):
        st.session_state.chat_input_from_button = "Show me the top performers this quarter"
    if st.button("🏆 Winners circle", use_container_width=True, key="ex2"):
        st.session_state.chat_input_from_button = "Who won the last SPIFF competition?"
    
    st.markdown("**🚀 Multi-Agent Power:**")
    if st.button("⚔️ Beat the competition!", use_container_width=True, key="ex3"):
        st.session_state.chat_input_from_button = "Compare our top performers with AT&T's SPIFF programs"
    if st.button("💡 Next month's play", use_container_width=True, key="ex4"):
        st.session_state.chat_input_from_button = "Based on our sales data and competitor intel, what SPIFFs should we offer next month?"
    if st.button("📈 Market domination", use_container_width=True, key="ex5"):
        st.session_state.chat_input_from_button = "How do our incentives compare to Verizon and T-Mobile?"
    
    st.markdown("**🧠 Full Auto (Smart Routing):**")
    if st.button("🎯 Spiff it GOOD!", use_container_width=True, key="ex6"):
        st.session_state.chat_input_from_button = "Should we increase our SPIFF budget? Consider sales performance, leaderboards, and what competitors are doing."
    
    st.markdown("---")
    st.markdown("**🔧 Test Individual Genies:**")
    st.caption("Verify each Genie space is working")
    
    if st.button("📊 Sales Genie", use_container_width=True, key="test_sales"):
        st.session_state.chat_input_from_button = "Show me our sales performance data"
    if st.button("📈 Analytics Genie", use_container_width=True, key="test_analytics"):
        st.session_state.chat_input_from_button = "Who won the recent SPIFF competitions?"
    if st.button("🌐 Market Genie", use_container_width=True, key="test_market"):
        st.session_state.chat_input_from_button = "What market intelligence data do we have?"
    
    st.markdown("**📞 Voice Activations (Cross-Workspace):**")
    st.caption("⚠️ Testing data analyst's fine-tuned Genie")
    if st.button("🎤 Voice Incentive Calc", use_container_width=True, key="test_voice"):
        # Formatted prompt for Voice Activations incentive calculation
        voice_prompt = """Return opportunity owner, sum MRR, and group by opportunity owner. Calculate incentive payout based on:

Voice Activations Incentive: (Payout Min. $250 MRR = $300 | $1000+ MRR = $1000)
• Designed to encourage sellers to drive incremental VOIP sales, including both new logo customers and existing customers adding incremental VOIP MRR
• Based on Opportunity Level
• Applies to any NEW Incremental VOIP MRR (Renewals are excluded):
  - New Logo Customers
  - Customers without Voice products
  - Customers with existing Voice products who are adding additional, incremental VOIP lines (this is not a renewal or swap)
• Incremental VOIP sales must generate new MRR
• Migrations or upgrades to incremental VOIP services that generate new MRR are included, while renewals or product swaps without revenue gain are excluded
• Reporting: The Net MRR is specifically separated from Renewal MRR to ensure that only new or incremental VOIP sales are counted, excluding renewals or migrations with no additional revenue gain"""
        st.session_state.chat_input_from_button = voice_prompt

# Tab 1: Chat (Clean Demo View)
with tab1:
    st.header("💬 Spiffit Chat")
    st.caption("⚡ Clean demo interface - just you and the AI agent")
    
    # Initialize chat history (separate from intelligence tab)
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": """👋 **Welcome to Spiffit!**
            
I'm your AI-powered SPIFF intelligence agent. I can help you:
- 📊 Analyze sales performance and incentives
- 🏆 Track SPIFF winners and leaderboards
- 🔍 Research competitor offers and programs
- 💡 Get strategic recommendations

**Try the examples in the sidebar →** or ask me anything!
"""
        })
    
    # Display chat history (CLEAN - no debug info)
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show copy button for assistant messages with data
            if message["role"] == "assistant":
                is_copyable, email_format, csv_data, headers, data_rows = format_for_email(message["content"])
                if is_copyable and email_format:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        with st.expander("📧 Copy for Email", expanded=False):
                            st.caption("Click the copy button on the right →")
                            st.code(email_format, language=None)
                    with col2:
                        st.download_button(
                            label="📎 Download CSV",
                            data=csv_data,
                            file_name=f"spiff_winners_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            help="Download data as CSV to attach to email",
                            key=f"download_{hash(message['content'])}"
                        )
    
    # Chat input (check for programmatic input from sidebar first)
    if st.session_state.chat_input_from_button:
        chat_prompt = st.session_state.chat_input_from_button
        st.session_state.chat_input_from_button = None  # Clear after use
    else:
        chat_prompt = st.chat_input("Ask anything about SPIFFs, sales, or competitors...", key="chat_input")
    
    if chat_prompt:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": chat_prompt})
        with st.chat_message("user"):
            st.markdown(chat_prompt)
        
        # Process with multi-tool agent
        with st.chat_message("assistant"):
            try:
                with st.spinner("🤔 Thinking..."):
                    import time
                    start_time = time.time()
                    result = st.session_state.multi_agent.query(chat_prompt)
                    elapsed = time.time() - start_time
                
                # Filter out SQL queries for clean demo view
                answer = result["answer"]
                
                # Remove SQL Query sections (they're verbose for demo)
                # Remove "**SQL Query:**\n```sql\n...\n```" blocks
                answer = re.sub(r'\*\*SQL Query:\*\*\s*```sql.*?```', '', answer, flags=re.DOTALL)
                # Remove standalone SQL code blocks
                answer = re.sub(r'```sql.*?```', '', answer, flags=re.DOTALL)
                # Clean up extra whitespace
                answer = re.sub(r'\n{3,}', '\n\n', answer).strip()
                
                # Display clean answer
                st.markdown(answer)
                
                # Check if this is copyable data (winners, SPIFFs, etc.)
                is_copyable, email_format, csv_data, headers, data_rows = format_for_email(answer)
                if is_copyable and email_format:
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        with st.expander("📧 Copy for Email", expanded=False):
                            st.caption("Click the copy button on the right to copy this formatted text →")
                            st.code(email_format, language=None)
                            st.caption("💡 Paste directly into your email - formatting preserved!")
                    with col2:
                        st.download_button(
                            label="📎 Download CSV",
                            data=csv_data,
                            file_name=f"spiff_winners_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            help="Download data as CSV to attach to email",
                            key=f"download_new_{datetime.now().timestamp()}"
                        )
                
                # Add subtle performance indicator
                if elapsed > 15:
                    st.caption(f"_Response time: {elapsed:.1f}s_")
                
                # Save response (clean - no SQL queries)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.caption("💡 Check the Intelligence tab for debugging details")
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Tab 2: Intelligence (Debug View)
with tab2:
    st.header("🧠 Intelligence - Debug Mode")
    st.caption("🔧 See how the AI agent thinks and routes queries (for development/troubleshooting)")
    
    # Initialize intelligence chat history
    if "intelligence_messages" not in st.session_state:
        st.session_state.intelligence_messages = []
        st.session_state.intelligence_messages.append({
            "role": "assistant",
            "content": """👋 **Welcome to Spiffit Multi-Agent!**
            
I can intelligently route your questions across:
- 🏢 **4 Genie Spaces** (Sales, Analytics, Market, Voice Activations*)
- 🌐 **Web Search** for competitor intel
- 🤖 **Foundation Models** for synthesis

**Try the examples in the sidebar →** or ask anything!

💡 **I'll show you which agents I use for each query.**

_*Voice Activations is in another workspace (data analyst fine-tuning)_
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
            
            # Show copy/download for assistant messages with data
            if message["role"] == "assistant":
                is_copyable, email_format, csv_data, headers, data_rows = format_for_email(message["content"])
                if is_copyable and email_format:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        with st.expander("📧 Copy for Email", expanded=False):
                            st.caption("Click the copy button on the right →")
                            st.code(email_format, language=None)
                    with col2:
                        st.download_button(
                            label="📎 Download CSV",
                            data=csv_data,
                            file_name=f"spiff_winners_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            help="Download data as CSV to attach to email",
                            key=f"intel_download_{hash(message['content'])}"
                        )
    
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
                if "genie_voice_activations" in result.get("tools_used", []):
                    genie_calls.append("Voice Activations*")
                
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

# Tab 3: Architecture & Tech Stack
with tab3:
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

# Tab 4: Troubleshooting & Environment
with tab4:
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

