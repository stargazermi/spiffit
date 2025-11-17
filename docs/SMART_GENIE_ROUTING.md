# Smart Genie Space Routing

## 📖 Overview

This document explains how to build intelligent routing that automatically selects the best Genie space based on the user's question. Instead of manually deciding which space to query, the system analyzes the question and routes it to the most appropriate data source.

---

## 🤔 The Problem

### Manual Routing (Current Approach)
```python
# You manually decide which space to use
if "sales" in question:
    response = genie_space_a.ask(question)
elif "finance" in question:
    response = genie_space_b.ask(question)
```

**Problems:**
- ❌ Hard to maintain as spaces grow
- ❌ Requires understanding all spaces
- ❌ Misses nuanced questions
- ❌ Doesn't handle ambiguous queries

### Smart Routing (Intelligent Approach)
```python
# System automatically picks the best space
response = router.ask_smart(question)
# Analyzes question → Routes to best space → Returns answer
```

**Benefits:**
- ✅ Automatic space selection
- ✅ Handles complex questions
- ✅ Learns from space descriptions
- ✅ Provides routing confidence
- ✅ Explains routing decisions

---

## 🎯 Implementation: Smart Router

### Complete Implementation

```python
# streamlit/spiffit-ai-calculator/smart_router.py

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import json

class SmartGenieRouter:
    """
    Intelligently routes questions to the best Genie space
    """
    
    def __init__(self):
        self.ws = WorkspaceClient()
        
        # Register your available Genie spaces with descriptions
        self.spaces = {
            "sales_data": {
                "space_id": "01efa5e57638161591974326e56e4807",
                "description": "Sales performance, MRR, TCV, deals, quotas, attainment",
                "expertise": ["sales metrics", "revenue", "deals", "quotas", "AE performance"]
            },
            "analytics": {
                "space_id": "01eff85bf03e1514838b4bc3fe884053",
                "description": "Analytics, trends, comparisons, rankings, statistics",
                "expertise": ["trends", "comparisons", "top performers", "rankings", "analysis"]
            },
            "hr_data": {
                "space_id": "your-hr-space-id",
                "description": "Employee info, roles, territories, hierarchy, compensation bands",
                "expertise": ["employee", "role", "manager", "territory", "hierarchy"]
            }
        }
    
    def route_question(self, question: str):
        """
        Analyze question and route to best Genie space
        
        Returns: (space_id, space_name, confidence)
        """
        
        # Use LLM to classify the question
        classification_prompt = f"""
        Analyze this user question and determine which data source would best answer it.
        
        Question: "{question}"
        
        Available data sources:
        {json.dumps({k: v['description'] for k, v in self.spaces.items()}, indent=2)}
        
        Respond with JSON:
        {{
            "best_space": "space_name",
            "confidence": 0.95,
            "reasoning": "why this space is best"
        }}
        """
        
        # Call Foundation Model to classify
        response = self.ws.serving_endpoints.query(
            name="databricks-meta-llama-3-1-70b-instruct",
            messages=[
                ChatMessage(
                    role=ChatMessageRole.USER,
                    content=classification_prompt
                )
            ]
        )
        
        # Parse classification result
        try:
            classification = json.loads(response.choices[0].message.content)
            space_name = classification["best_space"]
            space_id = self.spaces[space_name]["space_id"]
            confidence = classification["confidence"]
            
            return {
                "space_id": space_id,
                "space_name": space_name,
                "confidence": confidence,
                "reasoning": classification.get("reasoning", "")
            }
        except:
            # Fallback to default space if classification fails
            return {
                "space_id": self.spaces["sales_data"]["space_id"],
                "space_name": "sales_data",
                "confidence": 0.5,
                "reasoning": "Defaulted to sales_data space"
            }
    
    def ask_smart(self, question: str):
        """
        Automatically route question to best Genie space and get answer
        """
        
        # Step 1: Determine best space
        routing = self.route_question(question)
        
        # Step 2: Query that space
        response = self.ws.genie.ask_question(
            space_id=routing["space_id"],
            content=question
        )
        
        return {
            "answer": response.content,
            "routed_to": routing["space_name"],
            "confidence": routing["confidence"],
            "reasoning": routing["reasoning"]
        }
```

---

## 🎯 Streamlit Integration

### Basic Usage

