# Multi-Genie Workflow Use Cases

## 📖 Overview

This document provides real-world examples of how to orchestrate multiple Genie spaces together to create powerful cross-functional workflows.

---

## 🎯 Why Use Multiple Genie Spaces?

### Common Reasons:

1. **Different Data Domains** - Each space connects to different databases/tables
2. **Security/Access Control** - Separate spaces for sensitive data
3. **Specialized Functions** - One space for data, another for analytics, another for reporting
4. **Team Ownership** - Different teams manage different spaces
5. **Performance** - Distribute load across multiple SQL warehouses

---

## 💼 Use Case 1: Sales Incentive Calculation

**Perfect for:** Sales operations, finance teams, compensation planning

### Setup:
- **Genie Space A**: Sales data (connected to CRM/sales tables)
- **Genie Space B**: Finance data (connected to budget/target tables)
- **Genie Space C**: HR data (connected to employee/hierarchy tables)

### Example Conversation Flow:

```
User: "Calculate incentive for John Smith"

→ SPACE A (Sales Data):
User: "What were John Smith's Q4 sales metrics?"
Genie A: "John Smith achieved:
- MRR: $125,000 (actual) vs $100,000 (target) = 125%
- TCV: $450,000 (actual) vs $400,000 (target) = 112.5%
- New customers: 12"

→ SPACE B (Finance/Budget):
User: "What is the incentive rate for someone at 125% MRR attainment?"
Genie B: "At 125% MRR attainment, the tier is 'Accelerator'
- Base incentive: 15% of budget
- Accelerator bonus: +5%
- Total rate: 20% of achieved revenue"

→ SPACE C (HR/Hierarchy):
User: "What is John Smith's role and compensation band?"
Genie C: "John Smith
- Role: Senior Account Executive
- Band: Level 3
- Manager: Sarah Johnson
- Region: Northeast
- Eligible for: Full incentive program"

→ Python Calculator (Your Code):
# Takes all the data and calculates final number

→ SPACE A (Reporting - back to sales space):
User: "Format this incentive calculation as an executive summary"
Genie A: "Q4 Incentive Summary for John Smith
🎉 Total Incentive: $45,230
Outstanding performance at 125% of MRR target!

Breakdown:
- MRR Component: $20,000 (125% attainment → Accelerator tier)
- TCV Component: $15,000 (112.5% attainment)
- Renewal Bonus: $10,230

Well done exceeding all targets!"
```

### Benefits:
- ✅ Data stays in appropriate systems
- ✅ Each team maintains their own space
- ✅ Security boundaries respected
- ✅ Comprehensive view across functions

---

## 💼 Use Case 2: Customer Health Score

**Perfect for:** Customer success, account management, retention analysis

### Setup:
- **Genie Space A**: Customer usage data (product analytics)
- **Genie Space B**: Support ticket data (help desk system)
- **Genie Space C**: Financial data (billing/payment history)

### Example Conversation:

```
User: "What's the health score for Acme Corp?"

→ SPACE A (Usage):
User: "How is Acme Corp using our product this quarter?"
Genie A: "Acme Corp usage metrics:
- Daily active users: 450 (up 15% from Q3)
- Feature adoption: 78%
- API calls: 1.2M/month
- Last login: 2 hours ago
⚡ High engagement!"

→ SPACE B (Support):
User: "How many support tickets has Acme Corp opened?"
Genie B: "Support ticket analysis for Acme Corp:
- Open tickets: 2 (Priority: Low)
- Avg resolution time: 4 hours
- Satisfaction score: 4.8/5
- Escalations: 0 in last 90 days
✅ Healthy support relationship"

→ SPACE C (Billing):
User: "What's Acme Corp's payment history?"
Genie C: "Payment status for Acme Corp:
- Current MRR: $15,000/month
- Payment status: Current (never late)
- Contract: Enterprise plan
- Renewal date: March 2026
💚 Financially healthy"

→ Final Analysis (LLM):
"Overall Health Score: 92/100 - HEALTHY
- Product Engagement: Excellent (95)
- Support Health: Excellent (96)
- Financial Health: Excellent (100)

Recommendation: Upsell opportunity - high usage indicates room for expansion."
```

### Benefits:
- ✅ 360° view of customer
- ✅ Early warning signs from multiple signals
- ✅ Data-driven renewal decisions
- ✅ Upsell opportunity identification

---

## 💼 Use Case 3: Cross-Functional Project Status

**Perfect for:** Project managers, leadership, cross-team coordination

### Setup:
- **Genie Space A**: Engineering data (Jira, GitHub)
- **Genie Space B**: Design data (Figma, design docs)
- **Genie Space C**: Marketing data (campaigns, analytics)

### Example Conversation:

