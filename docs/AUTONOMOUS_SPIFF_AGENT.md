# Autonomous SPIFF Recommendation Agent

## 🎯 Overview

This document describes an intelligent, time-aware agent that autonomously manages the SPIFF (Sales Performance Incentive Fund) lifecycle by:
- Monitoring the calendar and triggering actions at key dates
- Analyzing historical performance data
- Checking competitor offerings
- Recommending next month's SPIFFs
- Generating performance reports and emails

---

## 🤖 Agent Architecture

### Agent Capabilities

**A. Time Awareness**
- Knows current day of month
- Triggers recommendations around day 15 (mid-month planning)
- Generates reports on day 1 (month-end review)

**B. Competitive Intelligence**
- Checks competitor SPIFF offerings
- Identifies market opportunities
- Recommends competitive positioning

**C. Historical Analysis**
- Reviews previous month's performance
- Identifies trends and patterns
- Spots high-performing strategies

**D. Automated Reporting**
- Generates winner lists
- Creates email summaries
- Distributes results to stakeholders

---

## 📅 Agent Timeline & Triggers

```
Month Lifecycle:

Day 1-5: 📊 REVIEW PHASE
├─ Generate previous month's results report
├─ Identify SPIFF winners
├─ Create email with achievements
└─ Distribute to team

Day 6-14: 📈 MONITORING PHASE
├─ Track current month progress
├─ Alert on low performance
└─ Provide mid-month updates

Day 15-20: 💡 PLANNING PHASE ⭐
├─ Analyze historical trends
├─ Check competitor SPIFFs
├─ Recommend next month's incentives
├─ Generate proposal document
└─ Submit for approval

Day 21-30: ✅ EXECUTION PHASE
├─ Finalize approved SPIFFs
├─ Communicate to sales team
├─ Set up tracking
└─ Prepare for next cycle
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│  SPIFF Agent (Orchestrator)                             │
│  - Time-aware scheduling                                │
│  - Reasoning & decision making                          │
│  - Workflow coordination                                │
└────────────┬────────────────────────────────────────────┘
             │
     ┌───────┴────────┐
     │                │
     ▼                ▼
┌─────────────┐  ┌─────────────────────────────────┐
│ Date/Time   │  │  Multi-Genie Spaces             │
│ Service     │  │                                 │
└─────────────┘  │  ┌─────────────────────┐       │
                 │  │ Space A: Sales Data │       │
                 │  │ - Performance       │       │
                 │  │ - Historical trends │       │
                 │  └─────────────────────┘       │
                 │                                 │
                 │  ┌─────────────────────┐       │
                 │  │ Space B: Analytics  │       │
                 │  │ - Winners/rankings  │       │
                 │  │ - Trend analysis    │       │
                 │  └─────────────────────┘       │
                 │                                 │
                 │  ┌─────────────────────┐       │
                 │  │ Space C: Market     │       │
                 │  │ - Competitor data   │       │
                 │  └─────────────────────┘       │
                 └─────────────────────────────────┘
                             │
                             ▼
                 ┌─────────────────────────────────┐
                 │  Output Actions                 │
                 │  - Email generation             │
                 │  - Report creation              │
                 │  - Recommendations              │
                 └─────────────────────────────────┘
```

---

## 💬 Example Agent Reasoning

### Scenario 1: Day 15 - Recommendation Time

