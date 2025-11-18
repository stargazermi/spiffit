"""
Quick Start Template for Databricks AI Hackathon
Excel Automation with AI - Incentive Compensation

Run this in a Databricks notebook to get started!
"""

# ============================================================================
# STEP 1: Load Excel Data to Delta Tables
# ============================================================================

import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Load the Excel files
ae_ethernet_file = "/dbfs/mnt/data/AE Ethernet Incentive Data.xlsx"
voice_incentive_file = "/dbfs/mnt/data/Voice_Incentive_data.xlsx"

# Read all sheets from AE Ethernet file
ae_sheet1 = pd.read_excel(ae_ethernet_file, sheet_name='AE Ethernet Incentive Data 1')
ae_sheet2 = pd.read_excel(ae_ethernet_file, sheet_name='AE Ethernet Incentive Data 2')
ae_sheet3 = pd.read_excel(ae_ethernet_file, sheet_name='AE Ethernet Incentive Data 3')

# Read Voice Incentive sheets
voice_sheet1 = pd.read_excel(voice_incentive_file, sheet_name='Voice Act. Incentive Data 1')
voice_sheet3 = pd.read_excel(voice_incentive_file, sheet_name='Voice Act. Incentive Data 3')

# Convert to Spark DataFrames and save as Delta tables
spark.createDataFrame(ae_sheet1).write.format("delta").mode("overwrite").saveAsTable("incentive.ae_performance")
spark.createDataFrame(ae_sheet2).write.format("delta").mode("overwrite").saveAsTable("incentive.ae_opportunities")
spark.createDataFrame(ae_sheet3).write.format("delta").mode("overwrite").saveAsTable("incentive.ae_detailed")
spark.createDataFrame(voice_sheet1).write.format("delta").mode("overwrite").saveAsTable("incentive.voice_performance")
spark.createDataFrame(voice_sheet3).write.format("delta").mode("overwrite").saveAsTable("incentive.voice_orders")

print("✅ All data loaded to Delta tables!")

# ============================================================================
# STEP 2: Basic AI Query Example
# ============================================================================

# Example 1: Use AI to analyze performance trends
sql_query = """
SELECT 
  AE,
  MRR_Attainment,
  TCV_Attainment,
  SPF,
  ai_analyze(
    'summarize',
    CONCAT(
      'AE: ', AE, 
      ', MRR Attainment: ', MRR_Attainment,
      ', TCV Attainment: ', TCV_Attainment,
      ', SPF: ', SPF
    )
  ) as performance_summary
FROM incentive.ae_performance
WHERE SPF > 100000
"""

# df = spark.sql(sql_query)
# display(df)

# ============================================================================
# STEP 3: LangChain Agent Setup
# ============================================================================

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_community.llms import Databricks

# Connect to your Databricks SQL warehouse
db = SQLDatabase.from_databricks(
    catalog="hive_metastore",
    schema="incentive"
)

# Use Databricks hosted LLM
llm = Databricks(
    endpoint_name="databricks-meta-llama-3-1-405b-instruct"
)

# Create SQL Agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="openai-functions"
)

# Example usage
def ask_ai(question: str):
    """Ask AI anything about your incentive data"""
    return agent.run(question)

# Example questions to try:
questions = [
    "What's the average SPF for AEs with over 100% MRR attainment?",
    "Show me the top 5 AEs by total SPF payout",
    "Which region has the highest TCV attainment?",
    "Calculate the total payout for all AEs in the Northeast region",
    "Find all opportunities with MRR over $50,000"
]

# Uncomment to test:
# for q in questions:
#     print(f"\n❓ {q}")
#     print(f"💡 {ask_ai(q)}\n")

# ============================================================================
# STEP 4: AI-Powered Payout Calculator
# ============================================================================

def calculate_smart_payout(ae_name: str, scenario: dict = None):
    """
    AI-powered payout calculator with what-if scenario support
    
    Args:
        ae_name: Name of the AE
        scenario: Optional dict with hypothetical values
                  e.g., {"additional_mrr": 5000, "additional_tcv": 100000}
    """
    
    # Get current performance
    current_query = f"""
    SELECT 
        AE,
        MRR_Budget,
        MRR_Actual,
        TCV_Budget,
        TCV_Actual,
        Ethernet_Actual,
        Lit_Actual,
        SPF
    FROM incentive.ae_performance
    WHERE AE = '{ae_name}'
    """
    
    df = spark.sql(current_query).toPandas()
    
    if df.empty:
        return f"AE {ae_name} not found"
    
    row = df.iloc[0]
    
    # Apply scenario if provided
    if scenario:
        if 'additional_mrr' in scenario:
            row['MRR_Actual'] += scenario['additional_mrr']
        if 'additional_tcv' in scenario:
            row['TCV_Actual'] += scenario['additional_tcv']
    
    # Calculate new attainments
    mrr_attainment = (row['MRR_Actual'] / row['MRR_Budget']) * 100 if row['MRR_Budget'] > 0 else 0
    tcv_attainment = (row['TCV_Actual'] / row['TCV_Budget']) * 100 if row['TCV_Budget'] > 0 else 0
    
    # Use AI to explain the payout logic
    explanation_prompt = f"""
    Analyze this sales performance and explain the payout calculation:
    
    AE: {ae_name}
    MRR Attainment: {mrr_attainment:.1f}%
    TCV Attainment: {tcv_attainment:.1f}%
    Current SPF: ${row['SPF']:,.2f}
    
    Explain:
    1. Is this performance above or below expectations?
    2. What factors are driving the payout?
    3. What should the AE focus on to increase their payout?
    """
    
    # ai_explanation = ask_ai(explanation_prompt)
    
    return {
        'ae': ae_name,
        'current_spf': row['SPF'],
        'mrr_attainment': mrr_attainment,
        'tcv_attainment': tcv_attainment,
        # 'ai_insights': ai_explanation
    }

