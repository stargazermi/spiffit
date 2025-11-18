# 🎯 Multi-Agent Architecture with Single Genie Backend

## Overview

**Architecture Design:** Multi-Agent System (4 specialized agents)  
**Current Implementation:** All agents backed by one Genie space  
**Genie Space:** "Hackathon- SPIFF Analyzer" (`0110c4ae99271d64835d414b8d43ddfb`)  
**Version:** v3.1.0-SPIFFIT

---

## Why This Approach?

### ✅ **Maintains Demo Value Proposition**
- Can demonstrate **multi-agent architecture** concepts
- Shows **smart routing** between specialized agents
- Proves **Foundation Model orchestration**
- Architecture supports **future expansion**

### ✅ **Simplifies Current Implementation**
- One Genie space to configure
- One space to permission
- Single SQL Warehouse connection
- Easier troubleshooting

### ✅ **Best of Both Worlds**
- **Architecture:** Designed for multiple agents
- **Implementation:** Uses one backend for now
- **Demo Story:** Multi-agent intelligence
- **Reality:** One Genie space doing the heavy lifting

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  USER QUERY: "What should we offer next month?"             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SMART ROUTER (Foundation Model - GPT-5.1 / Claude / Llama) │
│  Analyzes intent, determines which agents to call            │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                     ↓                      ↓
┌───────────────┐     ┌───────────────┐     ┌──────────────┐
│ Sales Agent   │     │ Analytics     │     │ Web Search   │
│               │     │ Agent         │     │ Tool         │
└───────────────┘     └───────────────┘     └──────────────┘
        ↓                     ↓                      ↓
        └─────────────────────┴──────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │  SAME BACKEND GENIE SPACE                 │
        │  "Hackathon- SPIFF Analyzer"              │
        │  ID: 0110c4ae99271d64835d414b8d43ddfb     │
        └───────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SQL WAREHOUSE: 0962fa4cf0922125                            │
│  Data: voice_opps, voice_orders                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SYNTHESIZER (Foundation Model)                             │
│  Combines results from multiple agents into coherent answer │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FINAL ANSWER TO USER                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## The 4 Agents

### 1. **Sales Performance Agent**
- **Environment Variable:** `GENIE_SALES_SPACE_ID`
- **Current Value:** `0110c4ae99271d64835d414b8d43ddfb`
- **Purpose:** Handle sales metrics, AE performance, quotas, deals
- **Example Queries:**
  - "Show me sales performance for Q3"
  - "Which AEs hit their quota?"
  - "What's our pipeline for next quarter?"

### 2. **Analytics & Winners Agent**
- **Environment Variable:** `GENIE_ANALYTICS_SPACE_ID`
- **Current Value:** `0110c4ae99271d64835d414b8d43ddfb`
- **Purpose:** Calculate SPIFF winners, leaderboards, historical payouts
- **Example Queries:**
  - "Who are the top performers this month?"
  - "Show me the SPIFF leaderboard"
  - "List recent incentive winners"

### 3. **Market Intelligence Agent**
- **Environment Variable:** `GENIE_MARKET_SPACE_ID`
- **Current Value:** `0110c4ae99271d64835d414b8d43ddfb`
- **Purpose:** Analyze trends, historical data, internal benchmarks
- **Example Queries:**
  - "What were our sales trends last quarter?"
  - "Compare this month to last month"
  - "Show historical SPIFF performance"

### 4. **Voice Activations Agent**
- **Environment Variable:** `GENIE_VOICE_ACTIVATIONS_SPACE_ID`
- **Current Value:** `0110c4ae99271d64835d414b8d43ddfb`
- **Purpose:** Calculate VOIP incentives, MRR payouts, opportunity owner performance
- **Example Queries:**
  - "Calculate Voice Activations incentives"
  - "Show VOIP MRR by opportunity owner"
  - "Who qualifies for Voice Activations payout?"

---

## Smart Routing in Action

### Example 1: Simple Internal Query
```
User: "Who are our top performers?"

Smart Router Decision:
{
  "tools": ["genie_sales", "genie_analytics"],
  "reasoning": "Need both sales data and leaderboard"
}

Result: Both agents hit same Genie space, but query is semantically routed
```

### Example 2: Multi-Tool Query
```
User: "What should we offer next month?"

Smart Router Decision:
{
  "tools": ["genie_sales", "genie_analytics", "web_search"],
  "reasoning": "Strategic decision needs internal trends + competitor intel"
}

Result: 
- Sales + Analytics agents hit Genie space for internal data
- Web search tool scrapes competitor sites
- Foundation Model synthesizes all results
```