```
Agent Internal Reasoning:

📅 Date Check: November 15, 2025
✓ Status: Mid-month planning window (Day 15)
→ Action: Initiate SPIFF recommendation workflow

Step 1: Gather Context
Agent thinks: "I need to understand current market and performance"

→ Query Space A (Sales Data):
  "What were our Q4 SPIFF results? Which SPIFFs had highest participation?"
  
  Result: 
  - "Double MRR November": 85% participation, +23% revenue
  - "New Logo Bonus": 45% participation, +12 new customers
  - "Renewal Rescue": 30% participation, +$2M saved

Agent analyzes: "Double MRR was very successful. Renewal Rescue had 
low participation - might not be compelling enough."

Step 2: Check Competition
Agent thinks: "What are competitors offering? I should match or beat."

→ Query Space C (Market Intelligence):
  "What SPIFFs are competitors running in December 2025?"
  
  Result:
  - Competitor A: $5K bonus for deals >$100K (Q4 only)
  - Competitor B: Triple commission on new verticals
  - Industry trend: Holiday season push with urgency incentives

Agent analyzes: "Competitors are focusing on large deals and new markets.
We should counter with similar but differentiated approach."

Step 3: Historical Trend Analysis
Agent thinks: "December is typically a strong month. What worked last year?"

→ Query Space B (Analytics):
  "Show me December 2024 SPIFF performance and trends"
  
  Result:
  - Dec 2024: "Holiday Close Bonus" generated $8M extra revenue
  - Q4 historically sees 35% more large deals (>$100K)
  - December urgency: Customers want to close before year-end

Agent analyzes: "End-of-year urgency is real. Should leverage that."

Step 4: Identify Opportunities
Agent thinks: "Based on all this data, what should we offer?"

→ Internal Reasoning:
  Factors considered:
  - November's Double MRR was highly successful (85% participation)
  - Competitors pushing large deal bonuses
  - December has historical strength in enterprise deals
  - Year-end urgency creates opportunity
  - Renewal Rescue needs improvement or replacement

Step 5: Generate Recommendations

Agent produces:

═══════════════════════════════════════════════════════════
📋 DECEMBER 2025 SPIFF RECOMMENDATIONS

Recommended SPIFFs:

1. 🎄 "Holiday Mega Deal Bonus"
   - Target: Deals >$150K closed in December
   - Incentive: $7,500 bonus + extra 5% commission
   - Reasoning: 
     * Counters competitor's $5K bonus (we're more generous)
     * Aligns with Q4 large deal trend (+35% in Dec)
     * Year-end urgency drives customers to close
   - Expected Impact: +$12M revenue, 40% participation
   - Budget: $300K

2. 🚀 "New Vertical Accelerator"
   - Target: First deal in Healthcare or Finance vertical
   - Incentive: $5K bonus + priority SC support
   - Reasoning:
     * Matches Competitor B's vertical push
     * Opens new markets for 2026
     * Low risk (first-deal only)
   - Expected Impact: 15 new vertical accounts
   - Budget: $75K

3. 💰 "Year-End Renewal Rush"
   - Target: Renewals signed before Dec 20
   - Incentive: 2x renewal commission
   - Reasoning:
     * Improves on underperforming "Renewal Rescue"
     * Early Dec timing reduces year-end chaos
     * Secures revenue for FY2026
   - Expected Impact: +$5M early renewals, 50% participation
   - Budget: $150K

TOTAL BUDGET: $525K
EXPECTED ROI: 3.8x (conservative)

Competitive Positioning:
✓ Beat Competitor A on large deal bonus ($7.5K vs $5K)
✓ Match Competitor B on vertical expansion
✓ Unique angle: Early renewal incentive (no competitor has this)

Historical Validation:
✓ Similar program in Dec 2024 generated $8M
✓ Builds on successful November "Double MRR" momentum
✓ Addresses low participation in renewal programs

RECOMMENDATION: Approve and communicate by Nov 20
═══════════════════════════════════════════════════════════

Agent next action: Generate approval document and email draft
```

---

### Scenario 2: Day 1 - Month-End Review

