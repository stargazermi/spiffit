# Use Case #1: AI-Powered Incentive Calculator
## Implementation Plan

### 🎯 Goal
Replace manual Excel formulas with an AI that understands natural language questions and automatically calculates incentives.

---

## Architecture Overview

```
User Question (Natural Language)
        ↓
    Genie (NL Understanding)
        ↓
    LLM (Formula Interpretation)
        ↓
    Python/Spark (Calculation Engine)
        ↓
    Delta Lake (Data Source)
        ↓
    AI BI Dashboard (Results Visualization)
```

---

## Step-by-Step Implementation

### Step 1: Data Preparation (30 minutes)

**1.1 Upload Data to Databricks**
```python
# In Databricks Notebook
from pyspark.sql import SparkSession

# Read Excel files
ae_ethernet_df = spark.read.format("excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("/FileStore/tables/AE_Ethernet_Incentive_Data.xlsx")

voice_df = spark.read.format("excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("/FileStore/tables/Voice_Incentive_data.xlsx")

# Write to Delta Lake
ae_ethernet_df.write.format("delta").mode("overwrite").save("/delta/incentives/ae_ethernet")
voice_df.write.format("delta").mode("overwrite").save("/delta/incentives/voice")

# Create Delta tables
spark.sql("""
    CREATE TABLE incentives.ae_ethernet
    USING DELTA
    LOCATION '/delta/incentives/ae_ethernet'
""")
```

**1.2 Clean and Transform Data**
```python
# Convert attainment percentages to numeric
from pyspark.sql.functions import regexp_replace, col

ae_clean = spark.table("incentives.ae_ethernet") \
    .withColumn("mrr_attainment_pct", 
                regexp_replace(col("MRR Attainment"), "%", "").cast("float") / 100) \
    .withColumn("renewal_attainment_pct",
                regexp_replace(col("Renewal Attainment"), "%", "").cast("float") / 100) \
    .withColumn("tcv_attainment_pct",
                regexp_replace(col("TCV Attainment"), "%", "").cast("float") / 100)

# Save cleaned version
ae_clean.write.format("delta").mode("overwrite").saveAsTable("incentives.ae_ethernet_clean")
```

---

### Step 2: Build Calculation Engine (45 minutes)

**2.1 Define Incentive Calculation Logic**
```python
# incentive_calculator.py

class IncentiveCalculator:
    """
    Core logic for incentive calculations
    Replaces Excel formulas with Python functions
    """
    
    def __init__(self, ae_data, voice_data):
        self.ae_data = ae_data
        self.voice_data = voice_data
    
    def calculate_mrr_incentive(self, ae_name):
        """
        Calculate MRR-based incentive
        Excel equivalent: =IF(MRR_Attainment >= 1, Budget * 0.15, 0)
        """
        ae_record = self.ae_data.filter(col("AE") == ae_name).first()
        
        if ae_record is None:
            return {"error": f"AE {ae_name} not found"}
        
        attainment = ae_record["mrr_attainment_pct"]
        budget = ae_record["MRR Budget"]
        
        # Tiered incentive structure
        if attainment >= 1.2:  # 120%+ = 20% bonus
            payout = budget * 0.20
            tier = "Platinum"
        elif attainment >= 1.0:  # 100-119% = 15% bonus
            payout = budget * 0.15
            tier = "Gold"
        elif attainment >= 0.8:  # 80-99% = 10% bonus
            payout = budget * 0.10
            tier = "Silver"
        else:  # <80% = 5% bonus
            payout = budget * 0.05
            tier = "Bronze"
        
        return {
            "ae_name": ae_name,
            "mrr_budget": budget,
            "mrr_actual": ae_record["MRR Actual"],
            "attainment_pct": attainment * 100,
            "incentive_tier": tier,
            "payout": payout,
            "explanation": f"{ae_name} achieved {attainment*100:.1f}% MRR attainment, " +
                          f"qualifying for {tier} tier with ${payout:,.2f} incentive"
        }
    
    def calculate_total_incentive(self, ae_name):
        """
        Calculate total incentive across all categories
        """
        mrr_incentive = self.calculate_mrr_incentive(ae_name)
        renewal_incentive = self.calculate_renewal_incentive(ae_name)
        tcv_incentive = self.calculate_tcv_incentive(ae_name)
        ethernet_incentive = self.calculate_ethernet_incentive(ae_name)
        
        total = (mrr_incentive.get("payout", 0) + 
                renewal_incentive.get("payout", 0) +
                tcv_incentive.get("payout", 0) +
                ethernet_incentive.get("payout", 0))
        
        return {
            "ae_name": ae_name,
            "mrr_incentive": mrr_incentive.get("payout", 0),
            "renewal_incentive": renewal_incentive.get("payout", 0),
            "tcv_incentive": tcv_incentive.get("payout", 0),
            "ethernet_incentive": ethernet_incentive.get("payout", 0),
            "total_payout": total,
            "breakdown": {
                "mrr": mrr_incentive,
                "renewal": renewal_incentive,
                "tcv": tcv_incentive,
                "ethernet": ethernet_incentive
            }
        }
    
    def calculate_renewal_incentive(self, ae_name):
        # Similar structure to MRR
        pass
    
    def calculate_tcv_incentive(self, ae_name):
        # Similar structure to MRR
        pass
    
    def calculate_ethernet_incentive(self, ae_name):
        # Similar structure to MRR
        pass
```

