# 🎸 Spiffit - When SPIFFs Get Tough, You Must Spiff It!

**AI-Powered Sales Incentive Intelligence Platform**  
*Powered by multi-agent AI • Databricks Genie • 100% pure hackathon energy!*

[![Version](https://img.shields.io/badge/version-v3.9.6-blue)]()
[![Databricks](https://img.shields.io/badge/Databricks-Apps-red)]()
[![AI](https://img.shields.io/badge/AI-Multi--Agent-green)]()

---

## 🎯 What is Spiffit?

**Spiffit** transforms complex sales incentive data analysis from hours of Excel work into seconds of natural language queries. Built for the Databricks AI Hackathon, it demonstrates the power of multi-agent AI systems for real-world business intelligence.

**The Challenge:**
- 📊 2,146+ rows of SPIFF/incentive data across multiple Excel files
- ⏰ Hours spent manually calculating payouts, analyzing performance, tracking competitors
- 📧 Tedious email reporting for compensation teams

**The Solution:**
- 💬 Natural language interface: "Who won last month's Voice Activations SPIFF?"
- 🤖 Multi-agent AI: Automatically routes queries to specialized data sources
- ⚡ Smart caching: 3-second responses after first query
- 📊 Auto-generated pivot tables, charts, and email-ready reports

---

## ✨ Key Features

### 🎤 **Natural Language Intelligence**
Ask questions in plain English:
- "Calculate Voice Activations incentives for August"
- "Who are our top performers this quarter?"
- "Compare our SPIFFs to AT&T's current promotions"
- "Should we increase our incentive budget?"

### 🤖 **Multi-Agent Architecture**
Smart routing to specialized agents:
- **Voice Activations Genie** - VOIP incentive calculations
- **Competitor Intelligence Tool** - Real-time market data
- **Smart Router** - Automatically picks the best agent(s)
- **Result Synthesizer** - Combines insights from multiple sources

### ⚡ **Performance Optimized**
- **14x faster** on repeated queries (35s → 3s with caching)
- Intelligent query result storage
- Realistic delays for demo polish (feels "live" not "pre-recorded")

### 📊 **Beautiful Data Visualization**
- Interactive Plotly charts
- Pivot tables grouped by owner/manager
- One-click CSV downloads
- Email-ready markdown formatting

### 🎯 **Demo-Ready**
- Automated demo story (full walkthrough in 90 seconds)
- Clean Chat interface for presentations
- Tech tab for debugging and exploration
- Foundation model switching (Llama, Claude, GPT)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web App                        │
│                  (Databricks Apps Platform)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
            ┌────────▼────────┐
            │  Multi-Agent     │
            │  Orchestrator    │
            │  (Smart Router)  │
            └─┬──────┬────┬───┘
              │      │    │
    ┌─────────▼──┐ ┌▼────▼──────────┐
    │  Genie     │ │ Competitor     │
    │  Space API │ │ Search Tool    │
    │            │ │ (Web Scraping) │
    └─────┬──────┘ └────────────────┘
          │
    ┌─────▼──────────────────────────┐
    │  Databricks SQL Warehouse      │
    │  - voice_opps (426 rows)       │
    │  - voice_orders (1,070 rows)   │
    └────────────────────────────────┘
```

### Tech Stack
- **Frontend:** Streamlit 1.28+
- **AI Platform:** Databricks (Genie, Foundation Models)
- **LLMs:** Llama 3.1 70B, Claude Sonnet, GPT-5 (Foundation Model API)
- **Data:** Unity Catalog, SQL Warehouse, Delta Lake
- **Tools:** Python 3.10+, Pandas, Plotly, BeautifulSoup
- **Deployment:** Databricks Apps (Git-integrated)

---

## 📁 Project Structure

```
spiffit/
├── README.md                                   # 👈 You are here
├── test-data/                                  # Original Excel files
│   ├── AE_Ethernet_Incentive_Data.xlsx
│   └── Voice_Incentive_data.xlsx
│
├── docs/                                       # 📚 Documentation
│   ├── DEMO_ONE_PAGER.md                      # Quick demo guide
│   ├── PERFORMANCE_OPTIMIZATION_v3.7.0.md     # Caching details
│   ├── UX_IMPROVEMENTS_v3.6.0.md              # UI enhancements
│   ├── GENIE_API_VS_UI_PERFORMANCE.md         # API performance analysis
│   ├── DATA_VISUALIZATION_UPDATE.md           # Chart implementation
│   └── SPIFFIT_SONG_AI_PROMPT.md              # 🎸 Theme song!
│
├── sql/                                        # 🗄️ Database setup
│   ├── 01_create_spg_demo_schema.sql
│   ├── 02_create_voice_opportunities.sql
│   ├── 03_create_voice_orders.sql
│   └── README.md
│
└── streamlit/spiffit-ai-calculator/            # 🚀 Main Application
    ├── app.py                                  # Streamlit UI (v3.7.6)
    ├── app.yaml                                # Databricks App config
    ├── requirements.txt                        # Python dependencies
    │
    ├── ai_helper.py                            # Genie API integration
    ├── multi_tool_agent.py                     # Multi-agent orchestrator
    ├── web_search_tool.py                      # Competitor intelligence
    ├── spiff_agent.py                          # SPIFF calculation agent
    ├── query_parser.py                         # Query parsing utilities
    │
    ├── deploy-app.ps1                          # Deployment script
    ├── check-app-logs.ps1                      # Log monitoring
    └── env.example                             # Environment template
```

---

## 🚀 Quick Start

### Prerequisites
- Databricks workspace (AWS, Azure, or GCP)
- SQL Warehouse (any size)
- Databricks Apps enabled
- Git integration configured

### 1️⃣ Clone & Setup

```bash
# Clone the repository
git clone https://github.com/your-org/spiffit.git
cd spiffit

# Copy environment template
cd streamlit/spiffit-ai-calculator
cp env.example .env

# Edit .env with your credentials
# DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
# DATABRICKS_TOKEN=your-pat-token
# GENIE_SPACE_ID=your-genie-space-id
# SQL_WAREHOUSE_ID=your-warehouse-id
```

### 2️⃣ Create Database & Genie Space

```bash
# Run SQL scripts in Databricks SQL Editor
# 1. sql/01_create_spg_demo_schema.sql
# 2. sql/02_create_voice_opportunities.sql
# 3. sql/03_create_voice_orders.sql

# Create Genie Space in Databricks:
# - Go to "AI/BI Dashboards" → "Genie Spaces" → "Create"
# - Name: "Hackathon- SPIFF Analyzer"
# - Connect to: hackathon.voice_opps, hackathon.voice_orders
# - Add instructions (see docs/GENIE_SETUP.md)
# - Copy the Space ID
```

### 3️⃣ Deploy to Databricks

```bash
# Push to GitHub (if not already)
git add .
git commit -m "Initial Spiffit deployment"
git push

# Deploy using Databricks CLI
databricks apps deploy spiffit-mocking-bird --profile your-profile

# Or use PowerShell script
./deploy-app.ps1
```

### 4️⃣ Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (use .env file)
export DATABRICKS_HOST="https://..."
export DATABRICKS_TOKEN="dapi..."
export GENIE_SPACE_ID="01f0c4ae..."
export SQL_WAREHOUSE_ID="0962fa4c..."

# Run Streamlit
streamlit run app.py --server.port 8000
```

---

## 🎸 Demo Guide

### Automated Demo Story
1. Click **"Demo"** tab
2. Click **"🎸 Spiff It Demo!"** in sidebar
3. Watch the magic:
   - ✅ Greeting & context
   - ✅ Voice Activations calculation (~30s first time, 3s cached)
   - ✅ Pivot table by Opportunity Owner
   - ✅ Interactive chart
   - ✅ "Copy for Email" + "Download CSV" buttons
   - ✅ Competitor intelligence analysis
   - ✅ Next month's recommendations

### Manual Queries (Tech Tab)
Try these example prompts:
- "Calculate incentives for Morgan Ellis"
- "Who earned over $5000 in Voice Activations?"
- "What SPIFFs is AT&T offering for fiber?"
- "Compare our top performers to industry benchmarks"

---

## 📊 Performance Metrics

### Query Performance
```
Voice Activations Detail (379 rows):
├─ First run:  35s (Genie API + SQL execution)
├─ Cached:      3s (artificial delay for demo feel)
└─ Speedup:    14x faster

Voice Pivot Summary (8 rows):
├─ First run:  20s (Genie API + SQL execution)
├─ Cached:      2s (artificial delay)
└─ Speedup:    10x faster

Total Demo Time:
├─ First run:  ~70s (authentic AI processing)
├─ Subsequent: ~20s (fast but realistic)
└─ Improvement: 3.5x faster replay
```

### Why the Delay?
Genie API uses polling (every 5 seconds), adding ~15s overhead vs. Databricks UI. Caching eliminates this for subsequent queries while maintaining a realistic user experience.

---

## 🔧 Configuration

### Environment Variables

**Required:**
```bash
DATABRICKS_HOST=https://dbc-xxxxx.cloud.databricks.com
DATABRICKS_TOKEN=dapi...                        # PAT token
GENIE_SPACE_ID=01f0c4ae...                     # Voice Activations Genie
SQL_WAREHOUSE_ID=0962fa4c...                   # Any warehouse
```

**Optional:**
```bash
GENIE_SALES_SPACE_ID=...                       # Additional Genies
GENIE_ANALYTICS_SPACE_ID=...
GENIE_MARKET_SPACE_ID=...
DATABRICKS_PROFILE=dlk-hackathon               # CLI profile
```

### Databricks App Configuration (app.yaml)

```yaml
command: ["streamlit", "run", "app.py", "--server.port", "8000"]

env:
  - name: DATABRICKS_HOST
    value: "https://..."
  - name: DATABRICKS_TOKEN
    value: "dapi..."
  - name: GENIE_SPACE_ID
    value: "01f0c4ae..."
  - name: SQL_WAREHOUSE_ID
    value: "0962fa4c..."
```

---

## 🎤 Talking Points for Demo

**Opening:**
> "When a problem comes along with manual Excel calculations... you must Spiff It! Let me show you how AI transforms hours of work into seconds of conversation."

**Multi-Agent Architecture:**
> "Behind the scenes, we have a smart router that analyzes each query and dispatches it to specialized agents - one for Voice Activations data, another for competitor intelligence. It's like having an expert team that collaborates automatically."

**Performance:**
> "The first time you run a query, it takes about 30 seconds as Genie parses the business logic and generates SQL. But watch what happens when I run it again... [3 seconds] That's our intelligent caching at work."

**Business Value:**
> "This isn't just about speed. It's about democratizing data access. Now anyone on the sales team can ask 'Who won last month?' instead of waiting for a data analyst to run reports."

---

## 📚 Documentation

- **[DEMO_ONE_PAGER.md](docs/DEMO_ONE_PAGER.md)** - Quick demo script
- **[PERFORMANCE_OPTIMIZATION_v3.7.0.md](docs/PERFORMANCE_OPTIMIZATION_v3.7.0.md)** - Caching implementation
- **[GENIE_API_VS_UI_PERFORMANCE.md](docs/GENIE_API_VS_UI_PERFORMANCE.md)** - API deep dive
- **[UX_IMPROVEMENTS_v3.6.0.md](docs/UX_IMPROVEMENTS_v3.6.0.md)** - UI enhancements
- **[SPIFFIT_SONG_AI_PROMPT.md](docs/SPIFFIT_SONG_AI_PROMPT.md)** - Theme song (yes, really!)

---

## 🐛 Troubleshooting

### "No tools were able to answer this question"
- **Fix:** Check that `GENIE_SPACE_ID` is set and valid
- **Fix:** Verify Genie space permissions (user needs "Can Manage")
- **Fix:** Ensure SQL warehouse is running

### "Missing optional dependency 'tabulate'"
- **Fix:** Add `tabulate>=0.9.0` to `requirements.txt` and redeploy

### "name 'time' is not defined"
- **Fix:** Add `import time` to top of `app.py`

### Genie queries are slow (30+ seconds)
- **Expected:** First query is slow (Genie API polling overhead)
- **Fix:** Cache works on subsequent queries (see v3.7.0 changes)
- **Workaround:** Keep SQL warehouse running (reduces cold start)

### Download CSV clears the screen
- **Fixed in v3.7.4:** Switched from modal to popover (no rerun)

---

## 🗺️ Roadmap / Future Enhancements

- [ ] **Multi-workspace support** - Query Genies across workspaces
- [ ] **Voice interface** - Speak your queries (voice-to-text)
- [ ] **Email integration** - Auto-send monthly reports
- [ ] **Slack bot** - Answer SPIFF questions in Slack
- [ ] **Historical tracking** - Trend analysis over time
- [ ] **Predictive analytics** - Forecast next quarter's performance
- [ ] **Mobile app** - iOS/Android native apps
- [ ] **PDF exports** - Generate executive summaries

---

## 🎸 The Spiffit Song

**"When a problem comes along... you must Spiff It!"**

Based on Devo's "Whip It", the Spiffit theme song embodies the spirit of tackling sales incentive challenges with AI-powered automation. 

*Full lyrics and AI performance prompt available in [docs/SPIFFIT_SONG_AI_PROMPT.md](docs/SPIFFIT_SONG_AI_PROMPT.md)*

---

## 📜 Version History

- **v3.7.6** (Current) - Fixed generic query routing
- **v3.7.5** - Added tabulate dependency
- **v3.7.4** - Fixed download CSV with popover
- **v3.7.3** - Real modal dialog for email copy
- **v3.7.2** - Improved truncation logic
- **v3.7.1** - Hotfix: Added missing time import
- **v3.7.0** - Performance caching (14x faster!)
- **v3.6.0** - Enhanced email copy + truncated competitor intel
- **v3.0.0** - Initial multi-agent architecture

---

## 🤝 Contributing

This is a hackathon project! Contributions, suggestions, and forks are welcome.

### Development Setup
```bash
git clone https://github.com/your-org/spiffit.git
cd spiffit/streamlit/spiffit-ai-calculator
pip install -r requirements.txt
cp env.example .env
# Edit .env with your credentials
streamlit run app.py
```

### Coding Standards
- Python 3.10+
- Black formatting (line length 100)
- Type hints for function signatures
- Docstrings for public functions
- Emoji in commit messages encouraged 🎸

---

## 📄 License

This project is part of a Databricks AI Hackathon.  
All rights reserved.

---

## 🙏 Acknowledgments

- **Databricks** - For the amazing AI platform and Genie API
- **The Hackathon Team** - For data, ideas, and endless energy
- **Devo** - For inspiring our theme song
- **You** - For checking out this project!

---

## 📞 Contact

Questions? Feedback? Want to Spiff It together?

- **Project Lead:** [Your Name]
- **Email:** [your.email@company.com]
- **Workspace:** dlk-hackathon (Databricks)

---

<div align="center">

**🎸 When SPIFFs get tough, you must Spiff It! 🎸**

*Built with ❤️ and AI at the Databricks Hackathon*

[![Databricks](https://img.shields.io/badge/Powered%20by-Databricks-red)](https://databricks.com)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

</div>
