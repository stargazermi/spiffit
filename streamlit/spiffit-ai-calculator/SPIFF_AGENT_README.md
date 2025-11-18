# SPIFF Agent - Quick Start Guide

## 🚀 What is This?

An autonomous AI agent that manages your SPIFF (Sales Performance Incentive Fund) lifecycle:
- **Day 1**: Automatically generates month-end reports and winner emails
- **Day 15-20**: Analyzes data and recommends next month's SPIFFs
- **Weekly**: Monitors progress and sends alerts
- **Always**: Learns and adapts based on what it discovers

---

## 📁 Files

```
spiffit-ai-calculator/
├── spiff_agent.py           # Core agent logic
├── spiff_agent_app.py       # Streamlit dashboard
├── SPIFF_AGENT_README.md    # This file
└── ...
```

---

## ⚙️ Configuration

### Step 1: Set Up Genie Spaces

You need 3 Genie spaces configured:

```bash
# Sales performance data
export GENIE_SALES_SPACE_ID="your-sales-space-id"

# Analytics and winners (Data analyst's space)
export GENIE_ANALYTICS_SPACE_ID="your-analytics-space-id"

# Market intelligence and competitors
export GENIE_MARKET_SPACE_ID="your-market-space-id"
```

**For Databricks deployment**, add to `app.yaml`:
```yaml
env:
  - name: GENIE_SALES_SPACE_ID
    value: "01efa5e57638161591974326e56e4807"
  - name: GENIE_ANALYTICS_SPACE_ID
    value: "your-analytics-space-id"
  - name: GENIE_MARKET_SPACE_ID
    value: "your-market-space-id"
```

---

## 🏃 Running Locally

### Option 1: Dashboard App (Interactive)

```bash
cd streamlit/spiffit-ai-calculator
pip install -r requirements.txt

# Set environment variables
export GENIE_SALES_SPACE_ID="your-sales-space-id"
export GENIE_ANALYTICS_SPACE_ID="your-analytics-space-id"
export GENIE_MARKET_SPACE_ID="your-market-space-id"

# Run the dashboard
streamlit run spiff_agent_app.py --server.port 8000
```

Open browser to: http://localhost:8000

### Option 2: Standalone Script (Automated)

```bash
cd streamlit/spiffit-ai-calculator

# Run agent once (checks date and executes appropriate workflow)
python spiff_agent.py
```

---

## 🎯 How It Works

### The Agent's Timeline

```
┌──────────────────────────────────────────────────────────┐
│ Day 1-5: REVIEW PHASE                                    │
│ Agent generates previous month's results                 │
│ • Queries analytics space for winners                    │
│ • Gets achievement details from sales space              │
│ • Creates winner email                                   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Day 15-20: PLANNING PHASE ⭐                             │
│ Agent recommends next month's SPIFFs                     │
│ • Analyzes historical trends                             │
│ • Checks competitor offerings                            │
│ • Reasons about opportunities                            │
│ • Generates recommendations                              │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Weekly: PROGRESS CHECKS                                  │
│ Agent monitors current month                             │
│ • Tracks against targets                                 │
│ • Identifies issues early                                │
│ • Sends alerts if needed                                 │
└──────────────────────────────────────────────────────────┘
```

### Agent Reasoning Example

When it's Day 15 (recommendation time), the agent:

1. **Plans Investigation**
   ```
   Agent thinks: "I need to recommend next month's SPIFFs.
   What information do I need?"
   ```

2. **Gathers Data Dynamically**
   ```
   Step 1: Query analytics → "What worked last month?"
   Step 2: Agent analyzes → "Double MRR was successful"
   Step 3: Agent decides → "I should check competition"
   Step 4: Query market → "What are competitors offering?"
   Step 5: Agent synthesizes → "Here's what we should do..."
   ```

3. **Generates Recommendations**
   ```
   The agent produces detailed SPIFF proposals with:
   - Program names
   - Target behaviors
   - Incentive amounts
   - Reasoning and expected ROI
   ```

---

## 📊 Example Outputs

### Month-End Email (Day 1)

```
Subject: 🎉 November SPIFF Results - Record Breaking Month!

Team,

What an INCREDIBLE November! You absolutely crushed it! 🚀

📊 BY THE NUMBERS:
- Total SPIFF payouts: $830K
- Revenue generated: $8.2M (+60% vs last year!)
- Participation: 85% of team
- Program ROI: 4.2x

🏆 TOP PERFORMERS:
1. Sarah Johnson - $45,230 in SPIFFs
2. Mike Chen - $38,150 in SPIFFs
3. Lisa Wang - $32,400 in SPIFFs

[Full details...]
```

### SPIFF Recommendations (Day 15-20)