**2.2 Test Calculations**
```python
# Test the calculator
calculator = IncentiveCalculator(
    ae_data=spark.table("incentives.ae_ethernet_clean"),
    voice_data=spark.table("incentives.voice")
)

# Test with a sample AE
result = calculator.calculate_mrr_incentive("John Smith")
print(result)
```

---

### Step 3: Add AI Natural Language Layer (45 minutes)

**3.1 Set Up Genie Integration**
```python
# genie_interface.py
from databricks.genie import GenieClient

class IncentiveGenieBot:
    """
    Natural language interface to incentive calculations
    """
    
    def __init__(self, calculator):
        self.calculator = calculator
        self.genie = GenieClient()
        
    def process_question(self, question):
        """
        Process natural language questions about incentives
        
        Examples:
        - "What's my Q4 incentive?"
        - "How much will John Smith earn this month?"
        - "Show me top earners in the Northeast region"
        - "What's my attainment for MRR?"
        """
        
        # Use LLM to extract intent and parameters
        intent = self.extract_intent(question)
        
        if intent["type"] == "individual_incentive":
            return self.calculator.calculate_total_incentive(intent["ae_name"])
        
        elif intent["type"] == "attainment_check":
            return self.calculator.get_attainment(intent["ae_name"], intent["metric"])
        
        elif intent["type"] == "top_performers":
            return self.calculator.get_top_performers(intent.get("region"), intent.get("limit", 10))
        
        elif intent["type"] == "projection":
            return self.calculator.project_incentive(intent["ae_name"], intent["scenario"])
        
        else:
            return {"error": "I don't understand that question. Try asking about incentives, attainment, or rankings."}
    
    def extract_intent(self, question):
        """
        Use LLM to understand the question intent
        """
        prompt = f"""
        Analyze this question about sales incentives and extract:
        1. Question type (individual_incentive, attainment_check, top_performers, projection)
        2. Person's name (if mentioned)
        3. Metric (MRR, TCV, Renewal, etc.)
        4. Time period (if mentioned)
        5. Region (if mentioned)
        
        Question: {question}
        
        Return as JSON.
        """
        
        # Call Databricks LLM
        response = self.genie.query(prompt, model="gemini-2.5")
        return response
```

**3.2 Create Conversational Interface**
```python
# chatbot.py
from databricks.sdk import WorkspaceClient

class IncentiveChatbot:
    """
    Full conversational AI for incentive questions
    """
    
    def __init__(self, genie_bot):
        self.genie_bot = genie_bot
        self.conversation_history = []
    
    def chat(self, user_message):
        """
        Handle multi-turn conversations
        """
        # Add context from previous messages
        context = "\n".join([f"User: {m['user']}\nBot: {m['bot']}" 
                            for m in self.conversation_history[-3:]])
        
        # Process with context
        response = self.genie_bot.process_question(user_message)
        
        # Store in history
        self.conversation_history.append({
            "user": user_message,
            "bot": response
        })
        
        # Generate natural language response
        natural_response = self.format_response(response)
        
        return natural_response
    
    def format_response(self, data):
        """
        Convert calculation results to natural language
        """
        if "error" in data:
            return data["error"]
        
        if "total_payout" in data:
            response = f"""
            Great news! Here's the incentive breakdown for {data['ae_name']}:
            
            💰 Total Payout: ${data['total_payout']:,.2f}
            
            Breakdown:
            • MRR Incentive: ${data['mrr_incentive']:,.2f}
            • Renewal Incentive: ${data['renewal_incentive']:,.2f}
            • TCV Incentive: ${data['tcv_incentive']:,.2f}
            • Ethernet Incentive: ${data['ethernet_incentive']:,.2f}
            
            {data['breakdown']['mrr']['explanation']}
            """
            return response
        
        return str(data)
```