```python
# streamlit/spiffit-ai-calculator/app.py

import streamlit as st
from smart_router import SmartGenieRouter

# Initialize router
@st.cache_resource
def init_router():
    return SmartGenieRouter()

router = init_router()

# User interface
st.title("🧠 Smart Genie Router")
user_question = st.text_input("Ask me anything about your data:")

if user_question:
    with st.spinner("🧠 Analyzing question and routing to best data source..."):
        result = router.ask_smart(user_question)
    
    # Show which space was used
    st.info(f"📍 Routed to: **{result['routed_to']}** (confidence: {result['confidence']*100:.0f}%)")
    
    with st.expander("🔍 Why this space?"):
        st.write(result['reasoning'])
    
    # Show answer
    st.success(result['answer'])
```

### Advanced Usage with Visualization

```python
import streamlit as st
from smart_router import SmartGenieRouter
import pandas as pd

router = SmartGenieRouter()

user_question = st.text_input("Ask a question:")

if user_question:
    # Get routing decision
    routing = router.route_question(user_question)
    
    # Visualize routing confidence
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.metric(
            "Best Space", 
            routing['space_name'],
            f"{routing['confidence']*100:.0f}% confidence"
        )
    
    with col2:
        # Show confidence as progress
        st.progress(routing['confidence'])
    
    # Show reasoning
    st.info(f"💡 {routing['reasoning']}")
    
    # Get actual answer
    with st.spinner("Querying Genie space..."):
        response = router.ws.genie.ask_question(
            space_id=routing['space_id'],
            content=user_question
        )
    
    st.success(response.content)
```

---

## 💬 Example Conversations

### Example 1: Sales Question
```
User: "What was John Smith's Q4 MRR?"

🧠 Router Analysis:
- Best space: "sales_data"
- Confidence: 98%
- Reasoning: "Question asks about MRR (Monthly Recurring Revenue), 
  which is a sales metric found in the sales_data space"

📍 Routed to: sales_data
✅ Answer: "John Smith's Q4 MRR was $125,000..."
```

### Example 2: Ranking Question
```
User: "Who are the top 10 performers by revenue?"

🧠 Router Analysis:
- Best space: "analytics"
- Confidence: 95%
- Reasoning: "Question asks for rankings and top performers, 
  which is best answered by the analytics space"

📍 Routed to: analytics
✅ Answer: "Top 10 performers by revenue:
1. Sarah Johnson - $450K
2. Mike Chen - $420K
..."
```

### Example 3: HR Question
```
User: "What region is John Smith in?"

🧠 Router Analysis:
- Best space: "hr_data"
- Confidence: 92%
- Reasoning: "Question asks about employee territory/region, 
  which is organizational data found in hr_data space"

📍 Routed to: hr_data
✅ Answer: "John Smith is assigned to the Northeast region..."
```

### Example 4: Ambiguous Question
```
User: "How is John Smith doing?"

🧠 Router Analysis:
- Best space: "sales_data"
- Confidence: 75%
- Reasoning: "Ambiguous question likely refers to performance metrics, 
  starting with sales_data. May need to query multiple spaces."

📍 Routed to: sales_data
✅ Answer: "John Smith's performance:
- Q4 MRR: $125,000 (125% of target)
- Overall attainment: Exceeds expectations
Would you like details on specific metrics?"
```

### Example 5: Multi-Space Question
```
User: "Calculate John Smith's incentive"

🧠 Router Analysis:
- Primary space: "sales_data" 
- Confidence: 85%
- Reasoning: "Complex question requires multiple data sources. 
  Starting with sales_data for performance metrics"

📍 Route 1: sales_data (get performance)
📍 Route 2: hr_data (get role/band)
📍 Route 3: Python calculator (compute incentive)
✅ Answer: "John Smith's Q4 incentive is $45,230..."
```

---

## 🔀 Advanced: Multi-Space Routing

For complex questions that need multiple Genie spaces:

```python
class AdvancedRouter(SmartGenieRouter):
    
    def route_complex_question(self, question: str):
        """
        Determine if question needs multiple Genie spaces
        """
        
        analysis_prompt = f"""
        Analyze if this question needs data from multiple sources:
        
        Question: "{question}"
        
        Available spaces:
        {json.dumps({k: v['description'] for k, v in self.spaces.items()}, indent=2)}
        
        Respond with JSON:
        {{
            "needs_multiple_spaces": true/false,
            "required_spaces": ["space1", "space2"],
            "execution_order": ["space1", "space2"],
            "reasoning": "why multiple spaces needed"
        }}
        """
        
        # Get LLM analysis
        response = self.ws.serving_endpoints.query(
            name="databricks-meta-llama-3-1-70b-instruct",
            messages=[
                ChatMessage(
                    role=ChatMessageRole.USER,
                    content=analysis_prompt
                )
            ]
        )
        
        analysis = json.loads(response.choices[0].message.content)
        
        if analysis["needs_multiple_spaces"]:
            return self.execute_multi_space_workflow(
                question, 
                analysis["required_spaces"],
                analysis["execution_order"]
            )
        else:
            return self.ask_smart(question)
    
    def execute_multi_space_workflow(self, question, spaces, order):
        """
        Execute queries across multiple spaces in sequence
        """
        results = {}
        context = ""
        
        for space_name in order:
            space_id = self.spaces[space_name]["space_id"]
            
            # Build question with context from previous steps
            contextual_question = f"""
            Previous context: {context}
            
            New question: {question}
            """
            
            # Query this space
            response = self.ws.genie.ask_question(
                space_id=space_id,
                content=contextual_question
            )
            
            # Store result and update context
            results[space_name] = response.content
            context += f"\nData from {space_name}: {response.content}"
        
        # Synthesize final answer
        return self.synthesize_multi_space_results(results, question)
    
    def synthesize_multi_space_results(self, results, original_question):
        """
        Combine results from multiple spaces into final answer
        """
        synthesis_prompt = f"""
        Synthesize these results from multiple data sources into a cohesive answer.
        
        Original question: {original_question}
        
        Results:
        {json.dumps(results, indent=2)}
        
        Provide a comprehensive answer that integrates all the data.
        """
        
        response = self.ws.serving_endpoints.query(
            name="databricks-meta-llama-3-1-70b-instruct",
            messages=[
                ChatMessage(
                    role=ChatMessageRole.USER,
                    content=synthesis_prompt
                )
            ]
        )
        
        return {
            "answer": response.choices[0].message.content,
            "sources": list(results.keys()),
            "raw_results": results
        }
```

---

## ⚡ Alternative: Keyword-Based Routing (Fast)

If you don't want LLM overhead for routing:

```python
# streamlit/spiffit-ai-calculator/keyword_router.py

class KeywordRouter:
    """
    Fast routing based on keywords (no LLM needed)
    """
    
    def __init__(self):
        self.ws = WorkspaceClient()
        
        # Map keywords to spaces
        self.space_keywords = {
            "sales_data": {
                "space_id": "01efa5e57638161591974326e56e4807",
                "keywords": ["mrr", "tcv", "revenue", "sales", "quota", "deal", 
                            "close", "pipeline", "forecast", "attainment"]
            },
            "analytics": {
                "space_id": "01eff85bf03e1514838b4bc3fe884053",
                "keywords": ["top", "best", "rank", "compare", "trend", "average",
                            "leader", "performance", "benchmark", "growth"]
            },
            "hr_data": {
                "space_id": "your-hr-space-id",
                "keywords": ["employee", "role", "manager", "territory", "region",
                            "team", "hierarchy", "org", "reports to", "band"]
            }
        }
    
    def route_by_keywords(self, question: str):
        """
        Match question keywords to space
        Returns: (space_id, space_name, confidence)
        """
        question_lower = question.lower()
        
        scores = {}
        for space_name, space_data in self.space_keywords.items():
            # Count keyword matches
            score = sum(1 for keyword in space_data["keywords"] 
                       if keyword in question_lower)
            scores[space_name] = score
        
        # Pick space with highest score
        if max(scores.values()) > 0:
            best_space = max(scores, key=scores.get)
            confidence = scores[best_space] / len(question_lower.split())
            
            return {
                "space_id": self.space_keywords[best_space]["space_id"],
                "space_name": best_space,
                "confidence": min(confidence, 1.0),
                "method": "keyword_matching"
            }
        else:
            # Default to sales_data if no keywords match
            return {
                "space_id": self.space_keywords["sales_data"]["space_id"],
                "space_name": "sales_data",
                "confidence": 0.5,
                "method": "default"
            }
    
    def ask_with_keywords(self, question: str):
        """
        Route using keywords and get answer
        """
        routing = self.route_by_keywords(question)
        
        response = self.ws.genie.ask_question(
            space_id=routing["space_id"],
            content=question
        )
        
        return {
            "answer": response.content,
            "routed_to": routing["space_name"],
            "confidence": routing["confidence"],
            "method": routing["method"]
        }
```

### Keyword Router Usage

```python
from keyword_router import KeywordRouter

router = KeywordRouter()

# Fast routing without LLM overhead
result = router.ask_with_keywords("What's the top AE by MRR?")

st.info(f"Routed to: {result['routed_to']} (keyword matching)")
st.write(result['answer'])
```

---

## 📊 Routing Approach Comparison