```
Agent Internal Reasoning:

📅 Date Check: December 1, 2025
✓ Status: Beginning of month (Day 1)
→ Action: Generate November results report

Step 1: Get SPIFF Results
Agent thinks: "Who won the November SPIFFs?"

→ Query Space B (Analytics/Winners):
  "Who achieved the November SPIFF targets? Generate leaderboard."
  
  Result:
  - Double MRR SPIFF: 34 qualifiers, $680K in bonuses
  - New Logo Bonus: 18 qualifiers, $90K in bonuses
  - Renewal Rescue: 12 qualifiers, $60K in bonuses

Top performers:
1. Sarah Johnson - $45K in SPIFFs (3 categories!)
2. Mike Chen - $38K in SPIFFs
3. Lisa Wang - $32K in SPIFFs

Step 2: Gather Supporting Details
Agent thinks: "I need the details to make this email compelling"

→ Query Space A (Sales Data):
  "For each SPIFF winner, what specific achievements qualified them?"
  
  Result:
  Sarah Johnson:
  - Closed $450K MRR (2.8x her quota)
  - Brought in 4 new logos ($600K TCV)
  - Saved 3 at-risk renewals ($1.2M)
  - Total impact: $2.25M revenue

  Mike Chen:
  - Closed $380K MRR (2.4x quota)
  - Brought in 3 new logos ($480K TCV)
  - Total impact: $1.86M revenue

  [... more details ...]

Step 3: Analyze Program Success
Agent thinks: "How did the overall program perform?"

→ Query Space B (Analytics):
  "Compare November 2025 vs November 2024 SPIFF impact"
  
  Result:
  - Revenue impact: +$8.2M (vs +$5.1M last year) = +60%
  - Participation: 85% (vs 72% last year) = +18%
  - ROI: 4.2x (vs 3.1x last year) = +35%
  - Team morale: Survey score 9.2/10

Step 4: Generate Email
Agent produces:

═══════════════════════════════════════════════════════════
Subject: 🎉 November SPIFF Results - Record Breaking Month!

Team,

What an INCREDIBLE November! You absolutely crushed it! 🚀

📊 BY THE NUMBERS:
- Total SPIFF payouts: $830K
- Revenue generated: $8.2M (+60% vs last year!)
- Participation: 85% of team earned SPIFFs
- Program ROI: 4.2x

🏆 TOP PERFORMERS:

1️⃣ Sarah Johnson - $45,230 in SPIFFs 👑
   - 2.8x MRR quota ($450K)
   - 4 new logos ($600K TCV)
   - 3 rescued renewals ($1.2M saved)
   - Total impact: $2.25M
   → Sarah, you're an absolute superstar!

2️⃣ Mike Chen - $38,150 in SPIFFs ⭐
   - 2.4x MRR quota ($380K)
   - 3 new logos ($480K TCV)
   - Total impact: $1.86M
   → Mike, exceptional execution!

3️⃣ Lisa Wang - $32,400 in SPIFFs 🌟
   - 2.1x MRR quota ($315K)
   - 2 new logos + 2 renewals
   - Total impact: $1.4M
   → Lisa, outstanding consistency!

[... Full leaderboard of 34 winners attached ...]

💰 SPIFF PAYOUTS:
All November SPIFFs will be paid with your December 15 paycheck.

🎄 WHAT'S NEXT?
December SPIFFs are even BIGGER! Check your email from 
[Manager] for details on our Holiday Mega Deal Bonus and 
Year-End Renewal Rush programs.

Let's finish 2025 with an absolute BANG! 💥

Congratulations to everyone who earned SPIFFs - you earned it!

[Automated by SPIFF Agent]
═══════════════════════════════════════════════════════════

Agent actions:
✓ Email sent to entire sales team
✓ Detailed report sent to VP Sales
✓ Accounting notified of $830K payout
✓ Leaderboard published on sales dashboard
```

---

## 🛠️ Implementation Architecture

### Core Components

**1. Time-Aware Scheduler**
```python
class TimeAwareScheduler:
    """
    Monitors date and triggers appropriate agent actions
    """
    
    def check_and_trigger(self):
        today = datetime.now()
        day_of_month = today.day
        
        if day_of_month == 1:
            return "month_end_review"
        elif 15 <= day_of_month <= 20:
            return "recommendation_time"
        elif day_of_month in [7, 14, 21, 28]:
            return "progress_check"
        else:
            return "monitoring"
```

**2. Agent Reasoner**
```python
class SPIFFAgent:
    """
    Intelligent agent that reasons about SPIFFs
    """
    
    def reason_and_act(self, trigger):
        # Agent determines what it needs to know
        investigation_plan = self.plan_investigation(trigger)
        
        # Agent gathers data dynamically
        gathered_data = self.investigate(investigation_plan)
        
        # Agent reasons about what it learned
        insights = self.analyze(gathered_data)
        
        # Agent decides what to do
        action = self.decide_action(insights)
        
        # Agent executes
        return self.execute(action)
```

**3. Multi-Genie Router**
```python
class MultiGenieRouter:
    """
    Routes queries to appropriate Genie spaces
    """
    
    def route_intelligent(self, query):
        # Determine which space(s) can answer
        relevant_spaces = self.classify_query(query)
        
        # Query all relevant spaces
        results = {}
        for space in relevant_spaces:
            results[space] = self.query_space(space, query)
        
        # Synthesize results
        return self.synthesize(results)
```

---

## 📊 Data Flow Diagrams

### Recommendation Workflow (Day 15)