```
📋 DECEMBER 2025 SPIFF RECOMMENDATIONS

1. 🎄 "Holiday Mega Deal Bonus"
   Target: Deals >$150K closed in December
   Incentive: $7,500 bonus + extra 5% commission
   
   Reasoning:
   - Counters competitor's $5K bonus (we're more generous)
   - Aligns with Q4 large deal trend (+35%)
   - Year-end urgency drives closings
   
   Expected Impact: +$12M revenue
   Budget: $300K

2. 🚀 "New Vertical Accelerator"
   [Details...]

3. 💰 "Year-End Renewal Rush"
   [Details...]

TOTAL BUDGET: $525K
EXPECTED ROI: 3.8x
```

---

## 🔧 Customization

### Adjust Agent Triggers

Edit `spiff_agent.py`:

```python
def check_and_act(self):
    day_of_month = datetime.now().day
    
    # Customize these triggers
    if day_of_month == 1:
        return self.generate_month_end_report()
    elif 15 <= day_of_month <= 20:  # Change this range
        return self.recommend_next_month_spiffs()
    # Add your own triggers...
```

### Add New Investigation Steps

```python
def _create_investigation_plan(self, target_month):
    return {
        "steps": [
            # Add your own steps
            {
                "action": "Check team capacity",
                "reason": "Need to ensure SPIFFs are achievable",
                "key": "capacity",
                "space": "sales_data"
            }
        ]
    }
```

---

## 🚀 Deploying to Databricks

### Option 1: Scheduled Job (Recommended)

Create a Databricks job that runs daily:

```yaml
# databricks_job.yml
jobs:
  - name: "SPIFF Agent Daily Run"
    schedule:
      quartz_cron_expression: "0 0 9 * * ?"  # 9 AM daily
    tasks:
      - task_key: "run_agent"
        python_wheel_task:
          package_name: "spiff_agent"
          entry_point: "run"
```

### Option 2: Databricks App

Deploy as a Databricks App:

```bash
# In your Databricks workspace:
# 1. Create new App
# 2. Source: Your GitHub repo
# 3. Path: streamlit/spiffit-ai-calculator/
# 4. Entry point: spiff_agent_app.py
# 5. Add environment variables for Genie spaces
```

---

## 🧪 Testing

### Test Different Scenarios

```python
# In Python console or notebook
from spiff_agent import SPIFFAgent

agent = SPIFFAgent()

# Simulate Day 1 (month-end)
result = agent.generate_month_end_report(datetime(2025, 12, 1))

# Simulate Day 15 (recommendations)
result = agent.recommend_next_month_spiffs(datetime(2025, 12, 15))
```

### Test Individual Queries

Use the dashboard's "Manual Testing" section to:
- Test different dates
- Query individual Genie spaces
- See agent reasoning

---

## 📚 Related Documentation

- **[AUTONOMOUS_SPIFF_AGENT.md](../AUTONOMOUS_SPIFF_AGENT.md)** - Full architecture docs
- **[SMART_GENIE_ROUTING.md](../SMART_GENIE_ROUTING.md)** - Routing implementation
- **[MULTI_GENIE_WORKFLOWS.md](../MULTI_GENIE_WORKFLOWS.md)** - Workflow examples

---

## ⚠️ Troubleshooting

### "Genie space not configured"
```bash
# Check environment variables are set
echo $GENIE_SALES_SPACE_ID
echo $GENIE_ANALYTICS_SPACE_ID
echo $GENIE_MARKET_SPACE_ID

# If empty, set them:
export GENIE_SALES_SPACE_ID="your-id"
```

### "Agent returns simulated responses"
- This happens when Genie spaces aren't configured
- The agent will show `[Simulated response from space_name]`
- Fix by setting the environment variables

### "LLM calls failing"
- Check Databricks authentication: `databricks auth login`
- Verify workspace has Foundation Model API access
- Check model name: `databricks-meta-llama-3-1-70b-instruct`

---

## 🎯 Demo Tips for Hackathon

### Best Features to Show

1. **Time Awareness**
   - Show dashboard on different days
   - Demonstrate how agent changes behavior

2. **Intelligent Reasoning**
   - Run on Day 15 to show recommendation workflow
   - Show the investigation steps and follow-ups
   - Highlight how agent asks follow-up questions

3. **Multi-Genie Integration**
   - Show queries going to different spaces
   - Demonstrate data synthesis

4. **Practical Output**
   - Show generated email on Day 1
   - Show detailed recommendations on Day 15

### Presentation Flow

```
1. "This is the agent dashboard" [Show spiff_agent_app.py]
2. "The agent is aware of the calendar" [Show timeline]
3. "Let's run it now" [Click Run Agent]
4. "Watch it reason through the problem" [Show investigation steps]
5. "Here's the output" [Show recommendations/email]
6. "This runs automatically on schedule" [Explain deployment]
```

---

## 🚀 Next Steps

1. ✅ Configure your 3 Genie spaces
2. ✅ Test locally with `streamlit run spiff_agent_app.py`
3. ✅ Verify agent can query your spaces
4. ✅ Deploy to Databricks as scheduled job or app
5. ✅ Watch the agent work its magic!

---

**Questions? Issues? Check the main documentation in `AUTONOMOUS_SPIFF_AGENT.md`** 🎉

