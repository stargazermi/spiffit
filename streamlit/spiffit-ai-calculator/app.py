"""
Spiffit AI Calculator - Streamlit App
Natural language interface for incentive calculations
"""

import streamlit as st
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
    # Option 1: Use Genie (if you have a space ID)
    # ai = IncentiveAI(genie_space_id="YOUR_GENIE_SPACE_ID")
    
    # Option 2: Use Foundation Model directly
    ai = IncentiveAI(model_name="databricks-meta-llama-3-1-70b-instruct")
    
    parser = QueryParser(ai)
    return ai, parser

# Only initialize if we're past the config page
if 'ai' not in st.session_state:
    st.session_state.ai, st.session_state.parser = init_ai()

# Main app
st.title("🤖 Spiffit AI Calculator")
st.caption("Ask me anything about incentives in plain English!")

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

# Chat interface
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

# Footer
st.markdown("---")
st.caption("💡 **Next steps:** Connect this to your calculator (cursor/prototypes/02_incentive_calculator.py) to get real results!")