---

### Step 4: Build UI with Databricks App (30 minutes)

**4.1 Create Streamlit App**
```python
# app.py
import streamlit as st
from incentive_calculator import IncentiveCalculator
from genie_interface import IncentiveGenieBot
from chatbot import IncentiveChatbot

st.title("🤖 AI Incentive Calculator")
st.caption("Ask me anything about your incentives in plain English!")

# Initialize components
@st.cache_resource
def init_components():
    calculator = IncentiveCalculator(
        ae_data=spark.table("incentives.ae_ethernet_clean"),
        voice_data=spark.table("incentives.voice")
    )
    genie_bot = IncentiveGenieBot(calculator)
    chatbot = IncentiveChatbot(genie_bot)
    return chatbot

chatbot = init_components()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about incentives..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get bot response
    response = chatbot.chat(prompt)
    
    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with example questions
st.sidebar.header("Example Questions")
st.sidebar.markdown("""
- What's my total incentive this quarter?
- How am I tracking against my MRR budget?
- Show me the top 10 performers
- What would my payout be if I close $50K more?
- Which region has the highest attainment?
""")
```

---

### Step 5: Add Validation & Insights (30 minutes)

**5.1 Add Anomaly Detection**
```python
# validation.py
from databricks.automl import classify

class IncentiveValidator:
    """
    Validate data quality and detect anomalies
    """
    
    def validate_incentive_calculation(self, ae_name, calculated_result):
        """
        Check if calculation seems reasonable
        """
        warnings = []
        
        # Check for unusual attainment
        if calculated_result["attainment_pct"] > 150:
            warnings.append("⚠️ Attainment over 150% - please verify data")
        
        # Check for missing data
        if calculated_result.get("mrr_actual") == 0:
            warnings.append("⚠️ Zero MRR Actual - possible data entry error")
        
        # Check against historical average
        historical_avg = self.get_historical_average(ae_name)
        if calculated_result["total_payout"] > historical_avg * 2:
            warnings.append(f"⚠️ Payout is 2x higher than historical average (${historical_avg:,.2f})")
        
        return warnings
    
    def get_historical_average(self, ae_name):
        # Query historical incentive data
        pass
```

---

## Demo Script

### The "Excel Way" (Show First)
1. Open Excel file
2. Scroll through multiple sheets
3. Find employee row
4. Look at formulas (zoom in to show complexity)
5. Manually calculate across 4-5 columns
6. Copy-paste to PowerPoint for reporting
7. **Time elapsed: 5-10 minutes for ONE person**

### The "AI Way" (Show Second)
1. Open Databricks App
2. Type: "What's John Smith's total incentive this quarter?"
3. Get instant response with:
   - Total payout
   - Breakdown by category
   - Attainment levels
   - Natural language explanation
4. Ask follow-up: "What if he closes $50K more?"
5. Get instant projection
6. **Time elapsed: 30 seconds**

### Impact Statement
> "We just reduced incentive calculation time from 10 minutes per person to 30 seconds.
> For a sales org of 200 people, that's 33 hours per month → **$10,000+ in cost savings**
> Plus elimination of calculation errors that could cost $50,000+ in mispaid incentives."

---

## Next Steps After Hackathon

1. **Add More Calculation Rules**
   - Territory multipliers
   - New product bonuses
   - Team performance accelerators

2. **Integration with Source Systems**
   - Pull live from Salesforce
   - Connect to HR system for employee data
   - Real-time updates

3. **Advanced Analytics**
   - Predict quarter-end attainment
   - Recommend actions to hit targets
   - Identify at-risk AEs

4. **Governance & Audit**
   - Calculation versioning
   - Approval workflows
   - Audit trail

---

## Success Criteria

- [ ] Data loaded into Delta Lake
- [ ] 3+ calculation formulas working
- [ ] Natural language queries working
- [ ] UI deployed and demo-ready
- [ ] "Before/After" comparison prepared
- [ ] Cost/time savings calculated
- [ ] 5-minute pitch rehearsed

