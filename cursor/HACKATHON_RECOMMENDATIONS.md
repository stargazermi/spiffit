# Hackathon: Excel Automation with Databricks AI
## Project Analysis & Recommendations

---

## 📊 Data Overview

### AE Ethernet Incentive Data (3 sheets, 650 total rows)
**Sheet 1:** Performance Dashboard (200 rows)
- Team performance metrics: MRR, TCV, Renewals, Ethernet, Lit Building counts
- Attainment calculations and SPF (Sales Performance Fund) payouts
- Leader/AE/Region hierarchy

**Sheet 2:** Opportunity Details (300 rows)
- Individual opportunity tracking
- Product-level sales data
- Manager and RVP assignments

**Sheet 3:** Detailed Opportunity Data (150 rows)
- Lit building counts per opportunity
- Product IDs and quantities
- Enhanced opportunity metadata

### Voice Incentive Data (2 sheets, 1,496 total rows)
**Sheet 1:** Performance & Payouts (500 rows)
- Sales stage tracking
- MRR and TCV metrics
- Calculated payouts (positive and negative)
- Order counts and stages

**Sheet 2:** Order Details (996 rows)
- Order-level granular data
- Stage ownership tracking
- Order start dates

---

## 🎯 What Users Currently Do in Excel (Pain Points)

1. **Manual Calculations**
   - Attainment % (Actual / Budget × 100)
   - SPF payouts based on complex rules
   - Aggregations across multiple sheets
   
2. **Data Consolidation**
   - Joining data across 5 different sheets
   - Matching opportunities to users/managers
   - Rolling up individual deals to team performance

3. **Reporting**
   - Creating pivot tables
   - Generating manager/RVP reports
   - Tracking changes over time

4. **Data Quality**
   - Finding missing values
   - Validating CRIS IDs and Opportunity IDs
   - Checking for duplicate entries

5. **What-If Analysis**
   - "What if I close this deal? What's my payout?"
   - Forecasting end-of-quarter performance
   - Budget reallocation scenarios

---

## 🚀 Recommended Databricks AI Solutions

### **OPTION 1: Genie AI Assistant (⭐ BEST FOR HACKATHON)**
**Why:** Natural language interface - users ask questions, get answers instantly

**Implementation:**
```python
# Users can ask questions like:
"What's the total SPF for Sarah Johnson's team?"
"Show me all deals over $100k MRR in the Northeast region"
"Which AEs are below 80% attainment?"
"Calculate my payout if I close opportunity PROD-10851"
```

**Pros:**
- ✅ No code required for end users
- ✅ Instant insights from natural language
- ✅ Built-in visualization
- ✅ Perfect for exploratory analysis

**Setup Time:** 2-4 hours (load data to Delta tables, configure Genie space)

---

### **OPTION 2: AI Functions + Databricks Apps**
**Why:** Build a custom web app that feels like Excel but with AI superpowers

**Implementation:**
```sql
-- Use AI functions for complex logic
SELECT 
  AE,
  MRR_Actual,
  ai_analyze('explain', 
    CONCAT('Analyze this performance: ', MRR_Actual, ' vs budget ', MRR_Budget)
  ) as performance_insight,
  ai_query('performance_model', 
    STRUCT(MRR_Actual, TCV_Actual, Ethernet_Actual)
  ) as predicted_payout
FROM incentive_data
```

**Build a Streamlit/Databricks App:**
- Upload Excel files → Auto-process
- Interactive dashboards
- "Ask AI" button for any calculation
- Export results back to Excel

**Pros:**
- ✅ Custom UI tailored to your workflow
- ✅ AI-powered insights embedded in the app
- ✅ Can handle file uploads
- ✅ Great demo factor

**Setup Time:** 4-8 hours

---

### **OPTION 3: LangChain + GPT-4 (Hosted LLMs)**
**Why:** Build an AI agent that understands incentive compensation rules

**Implementation:**
```python
from langchain import LLMChain
from databricks import sql

# Create an AI agent that knows your incentive rules
agent = create_sql_agent(
    llm=Databricks_LLM("databricks-meta-llama-3-1-405b-instruct"),
    db=databricks_connection,
    agent_type="openai-functions",
    verbose=True
)

# Users interact naturally
result = agent.run("""
    Calculate the SPF payout for all AEs where:
    - MRR Attainment > 100%
    - TCV Attainment > 85%
    - Ethernet Attainment > 90%
    Use the standard payout formula: 
    Base SPF × (0.4 × MRR + 0.3 × TCV + 0.3 × Ethernet)
""")
```

**Pros:**
- ✅ Understands complex business logic in natural language
- ✅ Can explain its reasoning
- ✅ Adapts to new rules without code changes
- ✅ Most impressive AI showcase

**Setup Time:** 6-10 hours

---

### **OPTION 4: Mosaic AI + Vector Search**
**Why:** Enable semantic search across all historical incentive data

**Implementation:**
```python
# Index all notes, deal descriptions, product names
vector_index = create_vector_search_index(
    table="incentive_history",
    text_columns=["Notes", "Opportunity_Name", "Product_Name"],
    embedding_model="bge-large-en"
)

# Users search naturally
results = vector_index.search(
    "Find all deals with contract renewals that had issues",
    top_k=10
)
```

**Use Case:** "Show me similar deals to this one" or "Find all deals with [specific characteristic]"