| Approach | Accuracy | Speed | Cost | Complexity | Best For |
|----------|----------|-------|------|------------|----------|
| **Manual** | High (you control) | Instant | Free | Low | Simple, predictable queries |
| **Keyword-based** | Medium-High | Instant | Free | Low | Fast prototypes, limited spaces |
| **LLM Classification** | Very High | ~1-2s | Low | Medium | Production, many spaces |
| **Multi-space Analysis** | Excellent | ~3-5s | Medium | High | Complex questions, workflows |

---

## 🎯 Decision Tree: Which Router to Use?

```
Do you have < 3 Genie spaces?
  YES → Use Manual or Keyword routing
  NO → Continue

Are questions predictable/simple?
  YES → Use Keyword routing
  NO → Continue

Do you need to explain routing decisions?
  YES → Use LLM Classification
  NO → Use Keyword routing

Do questions require multiple spaces?
  YES → Use Advanced Multi-Space Router
  NO → Use LLM Classification
```

---

## 🚀 Implementation Steps

### Step 1: Start Simple (Keyword Router)
```python
# Quick implementation for hackathon
if "top" in question or "best" in question:
    space = "analytics"
elif "employee" in question or "role" in question:
    space = "hr_data"
else:
    space = "sales_data"
```

### Step 2: Add Smart Routing (If Time Allows)
```python
# Upgrade to LLM-based routing
router = SmartGenieRouter()
result = router.ask_smart(question)
```

### Step 3: Add Multi-Space (Advanced)
```python
# Handle complex questions
advanced_router = AdvancedRouter()
result = advanced_router.route_complex_question(question)
```

---

## 💡 Best Practices

### 1. Provide Good Space Descriptions
```python
# Good - specific and descriptive
"description": "Sales performance metrics including MRR, TCV, deals, quotas, and attainment rates"

# Bad - too vague
"description": "Sales data"
```

### 2. Add Fallback Logic
```python
try:
    result = router.ask_smart(question)
except Exception as e:
    # Fallback to default space
    result = default_space.ask(question)
```

### 3. Cache Routing Decisions
```python
@st.cache_data
def get_routing(question):
    return router.route_question(question)
```

### 4. Show Routing Transparency
```python
# Let users see why routing happened
st.info(f"Routing to {space_name} because: {reasoning}")
```

### 5. Allow Manual Override
```python
# Give users option to choose space
auto_route = st.checkbox("Auto-route (recommended)", value=True)

if not auto_route:
    space = st.selectbox("Choose space:", list(spaces.keys()))
```

---

## 🔍 Debugging Routing Decisions

### Add Logging
```python
import logging

logger = logging.getLogger(__name__)

def route_question(self, question):
    routing = self._classify_question(question)
    
    logger.info(f"Question: {question}")
    logger.info(f"Routed to: {routing['space_name']}")
    logger.info(f"Confidence: {routing['confidence']}")
    logger.info(f"Reasoning: {routing['reasoning']}")
    
    return routing
```

### Streamlit Debug Mode
```python
if st.checkbox("Show debug info"):
    st.json({
        "question": question,
        "routing": routing,
        "available_spaces": list(router.spaces.keys())
    })
```

---

## 📚 Related Documentation

- **Multi-Genie Workflows**: `MULTI_GENIE_WORKFLOWS.md`
- **AI Integration Guide**: `ai_integration_guide.md`
- **Genie Setup**: `GENIE_SETUP.md`

---

## 🎯 Recommendation for Hackathon

**Start with keyword-based routing:**
- ✅ Fast to implement (30 minutes)
- ✅ No LLM costs during development
- ✅ Works well for demo
- ✅ Easy to debug

**Upgrade to LLM routing if:**
- You have time
- You want to showcase advanced AI
- Questions are complex/ambiguous
- You have >3 Genie spaces

---

## 🚀 Ready-to-Use Code

### Minimal Smart Router (Copy-Paste Ready)

```python
from databricks.sdk import WorkspaceClient
import os

class SimpleRouter:
    def __init__(self):
        self.ws = WorkspaceClient()
        self.default_space = os.getenv("GENIE_SPACE_ID")
    
    def route_and_ask(self, question):
        # Simple keyword routing
        q = question.lower()
        
        if any(word in q for word in ["top", "best", "rank"]):
            space_type = "analytics"
        elif any(word in q for word in ["employee", "role", "manager"]):
            space_type = "hr"
        else:
            space_type = "sales"
        
        # Use your space (or implement multiple spaces)
        response = self.ws.genie.ask_question(
            space_id=self.default_space,
            content=question
        )
        
        return {
            "answer": response.content,
            "routed_to": space_type
        }
```

---

**Ready to implement smart routing? Pick your approach and start coding!** 🎉

