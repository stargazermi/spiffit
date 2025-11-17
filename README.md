# Spiffit - AI Hackathon Project

## 🎯 Mission
Explore AI automation opportunities for Excel-based workflows using Databricks

## 📊 Project Status
Active exploration and prototyping for hackathon

---

## 📁 Project Structure

```
spiffit/
├── README.md                          # This file
├── test-data/                         # Sample Excel files
│   ├── AE Ethernet Incentive Data.xlsx
│   └── Voice_Incentive_data.xlsx
│
├── streamlit/                         # Streamlit app experiments
│   ├── app.py                         # Hello world test app
│   ├── app.yaml                       # Databricks config (port 8000)
│   └── requirements.txt               # Dependencies
│
└── cursor/                            # Exploration & analysis work
    ├── data-exploration/              # Data analysis
    ├── automation-ideas/              # Use case brainstorming
    └── prototypes/                    # Code experiments
```

---

## 🛠️ Available Tech Stack

### Dev Tools
- Delta Lake, Databricks Apps, Notebooks, AI BI Dashboard
- Python, GitHub, Power BI

### Agent Tools
- MCP, Vector Search, Agent Bricks, Genie
- Mosaic AI, ML Flow, LangChain, LangGraph

### LLMs
- GPT-OSS, Llama, Gemma, GTE, BGE
- Claude Sonnet, Claude Opus 4.1, GPT-5, Gemini 2.5

---

## 📊 Data Overview

### Test Data Available
- **AE Ethernet Incentive Data**: 3 sheets, 650 rows
- **Voice Incentive Data**: 2 sheets, 1,496 rows
- **Total**: 2,146 rows of incentive/sales data

### Initial Analysis
- Multiple numeric calculations per record
- Complex formulas across sheets
- Some missing data fields
- Manual processing currently taking significant time

---

## 🚀 Getting Started

### Streamlit Test App
A simple hello world app to test Databricks Apps deployment:

```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py --server.port 8000
```

See `streamlit/README.md` for Databricks deployment instructions.

### Exploration Work
The `cursor/` folder contains:
- Data analysis scripts and results
- Use case ideas and brainstorming
- Prototype code experiments
- Implementation planning notes

---

## 🎯 Hackathon Goals

- Explore automation opportunities in Excel workflows
- Experiment with Databricks AI capabilities
- Build proof-of-concept demonstrations
- Identify high-impact use cases

---

## 📞 Repository Info

**GitHub:** https://github.com/stargazermi/spiffit  
**Purpose:** Hackathon AI exploration and prototyping  
**Team:** Internal hackathon team

---

Good luck, team! 🚀
