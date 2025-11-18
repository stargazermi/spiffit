# Spiffit AI Calculator

## 🎯 Purpose
Natural language interface for incentive calculations and competitor intelligence using Databricks AI.

## ✨ Features

### 💬 Chat Tab
- Natural language queries for internal incentive data
- Connected to Genie space for sales performance
- Intent extraction and query parsing

### 🌐 Competitor Intelligence Tab (NEW v1.3.0!)
- **Multi-tool agent** with automatic smart routing
- **Source selection**:
  - Internal queries → Genie spaces (sales, analytics, market)
  - Competitor queries → Web search tool
  - Complex queries → Multiple sources + AI synthesis
- **GPT-5.1** orchestration for reasoning and recommendations
- **Transparent AI** - see which tools were used and routing decisions

### 🔧 Troubleshooting Tab
- Environment variable inspection
- Connection status monitoring
- Deployment version/timestamp tracking

## 📁 Files
- `app.py` - Main Streamlit application with 3 tabs
- `ai_helper.py` - AI/LLM integration (Genie & Foundation Models)
- `query_parser.py` - Natural language query parsing
- `multi_tool_agent.py` - **NEW:** Smart routing orchestrator
- `web_search_tool.py` - **NEW:** Competitor intelligence search
- `app.yaml` - Databricks App configuration
- `requirements.txt` - Python dependencies
- `CHANGELOG.md` - Version history
- `README.md` - This file

## 🚀 Quick Start

### ⭐ RECOMMENDED: Deploy to Databricks Apps

```bash
# 1. Push to Git
git add .
git commit -m "Add AI calculator app"
git push origin main

# 2. In Databricks (https://dbc-4a93b454-f17b.cloud.databricks.com):
#    - Go to Apps
#    - Create App
#    - Source: github.com/stargazermi/spiffit
#    - Path: streamlit/spiffit-ai-calculator/
#    - Deploy! (takes ~2-3 minutes)
```

**Why Databricks Apps?**
- ✅ Automatic authentication (no CLI setup)
- ✅ All Genie spaces pre-configured in `app.yaml`
- ✅ Share with team via URL
- ✅ Production-ready hosting

**See `DEPLOY_TO_DATABRICKS.md` for detailed steps.**

---

### Option 2: Test Locally (Advanced)

Requires Databricks CLI authentication:

```bash
# 1. Authenticate
databricks auth login --host https://dbc-4a93b454-f17b.cloud.databricks.com --profile dlk-hackathon

# 2. Install and run
cd streamlit/spiffit-ai-calculator
pip install -r requirements.txt
streamlit run app.py --server.port 8000
```

**Note:** Local testing requires `.env` file with `DATABRICKS_PROFILE=dlk-hackathon`

## 🔧 Configuration

### ✅ Genie Spaces Already Configured!

Your Genie spaces are already set up with IDs from `dlk-hackathon` workspace:

- **Sales:** `spg-mocking-bird-sales` → `01f0c403c3cf184e9b7f1f6c9ee45905`
- **Analytics:** `spg-mocking-bird-analytics` → `01f0c404048613b3b494b1a64a1bca84`
- **Market:** `spg-mocking-bird-market` → `01f0c4043acf19dc936c37fd2a8bced3`

### For Local Testing:

**Option 1: Use the example file**
```bash
# Copy the example file
cp env.example .env

# Edit .env if you want to change space IDs (optional)
# Then run:
streamlit run app.py --server.port 8000
```

**Option 2: Set environment variables directly**
```bash
# Windows (PowerShell)
$env:GENIE_SPACE_ID="01f0c403c3cf184e9b7f1f6c9ee45905"
streamlit run app.py --server.port 8000

# Mac/Linux
export GENIE_SPACE_ID="01f0c403c3cf184e9b7f1f6c9ee45905"
streamlit run app.py --server.port 8000
```

**For Databricks deployment:**
Space IDs are already configured in `app.yaml` - just deploy!

**If not configured:** App will show a warning and fall back to Foundation Model API.

## 📊 What It Does Right Now

✅ **Query Parsing** - Understands user intent
- Calculates incentives
- Shows top performers
- What-if scenarios
- Comparisons

✅ **AI Integration** - Connected to Databricks LLMs
- Genie support
- Foundation Model API support
- Natural language responses

⏳ **Next Steps** - Connect to calculator
- Import your calculator from `cursor/prototypes/02_incentive_calculator.py`
- Connect to Delta Lake tables
- Return real calculation results

## 🔗 Connecting the Calculator

To make this work with real data:

1. **Copy calculator code:**
```bash
cp cursor/prototypes/02_incentive_calculator.py streamlit/spiffit-ai-calculator/
```

2. **Update app.py imports:**
```python
from incentive_calculator import IncentiveCalculator

# Initialize calculator
calculator = IncentiveCalculator(spark)
```

3. **Replace demo responses with real calculations:**
```python
if parsed['intent'] == "calculate_incentive":
    result = calculator.calculate_total_incentive(parsed['employee_name'])
    response = ai.ask_question(
        f"Format this data: {result}",
        calculator_results=result
    )
```

See `ai_integration_guide.md` in the parent folder for detailed instructions.

## 🎯 Example Queries

### 💬 Chat Tab (Internal Data):
- "What's my incentive?"
- "Show John Smith's total payout"
- "Who are the top 10 performers?"
- "What if I close $50K more in MRR?"
- "How am I tracking against my budget?"

### 🌐 Competitor Intelligence Tab (NEW!):
- "What SPIFFs is AT&T offering in Q4?"
- "Compare Verizon and T-Mobile programs"
- "How do our incentives compare to competitors?"
- "What are common themes in competitor promotions?"
- "Recommend competitive SPIFFs based on market analysis"

## 🆘 Troubleshooting

**AI/LLM not responding?**
- Check Databricks SDK is installed
- Verify workspace permissions
- Try switching between Genie/Foundation Model

**Query parsing not working?**
- Check `query_parser.py` patterns
- Add more employee names to the parser
- Use the "What I understood" expander to debug

**Want simpler version?**
- See bottom of `ai_integration_guide.md` for keyword-only approach
- No AI needed for basic routing

## 📚 Documentation

- **AI Integration Guide:** `../ai_integration_guide.md`
- **Full Implementation Plan:** `../../cursor/automation-ideas/implementation-plans/use-case-1-ai-calculator.md`
- **Calculator Code:** `../../cursor/prototypes/02_incentive_calculator.py`

**Good luck! 🚀**