```
User: "Status update on Project Phoenix"

→ SPACE A (Engineering):
User: "What's the engineering progress on Project Phoenix?"
Genie A: "Project Phoenix - Engineering Status:
- Sprint: 12 of 16 complete
- Story points: 145/200 complete (72.5%)
- Blockers: 2 critical bugs
- Code coverage: 87%
- Target launch: 3 weeks"

→ SPACE B (Design):
User: "What's the design status for Project Phoenix?"
Genie B: "Project Phoenix - Design Status:
- Design system: 100% complete
- User flows: 8/10 approved
- Prototypes: Ready for dev handoff
- User testing: Completed with positive feedback"

→ SPACE C (Marketing):
User: "Is marketing ready for Project Phoenix launch?"
Genie C: "Project Phoenix - Marketing Status:
- Landing page: In review
- Email campaigns: Drafted, pending approval
- Social media: Content calendar ready
- PR: Press release scheduled for launch week
⚠️ Need 2 more weeks for full readiness"

→ Summary (Aggregated):
"Project Phoenix Cross-Functional Status:
🟢 Engineering: On track (72.5% complete)
🟢 Design: Ready (all deliverables complete)
🟡 Marketing: Needs time (2 weeks behind)

RECOMMENDATION: Delay launch by 2 weeks to align marketing readiness."
```

### Benefits:
- ✅ Single view across all teams
- ✅ Identify blockers early
- ✅ Coordinate timelines
- ✅ Data-driven launch decisions

---

## 💼 Use Case 4: Compliance & Risk Assessment

**Perfect for:** Audit teams, compliance officers, risk management

### Setup:
- **Genie Space A**: Transaction data (financial systems)
- **Genie Space B**: Compliance rules (policy database)
- **Genie Space C**: Audit logs (security systems)

### Example Conversation:

```
User: "Audit this $500K deal for compliance"

→ SPACE A (Transaction Data):
User: "Show me details of deal #12345"
Genie A: "Deal #12345:
- Amount: $500,000
- Customer: GlobalTech Inc
- AE: Maria Rodriguez
- Discount: 25%
- Contract term: 3 years
- Signed: January 15, 2025"

→ SPACE B (Compliance Rules):
User: "What approval is required for a $500K deal with 25% discount?"
Genie B: "Approval requirements:
- Deals >$250K: Director approval ✅
- Discounts >20%: VP approval ✅
- 3-year terms: CFO approval ❌ MISSING
⚠️ CFO sign-off required but not found"

→ SPACE C (Audit Logs):
User: "Show approval trail for deal #12345"
Genie C: "Approval audit trail:
✅ Jan 12: AE submitted (Maria Rodriguez)
✅ Jan 13: Director approved (John Smith)
✅ Jan 14: VP approved (Sarah Lee)
❌ CFO approval: NOT RECORDED

ALERT: Deal closed without required CFO approval"

→ Risk Assessment (Final):
"Compliance Issue Detected:
🚨 Deal #12345 is NON-COMPLIANT

Missing: CFO approval for 3-year/$500K deal
Action needed: Immediate review + retroactive approval
Risk level: HIGH"
```

### Benefits:
- ✅ Automated compliance checking
- ✅ Full audit trail visibility
- ✅ Real-time risk detection
- ✅ Policy enforcement

---

## 💼 Use Case 5: Hiring Pipeline Analysis

**Perfect for:** Recruiting teams, hiring managers, talent acquisition

### Setup:
- **Genie Space A**: Recruiting data (ATS system)
- **Genie Space B**: Interview feedback (interview platform)
- **Genie Space C**: Comp data (HR systems)

### Example Conversation:

```
User: "Should we make an offer to candidate Jane Doe?"

→ SPACE A (Recruiting):
User: "What's Jane Doe's application history?"
Genie A: "Candidate: Jane Doe
- Applied: Senior Engineer position
- Source: LinkedIn referral
- Experience: 8 years
- Current stage: Final interview
- Time in pipeline: 18 days"

→ SPACE B (Interview Feedback):
User: "What did interviewers say about Jane Doe?"
Genie B: "Interview feedback summary:
Round 1 (Tech screen): Strong pass ⭐⭐⭐⭐⭐
Round 2 (System design): Pass ⭐⭐⭐⭐
Round 3 (Behavioral): Strong pass ⭐⭐⭐⭐⭐
Round 4 (Team fit): Pass ⭐⭐⭐⭐

Overall: 4 strong passes, 0 no-hires
Consensus: Make offer ASAP"

→ SPACE C (Compensation):
User: "What's the comp band for Senior Engineer with 8 YOE?"
Genie C: "Compensation analysis:
- Role: Senior Engineer
- Experience: 8 years
- Band: L5
- Salary range: $150K-$185K
- Equity: 0.08%-0.12%
- Sign-on: Up to $25K
Market data: Competitive for this profile"

→ Hiring Decision (Final):
"Recommendation: MAKE OFFER to Jane Doe

Evidence:
✅ Unanimous positive feedback (all 4 rounds)
✅ 18 days in pipeline (fast)
✅ Strong technical skills
✅ Culture fit confirmed
✅ Comp within band

Suggested offer:
- Base: $170K
- Equity: 0.10%
- Sign-on: $20K
Act fast - strong candidate likely has other offers!"
```

### Benefits:
- ✅ Data-driven hiring decisions
- ✅ Competitive offer analysis
- ✅ Fast consensus building
- ✅ Reduced time-to-hire

---

## 💼 Use Case 6: What-If Scenario Analysis