### Example 3: Voice Activations
```
User: "Calculate Voice Activations incentives"

Smart Router Decision:
{
  "tools": ["genie_voice_activations"],
  "reasoning": "Voice Activations incentive calculations"
}

Result: Routes to Voice Activations agent (same Genie backend)
```

---

## Configuration

### `app.yaml` - All 4 agents configured:
```yaml
# Sales Performance Agent
- name: GENIE_SALES_SPACE_ID
  value: "0110c4ae99271d64835d414b8d43ddfb"

# Analytics & Winners Agent
- name: GENIE_ANALYTICS_SPACE_ID
  value: "0110c4ae99271d64835d414b8d43ddfb"

# Market Intelligence Agent
- name: GENIE_MARKET_SPACE_ID
  value: "0110c4ae99271d64835d414b8d43ddfb"

# Voice Activations Agent
- name: GENIE_VOICE_ACTIVATIONS_SPACE_ID
  value: "0110c4ae99271d64835d414b8d43ddfb"
```

### `multi_tool_agent.py` - Supports 4 agents:
```python
def __init__(
    self,
    genie_sales_id: str = None,
    genie_analytics_id: str = None,
    genie_market_id: str = None,
    genie_voice_activations_id: str = None,
    orchestrator_model: str = "databricks-gpt-5-1"
):
    # Initialize 4 separate agent objects
    self.genie_sales = IncentiveAI(genie_space_id=genie_sales_id)
    self.genie_analytics = IncentiveAI(genie_space_id=genie_analytics_id)
    self.genie_market = IncentiveAI(genie_space_id=genie_market_id)
    self.genie_voice_activations = IncentiveAI(genie_space_id=genie_voice_activations_id)
```

---

## Future Expansion Path

When you're ready to add more Genie spaces, simply:

### Step 1: Create New Genie Space
- Create specialized Genie space in Databricks
- Connect to specific tables/data
- Get the new space ID

### Step 2: Update `app.yaml`
```yaml
- name: GENIE_ANALYTICS_SPACE_ID
  value: "[NEW_ANALYTICS_SPACE_ID]"  # ← Update with new space
```

### Step 3: Redeploy
- Push to GitHub
- Databricks Apps auto-deploys
- Smart router automatically uses new agent

### Step 4: Done!
- No code changes needed
- Router already configured to handle all agents
- Each agent now has specialized data access

---

## Demo Talking Points

### **For Technical Audience:**
> "We've implemented a multi-agent architecture where each agent is specialized for different query types. Currently, all agents point to the same Genie space for simplicity, but the architecture is designed to support separate Genie spaces as we scale. The smart router uses a Foundation Model to intelligently decide which agent(s) to call based on the user's question."

### **For Business Audience:**
> "Think of it like having a team of specialists. When you ask a question, our AI manager (the smart router) decides which specialists to consult. Right now they all access the same database, but as we grow, each specialist can have their own dedicated data sources without changing the user experience."

### **For Stakeholders:**
> "The system is designed for growth. We can easily add more specialized agents by creating new Genie spaces and updating a single configuration file. No code changes required."

---

## Benefits of This Approach

### ✅ **Demo Value**
- Shows off multi-agent architecture
- Demonstrates intelligent routing
- Proves scalability story

### ✅ **Practical Implementation**
- One Genie space = easier setup
- Faster queries (no waiting for multiple calls)
- Simpler debugging

### ✅ **Future-Proof**
- Add new agents anytime
- No code refactoring needed
- Architecture supports expansion

### ✅ **AI Reasoning**
- Smart router demonstrates Foundation Model capabilities
- Shows intent classification
- Proves synthesis of multiple sources

---

## Testing Checklist

- [ ] **Sales queries** route to Sales Agent → hits Genie
- [ ] **Analytics queries** route to Analytics Agent → hits Genie
- [ ] **Market queries** route to Market Agent → hits Genie
- [ ] **Voice Activations** routes to Voice Agent → hits Genie
- [ ] **Competitor queries** route to Web Search → external API
- [ ] **Multi-tool queries** call multiple agents → synthesize results
- [ ] **Troubleshooting tab** shows all 4 agents as "Connected"
- [ ] **Environment variables** display all 4 space IDs (same value)

---

## Key Points for Demo

1. **Architecture is Multi-Agent** ✅
2. **Smart Router is Real** ✅
3. **Foundation Models Orchestrate** ✅
4. **Backend happens to be one Genie** ✅ (but architecture supports multiple)
5. **Expansion is Easy** ✅ (just update config)

---

**Status:** ✅ Ready for Demo  
**Version:** v3.1.0-SPIFFIT  
**Architecture:** Multi-Agent with Single Backend  

🎸 **When a problem comes along... you must Spiff It!** 🎸

