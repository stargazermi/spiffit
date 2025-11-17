# Spiffit AI Calculator

## 🎯 Purpose
Natural language interface for incentive calculations using Databricks AI.

## 📁 Files
- `app.py` - Main Streamlit application with chat interface
- `ai_helper.py` - AI/LLM integration (Genie & Foundation Models)
- `query_parser.py` - Natural language query parsing
- `app.yaml` - Databricks App configuration
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🚀 Quick Start

### Option 1: Test Locally
```bash
cd streamlit/spiffit-ai-calculator
pip install -r requirements.txt
streamlit run app.py --server.port 8000
```

### Option 2: Deploy to Databricks

```bash
# Push to Git
git add streamlit/spiffit-ai-calculator/
git commit -m "Add AI calculator app"
git push origin main

# In Databricks:
# 1. Go to Apps
# 2. Create App
# 3. Source: Your repo (spiffit)
# 4. Path: streamlit/spiffit-ai-calculator/
# 5. Deploy!
```

## 🔧 Configuration

### Set Your Genie Space ID

The app reads the Genie Space ID from the `GENIE_SPACE_ID` environment variable.

**For local testing:**
```bash
# Windows (PowerShell)
$env:GENIE_SPACE_ID="your-space-id"
streamlit run app.py --server.port 8000

# Mac/Linux
export GENIE_SPACE_ID=your-space-id
streamlit run app.py --server.port 8000
```

**For Databricks deployment:**
Edit `app.yaml` and uncomment the GENIE_SPACE_ID section:
```yaml
env:
  - name: GENIE_SPACE_ID
    value: "your-space-id-here"
```

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

Try these questions:
- "What's my incentive?"
- "Show John Smith's total payout"
- "Who are the top 10 performers?"
- "What if I close $50K more in MRR?"
- "How am I tracking against my budget?"

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