**Perfect for:** Strategic planning, forecasting, budget planning

### Setup:
- **Genie Space A**: Current performance data
- **Genie Space B**: Financial/budget data
- **Genie Space C**: Analytics/comparison data

### Example Conversation:

```
User: "What if our Northeast team all hit 120% of target?"

→ SPACE A (Current Performance):
User: "Get all Northeast AEs and their current performance"
Genie A: "Northeast Team (12 AEs):
- Current avg attainment: 95%
- Total actual MRR: $1.2M
- Total budget: $1.26M
- Current total incentives: $320K"

→ Python Calculator:
# Calculate new incentives at 120% for each AE

→ SPACE B (Budget Impact):
User: "What's the total budget impact of $450K in incentives?"
Genie B: "Budget analysis:
- Current incentive spend: $320K
- Projected at 120%: $450K
- Increase: +$130K (+40.6%)
- Annual incentive budget: $1.8M
- Remaining budget: $1.35M
✅ Within tolerance (75% of budget used)"

→ SPACE C (Regional Comparison):
User: "How would Northeast compare to other regions at 120%?"
Genie C: "Regional performance comparison:
Current state:
1. West: 108% avg attainment
2. Southeast: 102% avg attainment
3. Northeast: 95% avg attainment ⬅️ Currently #3

At 120% attainment:
1. Northeast: 120% avg attainment ⬅️ Would be #1 🏆
2. West: 108% avg attainment
3. Southeast: 102% avg attainment

Northeast would exceed company average by +18%"

→ Final Analysis:
"What-If Analysis: Northeast Team at 120%

Financial Impact:
- Total incentive payout: $450K (vs $320K current)
- Budget impact: +$130K (+40.6%)
- Still within annual budget: ✅

Performance Impact:
- Regional rank: Would move from #3 to #1
- Above company average: +18%
- Team morale: Significant boost expected

Feasibility:
✅ Achievable with focused effort
✅ Within budget tolerances
✅ Would set new company benchmark

Recommendation: Set this as stretch goal for Q2"
```

### Benefits:
- ✅ Model different scenarios quickly
- ✅ Understand cross-functional impact
- ✅ Budget planning and forecasting
- ✅ Goal-setting based on data

---

## 🛠️ Implementation Patterns

### Pattern 1: Sequential Processing
```python
result_a = genie_space_a.ask(question_1)
result_b = genie_space_b.ask(question_2, context=result_a)
result_c = genie_space_c.ask(question_3, context=[result_a, result_b])
```

### Pattern 2: Parallel Processing (Independent Queries)
```python
# Query multiple spaces simultaneously
results = await asyncio.gather(
    genie_space_a.ask(question_1),
    genie_space_b.ask(question_2),
    genie_space_c.ask(question_3)
)
# Aggregate results
```

### Pattern 3: Conditional Routing
```python
result_a = genie_space_a.ask(question)

if result_a.contains_risk:
    result_b = genie_space_compliance.ask(audit_question)
else:
    result_b = genie_space_standard.ask(standard_question)
```

---

## 💡 Best Practices

### 1. Context Passing
Always pass relevant context from previous steps:
```python
context = f"Previous data: {result_from_space_a}"
next_result = space_b.ask(f"{context}\n\nNew question: {question}")
```

### 2. Error Handling
Handle failures gracefully:
```python
try:
    result = space_a.ask(question)
except GenieError:
    # Fall back to alternative space or default behavior
    result = space_b.ask(alternative_question)
```

### 3. Caching
Cache intermediate results to avoid redundant queries:
```python
@cache
def get_employee_data(employee_id):
    return space_a.ask(f"Get data for employee {employee_id}")
```

### 4. Progress Indicators
Show users what's happening:
```python
with st.spinner("Querying sales data..."):
    sales_data = space_a.ask(question)

with st.spinner("Analyzing compliance..."):
    compliance_check = space_b.ask(question)
```

---

## 🎯 Choosing the Right Approach

| Scenario | Single Genie Space | Multiple Genie Spaces |
|----------|-------------------|----------------------|
| All data in one database | ✅ Best | ❌ Overkill |
| Data across systems | ⚠️ Limited | ✅ Best |
| Security boundaries needed | ❌ Can't enforce | ✅ Best |
| Simple queries | ✅ Best | ❌ Overkill |
| Cross-functional insights | ⚠️ Limited | ✅ Best |
| Different team ownership | ❌ Conflicts | ✅ Best |

---

## 📚 Related Documentation

- **AI Integration Guide**: `ai_integration_guide.md`
- **Genie Setup**: `GENIE_SETUP.md`
- **Implementation Code**: `spiffit-ai-calculator/genie_workflow.py`

---

## 🚀 Getting Started

1. **Identify your use case** from the examples above
2. **Map your data sources** to appropriate Genie spaces
3. **Design your workflow** (sequential, parallel, or conditional)
4. **Implement using Option 3** (Agent Pattern) from the integration guide
5. **Test with sample queries** to refine the flow

---

**Ready to build multi-Genie workflows? See `ai_integration_guide.md` for implementation details!**