**Pros:**
- ✅ Find patterns in unstructured data (Notes fields)
- ✅ Similarity-based recommendations
- ✅ Works great with historical data

**Setup Time:** 3-5 hours

---

## 🏆 **HACKATHON WINNING STRATEGY**

### **Recommended Approach: Hybrid Solution**
Combine multiple AI features for maximum impact:

#### **Phase 1: Data Foundation (30 min)**
1. Load Excel files to Delta tables
2. Create basic transformations
3. Set up Unity Catalog

#### **Phase 2: Genie Setup (1 hour)**
1. Create Genie space with all tables
2. Add sample questions
3. Demo natural language queries

#### **Phase 3: AI-Powered App (3-4 hours)**
Build a Databricks App with:
- **File Upload**: Drag & drop Excel files
- **AI Chat Interface**: Ask questions about your data
- **Smart Calculations**: AI determines the right formula
- **Visualization**: Auto-generate charts
- **Export**: Download results to Excel

#### **Phase 4: Advanced AI (2-3 hours)**
- Implement `ai_analyze()` for performance insights
- Use GPT-4 via Hosted LLMs for complex what-if scenarios
- Add vector search for similar deal recommendations

---

## 💡 Demo Script Ideas

### **Demo 1: The "Excel Whisperer"**
1. Show messy Excel workflow (multiple sheets, manual formulas)
2. Upload to your app
3. Ask: "Which AEs are trending to miss their targets?"
4. AI instantly analyzes and highlights at-risk performers
5. Ask: "What deals should they focus on to hit target?"
6. AI recommends top opportunities based on historical close rates

### **Demo 2: The "Payout Calculator"**
1. Manager asks: "What's my team's total payout this quarter?"
2. AI calculates across all sheets, applying complex rules
3. Drill down: "Show me the breakdown by AE"
4. Explain: "Why is John's payout higher than Mary's?"
5. AI explains the performance differences

### **Demo 3: The "Forecaster"**
1. "What's my projected SPF if I close my top 3 deals?"
2. AI runs scenario analysis
3. "What if one of them slips to next quarter?"
4. AI recalculates instantly
5. Show confidence intervals and recommendations

---

## 🛠️ Quick Start Implementation

### **Option A: Fastest Path to Demo (Genie)**
```sql
-- 1. Create Delta tables (run this notebook)
CREATE TABLE incentive_performance AS
SELECT * FROM read_files(
  'dbfs:/mnt/data/AE_Ethernet_Incentive_Data.xlsx',
  format => 'excel',
  sheetName => 'AE Ethernet Incentive Data 1'
);

-- 2. Enable Genie on this table

-- 3. Start asking questions!
```

### **Option B: Most Impressive Demo (LangChain + App)**
```python
# cursor/app.py
import streamlit as st
from databricks import sql
from langchain_community.llms import Databricks

st.title("💰 AI Incentive Calculator")

uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
question = st.text_input("Ask anything about your incentive data...")

if question:
    # Use AI to answer
    answer = ai_agent.run(question)
    st.write(answer)
    
    # Show visualization
    st.plotly_chart(auto_viz(answer.data))
```

---

## 📋 Hackathon Checklist

- [ ] Load test data to Databricks workspace
- [ ] Create Delta tables from Excel files
- [ ] Set up Genie space
- [ ] Test AI functions (ai_query, ai_analyze)
- [ ] Build Databricks App skeleton
- [ ] Integrate LangChain agent
- [ ] Create demo scenarios
- [ ] Prepare presentation slides
- [ ] Practice demo (2-3 times)

---

## 🎪 Judging Criteria Alignment

| Criteria | How This Project Delivers |
|----------|---------------------------|
| **Innovation** | First AI-native incentive calculator, replaces 40-year-old Excel workflow |
| **Technical Complexity** | Multi-modal AI: NLP, SQL generation, predictive analytics, vector search |
| **Business Impact** | Saves 10+ hours/week per sales ops person, reduces errors, faster insights |
| **Usability** | Natural language interface - anyone can use it |
| **Scalability** | Handles unlimited data, real-time updates, works for entire sales org |

---

## 🚨 Common Pitfalls to Avoid

1. **Don't:** Try to replicate every Excel formula
   **Do:** Focus on the 3-5 most painful manual tasks

2. **Don't:** Build a basic dashboard (boring!)
   **Do:** Showcase AI answering questions humans ask

3. **Don't:** Over-engineer the data model
   **Do:** Keep it simple, focus on the AI layer

4. **Don't:** Demo with perfect data
   **Do:** Show AI handling messy real-world data

---

## 📚 Key Databricks Features to Use

- ✅ **Delta Lake** - Reliable data storage
- ✅ **Genie** - Natural language SQL
- ✅ **AI Functions** - `ai_query()`, `ai_analyze()`, `ai_classify()`
- ✅ **Hosted LLMs** - GPT-4, Claude, Llama
- ✅ **MLFlow** - Model tracking (if you build ML models)
- ✅ **Databricks Apps** - Web interface
- ✅ **Vector Search** - Semantic search
- ✅ **Unity Catalog** - Data governance

---

## 🎯 Success Metrics for Your Demo

- Can answer 10 common questions in <5 seconds each
- Handles malformed data gracefully
- Explains its reasoning (not a black box)
- Provides actionable insights, not just numbers
- Wow factor: something impossible in Excel

---

Good luck! 🚀 You've got a killer use case here - incentive compensation is PAINFUL in Excel and ripe for AI disruption.

