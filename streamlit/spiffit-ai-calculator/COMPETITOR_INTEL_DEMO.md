# 🌐 Competitor Intelligence Demo Guide

## Overview
The Competitor Intelligence tab showcases a **multi-tool agent** that automatically routes queries to the right data sources and synthesizes results using foundation models.

## 🏗️ Architecture

```
User Query
    ↓
GPT-5.1 Router (Smart Routing Decision)
    ↓
┌──────────┴──────────────┐
│                          │
▼                          ▼
Genie Spaces          Web Search Tool
(Internal Data)       (Competitor Data)
    ↓                      ↓
└──────────┬──────────────┘
           ↓
    GPT-5.1 Synthesizer
           ↓
    Final Answer
```

## 🎯 Demo Flow for Hackathon

### Step 1: Show Simple Query (Single Tool)
**Click:** "🔍 Search AT&T Programs"

**What happens:**
- Router decides: `web_search` only
- Returns competitor data
- **Expand "🧠 AI Reasoning"** to show routing decision

**Key talking point:** "Notice how the agent automatically detected this is a competitor query and routed to web search."

---

### Step 2: Show Internal Query (Single Tool)
**Type:** "Who are our top performers this month?"

**What happens:**
- Router decides: `genie_analytics`
- Queries internal Genie space
- Returns leaderboard data

**Key talking point:** "Now it recognized this as internal data and used our Genie space instead."

---

### Step 3: Show Multi-Tool Query (The Magic!)
**Click:** "⚔️ Our SPIFFs vs Competitors"

**What happens:**
1. Router decides: `genie_analytics` + `web_search`
2. Queries BOTH sources
3. GPT-5.1 synthesizes results
4. Provides comparative analysis

**Key talking point:** "This is where it gets powerful - the agent queried BOTH internal and external sources, then used GPT-5.1 to synthesize a comprehensive comparison."

---

### Step 4: Show AI Recommendations
**Click:** "💡 Get Recommendations"

**What happens:**
- Multi-source query
- Analyzes patterns
- Provides actionable SPIFF recommendations

**Key talking point:** "The agent can make strategic recommendations by analyzing both what we're doing AND what competitors are offering."

---

## 🔑 Key Features to Highlight

### 1. **Automatic Routing**
- No manual tool selection
- LLM decides which tools to use
- Handles single or multiple sources

### 2. **Transparent AI**
- Click "🧠 AI Reasoning & Tools" to see:
  - Routing decision explanation
  - Which tools were called
  - Raw results from each tool

### 3. **Real Foundation Models**
- Uses hackathon-provided serving endpoints:
  - GPT-5.1 for orchestration
  - Gemini 2.5 Flash available
  - Claude Sonnet 4.5 available

### 4. **Mock Competitor Data** (for demo)
- Pre-loaded with AT&T, Verizon, T-Mobile, Comcast
- Easy to swap with real search API (SerpAPI, Bing)
- Shows the pattern without API costs

---

## 🎤 Talking Points for Judges

1. **"This demonstrates agentic AI in action"**
   - Agent makes decisions
   - Uses tools autonomously
   - Synthesizes results intelligently

2. **"It's extensible beyond SPIFFs"**
   - Pattern works for any multi-source query
   - Add more tools easily (pricing API, CRM data, etc.)
   - Foundation models handle reasoning

3. **"Built on Databricks native stack"**
   - Genie for structured data
   - Foundation Model API for LLMs
   - No external dependencies

4. **"Production-ready architecture"**
   - Modular design (`multi_tool_agent.py`, `web_search_tool.py`)
   - Easy to add real search APIs
   - Monitoring and transparency built-in

---

## 🧪 Test Queries

### Internal Only:
- "Show me our November SPIFF winners"
- "Who exceeded 125% of quota?"

### External Only:
- "What is T-Mobile offering?"
- "Compare AT&T and Verizon programs"

### Multi-Tool (Best Demo):
- "How competitive are our SPIFFs?"
- "Should we increase our large deal bonus based on competitors?"
- "What gaps exist in our SPIFF strategy?"

---

## 🚀 Quick Setup Reminders

1. **Environment variables** are configured in `app.yaml`
2. **Genie spaces** already set up (sales, analytics, market)
3. **GPT-5.1** endpoint from hackathon serving endpoints
4. **Mock data** in `web_search_tool.py` (lines 24-68)

---

## 💡 Future Enhancements (mention if asked)

- Replace mock data with real search API
- Add more tools (pricing API, historical trends, etc.)
- Implement caching for repeated queries
- Add memory/context across conversations
- Schedule autonomous reports (morning briefing)

**Good luck with your demo! 🎉**

