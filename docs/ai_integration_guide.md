# AI Integration Quick Reference
## Hour 5-6: Adding Natural Language to Your App

Since Genie is already set up, here's how to connect it to your calculations.

---

## 🎯 Goal
Transform this:
```python
calculator.calculate_total_incentive("John Smith")
```

Into this:
```
User: "What's John Smith's incentive?"
AI: "John Smith earned $45,230 this quarter..."
```

---

## 📁 Code Files

All code has been extracted to separate Python files in `spiffit-ai-calculator/`:

- **`ai_helper.py`** - AI/LLM integration (Genie & Foundation Models)
- **`query_parser.py`** - Natural language query parsing & intent extraction
- **`app.py`** - Main Streamlit application with chat interface

---

## 📋 Step-by-Step Implementation

### Step 1: Connect to Genie (10 minutes)

See **`spiffit-ai-calculator/ai_helper.py`** for the full implementation.

Key class:

```python
"""
AI/LLM Integration for Natural Language Queries
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import json
import re

class IncentiveAI:
    """
    Handles natural language queries using Databricks LLMs
    """
    
    def __init__(self):
        self.workspace = WorkspaceClient()
        # Use your Genie space or LLM endpoint name
        self.genie_space_id = "YOUR_GENIE_SPACE_ID"  # Get from Genie UI
        # Or use Foundation Model API
        self.model_name = "databricks-meta-llama-3-1-70b-instruct"  # or gemini, claude
    
    def ask_question(self, question: str, calculator_results: dict = None):
        """
        Process a natural language question
        
        Args:
            question: User's question
            calculator_results: Optional pre-computed results to format
            
        Returns:
            Natural language response
        """
        
        # Option 1: Use Genie if you have a space set up
        if self.genie_space_id:
            return self._ask_genie(question)
        
        # Option 2: Use Foundation Model API directly
        else:
            return self._ask_foundation_model(question, calculator_results)
    
    def _ask_genie(self, question: str):
        """
        Query using Genie space
        """
        try:
            # Genie API call
            response = self.workspace.genie.ask_question(
                space_id=self.genie_space_id,
                content=question
            )
            return response.content
        except Exception as e:
            return f"Genie error: {str(e)}"
    
    def _ask_foundation_model(self, question: str, calculator_results: dict = None):
        """
        Use Foundation Model API (Gemini/Claude/Llama) directly
        """
        
        # Build context from calculator results if provided
        context = ""
        if calculator_results:
            context = f"\n\nAvailable data: {json.dumps(calculator_results, indent=2)}"
        
        # Create prompt
        prompt = f"""You are an AI assistant helping with sales incentive calculations.

User question: {question}
{context}

Provide a clear, conversational answer. If you need specific employee data, ask for it.
If data is provided, format numbers as currency and explain the calculations.
"""
        
        try:
            # Call Foundation Model
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
            return f"LLM error: {str(e)}"
```

---

### Step 2: Extract Intent (15 minutes)

See **`spiffit-ai-calculator/query_parser.py`** for the full implementation.

Key class:

```python
# See spiffit-ai-calculator/query_parser.py for full implementation

class QueryParser:
    """Parse user questions to determine intent and extract parameters"""
    
    def parse_question(self, question: str):
        # Returns: {"intent", "employee_name", "metric", "additional_amount"}
        pass
```

---

### Step 3: Integrate with Calculator (15 minutes)

See **`spiffit-ai-calculator/app.py`** for a complete working demo!

The app currently shows:
- ✅ Query parsing working
- ✅ AI/LLM integration ready
- ⏳ Placeholder for calculator connection

To connect the real calculator:

