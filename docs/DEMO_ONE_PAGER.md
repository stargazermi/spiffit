# 🎸 Spiffit - Demo One-Pager

## What is it?
AI-powered sales incentive intelligence platform built on Databricks in 6 hours using Cursor AI.

## Tech Stack
- **Development**: Cursor AI (AI pair programming)
- **Deployment**: Databricks Apps (serverless, Git-based)
- **Data**: Unity Catalog + SQL Warehouse
- **AI**: Databricks Genie + Foundation Models (Llama, GPT, Claude)
- **Code**: Python, Streamlit, GitHub

## Architecture

### Multi-Agent System
4 specialized agents, each with its own Genie space:
1. **Sales Performance** - Historical data & winners
2. **Analytics** - Trends & forecasting
3. **Market Intelligence** - Competitor intel
4. **Voice Activations** - VOIP/MRR calculations

### Smart Router + AI Reasoning
- **Orchestrator Models**: Llama 3.1 70B, Claude Sonnet, GPT-5, DBRX
- **Routes** user questions to the right agent(s)
- **AI Reasoning**: Time-aware, context-aware, workflow-aware
- **Chains** multiple agents for complex queries

## Models in Use

### Foundation Models (Smart Router)
- Meta Llama 3.1 70B / 3.3 70B
- Claude Sonnet 3.7 / 4.0
- GPT-5 Turbo / 5.1
- DBRX Instruct
- Gemini 2.5 Pro/Flash

### Genie Spaces (SQL Generation)
- Natural language → SQL
- Each connected to specific tables
- Powered by SQL Warehouse

## Key Innovations

1. **Multi-Genie Workflow**: One question, multiple data sources
2. **Autonomous Agent**: Proactively runs month-end reports
3. **6-hour build time**: Cursor AI + Databricks Apps = rapid development

## Demo Highlights

**Automated Story**: 
- "Good afternoon! It's September 5th..."
- Runs Voice Activations calculation
- Shows Copy to Email + Download CSV
- Suggests next month's SPIFFs

**Interactive**: Sidebar examples for Sales, Competitors, Analytics

## Business Value
- ⚡ **Speed**: Hours to build, not weeks
- 📈 **Accuracy**: Multi-agent specialization
- 🔄 **Scalability**: Serverless, auto-scaling
- 🛡️ **Governance**: Unity Catalog built-in

---

**"When SPIFFs get tough, you must Spiff It!"** 🎸

*v3.0.1-SPIFFIT*