# Example usage:
# result = calculate_smart_payout('Sarah Johnson')
# print(result)

# What-if scenario:
# scenario_result = calculate_smart_payout(
#     'Sarah Johnson', 
#     scenario={'additional_mrr': 10000, 'additional_tcv': 250000}
# )

# ============================================================================
# STEP 5: Vector Search for Similar Deals (Advanced)
# ============================================================================

from databricks.vector_search.client import VectorSearchClient

def setup_vector_search():
    """
    Set up vector search for finding similar opportunities
    Based on notes, product names, and opportunity descriptions
    """
    
    vsc = VectorSearchClient()
    
    # Create vector search index
    vsc.create_endpoint(
        name="incentive_search_endpoint",
        endpoint_type="STANDARD"
    )
    
    # Index opportunity data
    vsc.create_index(
        endpoint_name="incentive_search_endpoint",
        index_name="incentive.opportunities_vector_index",
        primary_key="18_Digit_Opty_ID",
        source_table="incentive.ae_opportunities",
        embedding_model="bge-large-en",
        columns_to_index=["Opportunity_Name", "Product_Name"]
    )
    
    return vsc

def find_similar_deals(opportunity_description: str, top_k: int = 5):
    """
    Find similar opportunities using vector search
    """
    vsc = VectorSearchClient()
    
    results = vsc.similarity_search(
        index_name="incentive.opportunities_vector_index",
        query_text=opportunity_description,
        top_k=top_k
    )
    
    return results

# Example:
# similar = find_similar_deals("Enterprise cloud migration with AI/ML components", top_k=5)

# ============================================================================
# STEP 6: Genie Setup (Manual - Do this in UI)
# ============================================================================

"""
To set up Genie:

1. Go to Databricks UI > Data Intelligence Platform > Genie
2. Create new Genie space called "Incentive Analyzer"
3. Add these tables:
   - incentive.ae_performance
   - incentive.ae_opportunities
   - incentive.ae_detailed
   - incentive.voice_performance
   - incentive.voice_orders

4. Add sample questions:
   - "What's the total SPF for all AEs?"
   - "Show me AEs with over 100% attainment"
   - "Which region has the best performance?"
   - "List all opportunities over $100k MRR"
   - "What's the average payout by region?"

5. Test natural language queries!
"""

# ============================================================================
# STEP 7: Build Databricks App (Streamlit)
# ============================================================================

"""
Create a new Python file: cursor/incentive_app.py

Then run in terminal:
  databricks apps deploy incentive_app.py --name "AI Incentive Calculator"
"""

# See cursor/incentive_app.py for the full app code

# ============================================================================
# SAMPLE DEMO FLOW
# ============================================================================

def run_demo():
    """
    Complete demo workflow showing AI capabilities
    """
    
    print("🎬 DEMO: AI-Powered Incentive Automation\n")
    
    # Demo 1: Natural language query
    print("=" * 60)
    print("DEMO 1: Ask AI About Performance")
    print("=" * 60)
    question = "Which AEs are at risk of missing their quota?"
    print(f"❓ Question: {question}")
    # answer = ask_ai(question)
    # print(f"💡 AI Answer: {answer}\n")
    
    # Demo 2: Payout calculation
    print("=" * 60)
    print("DEMO 2: Smart Payout Calculator")
    print("=" * 60)
    result = calculate_smart_payout('Sarah Johnson')
    print(f"Current Performance:")
    print(f"  SPF: ${result['current_spf']:,.2f}")
    print(f"  MRR Attainment: {result['mrr_attainment']:.1f}%")
    print(f"  TCV Attainment: {result['tcv_attainment']:.1f}%\n")
    
    # Demo 3: What-if scenario
    print("=" * 60)
    print("DEMO 3: What-If Analysis")
    print("=" * 60)
    print("What if Sarah closes 2 more deals worth $10k MRR and $250k TCV?")
    scenario = calculate_smart_payout(
        'Sarah Johnson',
        scenario={'additional_mrr': 10000, 'additional_tcv': 250000}
    )
    print(f"Projected SPF: ${scenario['current_spf']:,.2f}")
    print(f"New MRR Attainment: {scenario['mrr_attainment']:.1f}%")
    print(f"New TCV Attainment: {scenario['tcv_attainment']:.1f}%\n")
    
    print("🎉 Demo Complete! That's your AI-powered incentive system!\n")

# Uncomment to run demo:
# run_demo()

# ============================================================================
# TIPS FOR SUCCESS
# ============================================================================

"""
🎯 HACKATHON PRO TIPS:

1. **Start Simple**: Get basic AI query working first, then add features
2. **Focus on Wow Factor**: Show something impossible in Excel
3. **Practice Your Demo**: Smooth demo = win
4. **Handle Errors Gracefully**: Show how AI handles bad data
5. **Explain the "Why"**: Don't just show results, show AI reasoning

🚀 IMPLEMENTATION TIMELINE:

Hour 1: Load data, set up Delta tables
Hour 2: Get basic AI queries working
Hour 3: Build LangChain agent
Hour 4: Create Streamlit app
Hour 5: Polish UI and add visualizations
Hour 6: Practice demo, prepare slides

💡 DEMO FLOW:

1. Show Excel pain (5 min)
2. Upload data to your app (1 min)
3. Ask 3-4 impressive AI questions (5 min)
4. Show payout calculator with what-if (5 min)
5. Reveal the "wow" feature (vector search or auto-insights) (3 min)
6. Q&A (1 min)

Total: 20 min presentation

Good luck! 🍀
"""

print("✅ Template loaded! Read the comments and start building!")