```
┌──────────────────────────────────────────────────────────┐
│ Trigger: Day 15 detected                                 │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ Agent: "I need to recommend next month's SPIFFs"         │
│ Plan: Gather historical data → Check competition →      │
│       Identify opportunities → Generate recommendations  │
└────────────────┬─────────────────────────────────────────┘
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
┌──────────────┐    ┌──────────────────┐
│ Genie Space  │    │ Genie Space B    │
│ A: Sales     │    │ Analytics        │
│              │    │                  │
│ Query:       │    │ Query:           │
│ "Last month  │    │ "Historical      │
│  SPIFF       │    │  December        │
│  results?"   │    │  trends?"        │
└──────┬───────┘    └────────┬─────────┘
       │                     │
       └──────────┬──────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────┐
│ Agent Analyzes: "Double MRR was successful (85%)        │
│ December historically strong for large deals"            │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ Agent Decides: "Need competitor intelligence"            │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ Genie Space C: Market Intelligence                       │
│ Query: "What are competitors offering in December?"      │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ Agent Synthesizes:                                       │
│ - Our historical data                                    │
│ - Competitor offers                                      │
│ - Market trends                                          │
│ → Generates 3 recommended SPIFFs with reasoning          │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│ Output: Recommendation document + Email to approvers     │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Agent Decision Matrix

| Trigger | Agent Investigation | Data Sources | Output |
|---------|-------------------|--------------|---------|
| **Day 1** | Who won last month? | Space B (Analytics) | Winner email |
| **Day 15** | What should we offer next? | Space A, B, C (All) | Recommendations |
| **Day 7/14/21/28** | How are we tracking? | Space A (Sales) | Progress alert |
| **Competitor update** | What changed in market? | Space C (Market) | Strategy update |

---

## 💡 Intelligence Features

### 1. Adaptive Questioning
Agent doesn't follow a script - it asks follow-ups based on what it learns:

```python
# Initial query
result = query("What were November SPIFF results?")

# Agent notices something unusual
if result.shows_low_participation("Renewal Rescue"):
    # Agent decides to investigate
    follow_up = query("Why was Renewal Rescue participation low?")
    
    # Agent learns it's not compelling enough
    if follow_up.indicates_low_value:
        # Agent decides to recommend replacement
        recommendation = "Replace with more attractive renewal incentive"
```

### 2. Context Awareness
Agent maintains conversation history:

```python
# Agent remembers what it learned earlier
if previously_learned("Large deals trending up"):
    # Agent connects the dots
    recommendation.emphasize("large deal incentives")
```

### 3. Proactive Alerts
Agent doesn't wait to be asked:

```python
if current_month_performance < 70% of target:
    agent.send_alert("⚠️ Current month tracking below target!")
```

---

## 📝 Configuration

### Genie Space Mapping

```yaml
spaces:
  sales_data:
    space_id: "your-sales-space-id"
    description: "Historical sales performance, deals, quotas"
    use_for:
      - Historical analysis
      - Performance tracking
      - Achievement verification
  
  analytics:
    space_id: "your-analytics-space-id"  # Data analyst's space
    description: "SPIFF winners, leaderboards, trend analysis"
    use_for:
      - Winner identification
      - Month-end reports
      - Trend analysis
  
  market_intelligence:
    space_id: "your-market-space-id"
    description: "Competitor data, industry trends"
    use_for:
      - Competitive analysis
      - Market positioning
      - Opportunity identification

triggers:
  day_1: "month_end_review"
  day_15_to_20: "recommendation_time"
  weekly: "progress_check"
```

---

## 🚀 Deployment Options

### Option 1: Scheduled Databricks Job
```yaml
# Run daily to check date and trigger appropriate action
job:
  name: "SPIFF Agent Daily Check"
  schedule:
    quartz_cron_expression: "0 0 9 * * ?" # 9 AM daily
  tasks:
    - task_key: "agent_check"
      notebook_task:
        notebook_path: "/notebooks/spiff_agent"
```

### Option 2: Streamlit Dashboard
```python
# Real-time dashboard showing agent status
st.title("🤖 SPIFF Agent Dashboard")

# Show current phase
current_phase = agent.get_current_phase()
st.info(f"Current Phase: {current_phase}")

# Manual trigger option
if st.button("🔄 Run Agent Now"):
    result = agent.run()
    st.write(result)
```

### Option 3: Serverless Function
```python
# AWS Lambda / Azure Functions
def lambda_handler(event, context):
    agent = SPIFFAgent()
    result = agent.check_and_act()
    return result
```

---

## 📚 Related Documentation

- **Smart Routing**: `SMART_GENIE_ROUTING.md`
- **Multi-Genie Workflows**: `MULTI_GENIE_WORKFLOWS.md`
- **AI Integration**: `ai_integration_guide.md`

---

## 🎯 Success Metrics

**Agent Effectiveness:**
- ✅ Recommendations generated on time (Day 15-20)
- ✅ Reports sent within 24 hours of month-end
- ✅ 90%+ accuracy in winner identification
- ✅ Recommendations align with business goals

**Business Impact:**
- 📈 SPIFF participation rate
- 💰 Revenue per SPIFF dollar
- 🎯 Goal achievement rate
- 😊 Sales team satisfaction

---

**Ready to implement! See `spiff_agent.py` for working code.** 🚀

