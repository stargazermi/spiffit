# 🎸 Spiffit Demo - Quick Cheat Sheet

## 30-Second Pitch
> **"We built an AI agent in 6 hours that automates sales incentive analysis by orchestrating multiple specialized AI agents across different data domains - all using Databricks Genie, Foundation Models, and Cursor AI."**

---

## The Stack (Point at each)

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND: Streamlit (Python) - Chat Interface             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SMART ROUTER: Foundation Models (Llama 3.1, Claude, GPT)  │
│  • Understands user intent                                   │
│  • Routes to right agent(s)                                  │
│  • Combines multi-agent results                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Genie Space  │ Genie Space  │ Genie Space  │ Genie Space  │
│ SALES        │ ANALYTICS    │ MARKET       │ VOICE        │
│ Performance  │ Trends       │ Intelligence │ Activations  │
└──────────────┴──────────────┴──────────────┴──────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER: Unity Catalog + SQL Warehouse                  │
│  • spg_demo.sales_performance                                │
│  • spg_demo.spiff_winners                                    │
│  • spg_demo.competitor_spiffs                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture in 3 Bullets

1. **Multi-Agent**: 4 specialized Genie spaces, each expert in one domain
2. **Smart Router**: Foundation Model orchestrates which agents to call
3. **AI Reasoning**: Time-aware, context-aware, autonomous workflows

---

## Models Quick Reference

| Component | Model | Purpose |
|-----------|-------|---------|
| **Orchestrator** | Llama 3.1 70B | Primary smart router |
| **Orchestrator** | Claude Sonnet 4 | High-quality reasoning |
| **Orchestrator** | GPT-5 Turbo | OpenAI integration |
| **Genie Spaces** | Databricks Genie | Natural language → SQL |
| **Web Search** | Custom Python | Real-time competitor intel |

---

## Demo Flow Walkthrough

### Automated Story (Demo Tab)
```
👋 Greeting: "Good afternoon! It's September 5th..."
   ↓
🤔 Smart Router: "User needs Voice Activations report"
   ↓
🎯 Route to: Voice Activations Genie
   ↓
💬 Genie: Converts request → SQL query
   ↓
📊 SQL Warehouse: Executes query
   ↓
✅ Results: Copy to Email + Download CSV
   ↓
💡 Follow-up: "Here are next month's ideas..."
   ↓
🤔 Smart Router: "Need sales trends + competitor intel"
   ↓
🔀 Multi-agent: Analytics Genie + Market Intelligence Genie
   ↓
📈 Combined Results: "Recommend X based on Y and Z"
```

---

## Key Talking Points (Memorize These!)

### **1. Multi-Agent Advantage**
*"Instead of one AI trying to be expert at everything, we have specialized agents. Like a sales team - everyone has their domain."*

### **2. Smart Router = The Brain**
*"The Foundation Model is the manager that decides: 'This question needs sales data AND competitor intel' - then calls both agents and combines results."*

### **3. Databricks Makes It Easy**
*"Genie turns English into SQL. Apps deploy from GitHub. Unity Catalog handles security. We just write the orchestration logic."*

### **4. Built with Cursor AI**
*"AI pair programming. Instead of Googling 'how to call Databricks API', Cursor writes it. 6 hours from idea to working demo."*

### **5. Production Ready**
*"This isn't a prototype. It's running on Databricks Apps - serverless, auto-scaling, Git-based deployment."*

---

## If They Ask: "Why Multiple Agents?"

**Single LLM approach**:
- ❌ Has to know ALL domains
- ❌ Gets confused with complex queries
- ❌ No specialized tuning
- ❌ Hard to debug

**Multi-agent approach**:
- ✅ Each agent is domain expert
- ✅ Router handles complexity
- ✅ Each Genie trained on specific data
- ✅ Clear logging per agent

---

## Tech Details (If Deep Dive)

### Genie Integration
```python
genie.start_conversation(space_id, content=user_question)
→ Returns: SQL query + Data results
```

### Smart Router Logic
```python
orchestrator.query("What SPIFFs for next month?")
→ Analyzes intent: [sales_trends, competitor_intel]
→ Calls: analytics_genie + market_genie
→ Combines: "Based on 20% growth in fiber + competitors offering X, recommend Y"
```

### Deployment
```bash
git push → Databricks Git Folder → App auto-restarts
```

---

## Closing Lines

### Option 1: Humor
*"When a SPIFF problem comes along... you must Spiff It! And with Databricks, you can Spiff It in 6 hours."* 🎸

### Option 2: Business Value
*"This shows how Databricks democratizes AI. Our team built a production multi-agent system in one afternoon. That's the power of integrated platform."*

### Option 3: Technical
*"This is the future of enterprise AI: specialized agents, orchestrated by Foundation Models, all running on governed data with Unity Catalog."*

---

## Anticipated Questions

**Q: "Could we add more agents?"**
A: "Yes! Each new data domain = new Genie space. Router automatically includes it."

**Q: "What about security?"**
A: "Unity Catalog handles all data access. Each Genie respects table permissions. PAT token for API auth."

**Q: "How do you swap models?"**
A: "Dropdown in UI. No code changes. All Foundation Models use same API interface."

**Q: "Cost?"**
A: "SQL Warehouse charges for query time. Foundation Model calls are per-token. Genie is included. Apps hosting is minimal."

**Q: "Can it handle real-time data?"**
A: "Yes! Web search tool does real-time scraping. Genie queries hit live SQL Warehouse data."

---

**Remember**: Smile, have fun, and when in doubt... **Spiff It!** 🎸

*v3.0.1-SPIFFIT - Ready to rock!*

