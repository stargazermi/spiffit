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

```
spiffit/
├── README.md                          # This file
├── test-data/                         # Source Excel files
│   ├── AE Ethernet Incentive Data.xlsx
│   └── Voice_Incentive_data.xlsx
│
├── docs/                              # 📚 Documentation & guides
│   ├── CREATE_GENIE_SPACES_GUIDE.md  # How to create Genie spaces
│   ├── ai_integration_guide.md       # AI/LLM integration
│   ├── GENIE_SETUP.md                # Genie configuration
│   ├── AUTONOMOUS_SPIFF_AGENT.md     # Agent architecture
│   ├── SMART_GENIE_ROUTING.md        # Routing strategies
│   └── MULTI_GENIE_WORKFLOWS.md      # Workflow patterns
│
├── sql/                               # 🗄️ Mock data SQL scripts
│   ├── 01_create_spg_demo_schema.sql
│   ├── 02_create_sales_performance_table.sql
│   ├── 03_create_spiff_winners_table.sql
│   ├── 04_create_competitor_spiffs_table.sql
│   └── README.md                     # SQL setup instructions
│
├── streamlit/                         # 🖥️ Streamlit applications
│   ├── README.md                     # Apps overview
│   ├── spiffit-hello/                # Hello world test app
│   └── spiffit-ai-calculator/        # AI calculator app
│
└── cursor/                            # All hackathon work (ORGANIZED!)
    ├── README.md                      # Project overview
    ├── QUICK_START.md                 # ⭐ Start here!
    ├── EXECUTIVE_SUMMARY.md           # Business case & ROI
    ├── HACKATHON_DAY_PLAN.md          # Hour-by-hour timeline
    │
    ├── data-exploration/              # Excel analysis results
    │   ├── analyze_excel_files.py
    │   └── analysis_results.json      # Detailed findings
    │
    ├── automation-ideas/              # Use cases & opportunities
    │   ├── use-cases.md               # 8 detailed ideas
    │   ├── identified_opportunities.json
    │   └── implementation-plans/
    │       └── use-case-1-ai-calculator.md
    │
    └── prototypes/                    # Ready-to-use code
        ├── 01_load_data_to_delta.py
        └── 02_incentive_calculator.py
```

---

## ⚡ 5-Minute Setup

```bash
# 1. Open cursor/QUICK_START.md and read it (5 min)

# 2. Pick your use case (recommend #1)

# 3. In Databricks:
#    - Upload test-data/*.xlsx files
#    - Run cursor/prototypes/01_load_data_to_delta.py
#    - Run cursor/prototypes/02_incentive_calculator.py

# 4. Build your AI layer and UI

# 5. Practice your demo using cursor/HACKATHON_DAY_PLAN.md
```
=======
### Test Data Available
- **AE Ethernet Incentive Data**: 3 sheets, 650 rows
- **Voice Incentive Data**: 2 sheets, 1,496 rows
- **Total**: 2,146 rows of incentive/sales data