```python
# In spiffit-ai-calculator/app.py

import streamlit as st
from ai_helper import IncentiveAI
from query_parser import QueryParser
# Add this import after copying calculator code:
from incentive_calculator import IncentiveCalculator

# Initialize
@st.cache_resource
def init_ai():
    ai = IncentiveAI()
    parser = QueryParser(ai)
    return ai, parser

ai, parser = init_ai()

# User input
user_question = st.text_input("Ask me about incentives:", 
                               placeholder="What's John Smith's total incentive?")

if user_question:
    with st.spinner("Thinking..."):
        # Parse the question
        parsed = parser.parse_question(user_question)
        
        st.write(f"**Understood:** {parsed['intent']}")
        
        # Route to appropriate handler
        if parsed['intent'] == "calculate_incentive" and parsed['employee_name']:
            # Calculate
            result = calculator.calculate_total_incentive(parsed['employee_name'])
            
            # Format with AI
            response = ai.ask_question(
                f"Format this incentive data in a friendly way: {result}",
                calculator_results=result
            )
            
            st.success(response)
            
        elif parsed['intent'] == "what_if" and parsed['employee_name'] and parsed['additional_amount']:
            # What-if scenario
            result = calculator.calculate_what_if_scenario(
                parsed['employee_name'], 
                parsed['additional_amount']
            )
            
            response = ai.ask_question(
                f"Explain this scenario: {result}",
                calculator_results=result
            )
            
            st.info(response)
            
        elif parsed['intent'] == "show_top":
            # Top performers
            result = calculator.get_top_performers(metric=parsed['metric'], limit=10)
            
            response = ai.ask_question(
                f"Format this leaderboard: {result}",
                calculator_results=result
            )
            
            st.success(response)
            
        else:
            # Let AI handle it directly
            response = ai.ask_question(user_question)
            st.write(response)
```

---

### Step 4: Test Queries (15 minutes)

Test these 5 question types:

```python
test_questions = [
    # 1. Direct calculation
    "What's my incentive?",
    "Show John Smith's total payout",
    
    # 2. Top performers
    "Show me the top 10 performers",
    "Who has the highest MRR attainment?",
    
    # 3. What-if scenarios
    "What if I close $50K more?",
    "What if John Smith adds $25,000 in renewals?",
    
    # 4. Comparisons
    "Compare my performance to the team average",
    
    # 5. Specific metrics
    "What's my MRR attainment?",
    "Show my renewal numbers"
]

# Add test button
if st.button("Run Tests"):
    for q in test_questions:
        st.write(f"**Q:** {q}")
        # Process and show result
```

---

## 🎯 Alternative: Simpler Approach (If Time is Tight)

If the above is too complex, here's a minimal version:

```python
# Simple keyword-based routing (no LLM needed)

def simple_query_handler(question, calculator):
    question_lower = question.lower()
    
    # Extract name (assume format: "What's [Name]'s incentive?")
    if "what" in question_lower and "incentive" in question_lower:
        # Try to extract name between "what's" and "'s"
        import re
        match = re.search(r"what'?s\s+(.+?)'?s", question, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            result = calculator.calculate_total_incentive(name)
            return result['summary']
    
    # Top performers
    elif "top" in question_lower:
        result = calculator.get_top_performers("mrr", limit=10)
        return result['summary']
    
    # What-if
    elif "what if" in question_lower:
        # Extract name and amount
        # ... simple parsing ...
        pass
    
    else:
        return "I can answer questions like: 'What's John Smith's incentive?' or 'Show top performers'"
```

---

## 📊 Expected Results

After implementation, you should be able to:

✅ **Ask:** "What's my incentive?"  
✅ **Get:** "Your Q4 incentive is $45,230 (MRR: $20K, Renewal: $15K, TCV: $10K)"

✅ **Ask:** "Show top 5 performers"  
✅ **Get:** Formatted leaderboard with rankings

✅ **Ask:** "What if I close $50K more?"  
✅ **Get:** Projection showing new tier and payout increase

---

## 🔧 Configuration Checklist

- [ ] Get your Genie Space ID (from Databricks Genie UI)
- [ ] OR choose Foundation Model endpoint name
- [ ] Test API access with simple query
- [ ] Add error handling for API failures
- [ ] Cache responses to avoid repeated API calls
- [ ] Add conversation history for context

---

## 🆘 Troubleshooting

**"Genie API not working"**
→ Fall back to Foundation Model API directly

**"Can't parse employee names"**
→ Use dropdown selector instead, or maintain employee list

**"Responses are slow"**
→ Cache calculator results, only call LLM for formatting

**"LLM gives wrong answers"**
→ Do calculations in Python first, use LLM only for natural language formatting

---

## 💡 Pro Tips

1. **Calculate First, Format Second**: Do math in Python, use AI only for natural language
2. **Simple Intents**: Start with 3-4 question types, expand later
3. **Fallback to Keywords**: If LLM fails, use simple string matching
4. **Show Raw Data**: Display calculation results even if formatting fails
5. **Test Early**: Test API access before building complex logic

---

**Need the full code?** See `cursor/automation-ideas/implementation-plans/use-case-1-ai-calculator.md` (Step 3)

