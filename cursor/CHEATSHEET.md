# 🚀 Databricks AI Hackathon - Quick Reference Cheat Sheet

## 📋 Table of Contents
1. [Data Loading](#data-loading)
2. [AI Functions](#ai-functions)
3. [LangChain Setup](#langchain-setup)
4. [Genie Commands](#genie-commands)
5. [Vector Search](#vector-search)
6. [Common SQL Patterns](#common-sql-patterns)
7. [Troubleshooting](#troubleshooting)

---

## 📊 Data Loading

### Load Excel to Delta Table
```python
import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Method 1: Via Pandas
df_pandas = pd.read_excel("/dbfs/mnt/data/your_file.xlsx", sheet_name="Sheet1")
df_spark = spark.createDataFrame(df_pandas)
df_spark.write.format("delta").mode("overwrite").saveAsTable("catalog.schema.table_name")

# Method 2: Direct with Spark (if available)
df = spark.read.format("excel") \
    .option("header", "true") \
    .option("sheetName", "Sheet1") \
    .load("/dbfs/mnt/data/your_file.xlsx")
df.write.format("delta").saveAsTable("catalog.schema.table_name")
```

### Upload Files to DBFS
```python
# In notebook
dbutils.fs.cp("file:/local/path/file.xlsx", "dbfs:/mnt/data/file.xlsx")

# List files
dbutils.fs.ls("dbfs:/mnt/data/")
```

---

## 🤖 AI Functions

### ai_query() - Ask questions about data
```sql
SELECT 
  AE,
  MRR_Attainment,
  ai_query(
    'databricks-meta-llama-3-1-70b-instruct',
    CONCAT('Analyze this performance: MRR at ', MRR_Attainment, '%. Is this good or bad?')
  ) as ai_analysis
FROM incentive.ae_performance
```

### ai_analyze() - Summarize or classify
```sql
SELECT 
  Opportunity_Name,
  ai_analyze(
    'summarize',
    CONCAT('Deal: ', Opportunity_Name, ' for ', TCV, ' over ', Contract_Length, ' years')
  ) as deal_summary
FROM incentive.opportunities
```

### ai_classify() - Categorize data
```sql
SELECT 
  Notes,
  ai_classify(
    Notes,
    ARRAY('At Risk', 'On Track', 'Exceeding'),
    STRUCT('instruction' AS 'Classify this AE performance based on the notes')
  ) as risk_category
FROM incentive.ae_performance
WHERE Notes IS NOT NULL
```

### ai_similarity() - Find similar text
```sql
SELECT 
  a.Opportunity_Name as query_opp,
  b.Opportunity_Name as similar_opp,
  ai_similarity(a.Opportunity_Name, b.Opportunity_Name) as similarity_score
FROM incentive.opportunities a
CROSS JOIN incentive.opportunities b
WHERE a.Opportunity_ID != b.Opportunity_ID
  AND ai_similarity(a.Opportunity_Name, b.Opportunity_Name) > 0.8
ORDER BY similarity_score DESC
LIMIT 10
```

---

## 🦜 LangChain Setup

### Basic LangChain Agent
```python
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_community.llms import Databricks

# Connect to database
db = SQLDatabase.from_databricks(
    catalog="hive_metastore",
    schema="incentive"
)

# Set up LLM
llm = Databricks(
    endpoint_name="databricks-meta-llama-3-1-405b-instruct"
)

# Create agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

# Use agent
answer = agent.run("What's the average SPF for AEs above quota?")
print(answer)
```

### Custom Prompt Template
```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["question", "schema"],
    template="""
You are an expert in sales compensation analysis.

Database Schema:
{schema}

Question: {question}

Provide a SQL query and explain your reasoning.
"""
)

formatted_prompt = prompt.format(
    question="Which AEs should get bonuses?",
    schema="ae_performance(AE, MRR_Attainment, SPF)"
)
```

---

## 💬 Genie Commands

### Set up Genie Space (UI)
1. Go to Databricks workspace
2. Click "Genie" in left sidebar
3. Create new space: "Incentive Analysis"
4. Add tables:
   - `incentive.ae_performance`
   - `incentive.ae_opportunities`
   - etc.

### Sample Genie Questions
```
Natural Language -> Genie Auto-generates SQL

"What's the total SPF for all AEs?"
"Show me AEs with MRR attainment over 100%"
"Which region has the highest average TCV?"
"List top 5 opportunities by MRR"
"Compare performance between Northeast and South regions"
"Show monthly trend of closed deals"
"Which products have the highest win rate?"
```

### Genie API (Python)
```python
from databricks import genie

# Create client
client = genie.Client()

# Ask question
response = client.query(
    space_id="your_space_id",
    question="What's the average SPF for AEs above quota?"
)

print(response.answer)
print(response.sql)  # See generated SQL
```

---

## 🔍 Vector Search

### Create Vector Search Index
```python
from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

# Create endpoint
vsc.create_endpoint(
    name="incentive_search",
    endpoint_type="STANDARD"
)

# Create index
vsc.create_index(
    endpoint_name="incentive_search",
    index_name="incentive.opportunities_index",
    primary_key="Opportunity_ID",
    source_table="incentive.ae_opportunities",
    embedding_model="bge-large-en",
    columns_to_index=["Opportunity_Name", "Product_Name", "Notes"]
)
```

### Search with Vector Index
```python
# Semantic search
results = vsc.similarity_search(
    index_name="incentive.opportunities_index",
    query_text="cloud migration with AI components",
    top_k=5
)

# Hybrid search (vector + filters)
results = vsc.similarity_search(
    index_name="incentive.opportunities_index",
    query_text="enterprise deals",
    top_k=10,
    filters={"TCV": {"$gt": 500000}}
)
```

---

## 📊 Common SQL Patterns

### Calculate Attainment
```sql
SELECT 
  AE,
  MRR_Actual,
  MRR_Budget,
  ROUND((MRR_Actual / NULLIF(MRR_Budget, 0)) * 100, 2) as MRR_Attainment_Pct,
  CASE 
    WHEN (MRR_Actual / NULLIF(MRR_Budget, 0)) >= 1.0 THEN 'At or Above Quota'
    WHEN (MRR_Actual / NULLIF(MRR_Budget, 0)) >= 0.8 THEN 'Near Quota'
    ELSE 'Below Quota'
  END as Performance_Category
FROM incentive.ae_performance
```

### Aggregate by Region
```sql
SELECT 
  Region,
  COUNT(DISTINCT AE) as AE_Count,
  SUM(MRR_Actual) as Total_MRR,
  AVG(MRR_Attainment) as Avg_Attainment,
  SUM(SPF) as Total_SPF
FROM incentive.ae_performance
GROUP BY Region
ORDER BY Total_SPF DESC
```

### Join Multiple Tables
```sql
SELECT 
  p.AE,
  p.Region,
  p.SPF,
  COUNT(o.Opportunity_ID) as Deal_Count,
  SUM(o.TCV) as Total_Deal_Value
FROM incentive.ae_performance p
LEFT JOIN incentive.ae_opportunities o
  ON p.AE = o.Opportunity_Owner
GROUP BY p.AE, p.Region, p.SPF
```

### Window Functions (Rank AEs)
```sql
SELECT 
  AE,
  Region,
  SPF,
  RANK() OVER (PARTITION BY Region ORDER BY SPF DESC) as Region_Rank,
  RANK() OVER (ORDER BY SPF DESC) as Overall_Rank
FROM incentive.ae_performance
```

### Time-based Analysis
```sql
SELECT 
  DATE_TRUNC('month', Close_Date) as Close_Month,
  COUNT(*) as Deal_Count,
  SUM(TCV) as Total_TCV,
  AVG(TCV) as Avg_Deal_Size
FROM incentive.ae_opportunities
WHERE Close_Date >= DATE_SUB(CURRENT_DATE(), 90)
GROUP BY DATE_TRUNC('month', Close_Date)
ORDER BY Close_Month
```

---

## 🎨 Streamlit App Commands

### Run Locally
```bash
streamlit run cursor/incentive_app.py
```

### Deploy to Databricks
```bash
# Install CLI
pip install databricks-cli

# Configure
databricks configure --token

# Deploy
databricks apps deploy cursor/incentive_app.py --name "AI Incentive Calculator"
```

### Common Streamlit Patterns

#### File Upload
```python
uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
```

#### Metrics Display
```python
col1, col2, col3 = st.columns(3)
col1.metric("Total SPF", f"${total:,.2f}", delta=f"+${delta:,.2f}")
col2.metric("Avg Attainment", f"{avg:.1f}%")
col3.metric("Top Performer", top_ae)
```

#### Charts with Plotly
```python
import plotly.express as px

fig = px.bar(df, x='AE', y='SPF', color='Region')
st.plotly_chart(fig, use_container_width=True)
```

#### Chat Interface
```python
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = ask_ai(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

---

## 🔧 Troubleshooting

### Issue: Can't connect to Databricks
```python
# Check workspace URL and token
import os
os.environ['DATABRICKS_HOST'] = 'https://your-workspace.databricks.com'
os.environ['DATABRICKS_TOKEN'] = 'your-token'

# Test connection
from databricks import sql
connection = sql.connect(
    server_hostname="your-workspace.databricks.com",
    http_path="/sql/1.0/warehouses/your-warehouse-id",
    access_token="your-token"
)
```

### Issue: AI Functions not available
```sql
-- Check if AI functions are enabled
SHOW FUNCTIONS LIKE 'ai_%';

-- If empty, contact admin to enable:
-- Workspace Settings > AI/ML > Enable AI Functions
```

### Issue: Out of memory
```python
# Process in chunks
chunk_size = 1000
for chunk in pd.read_excel(file_path, chunksize=chunk_size):
    spark.createDataFrame(chunk).write.format("delta").mode("append").saveAsTable("table")
```

### Issue: Slow queries
```sql
-- Add indexes
CREATE INDEX idx_ae ON incentive.ae_performance(AE);

-- Use OPTIMIZE
OPTIMIZE incentive.ae_performance;

-- Check query plan
EXPLAIN SELECT * FROM incentive.ae_performance WHERE AE = 'Sarah';
```

---

## 💡 Pro Tips

### 1. Use Caching
```python
@st.cache_data
def load_data():
    return spark.sql("SELECT * FROM incentive.ae_performance").toPandas()
```

### 2. Handle Nulls
```sql
SELECT 
  AE,
  COALESCE(MRR_Actual, 0) as MRR_Actual,
  COALESCE(Notes, 'No notes') as Notes
FROM incentive.ae_performance
```

### 3. Format Numbers
```python
# In Python
f"${amount:,.2f}"  # $1,234.56
f"{percent:.1f}%"  # 98.5%

# In SQL
SELECT FORMAT_NUMBER(SPF, 2) as SPF_Formatted
```

### 4. Error Handling
```python
try:
    result = ask_ai(question)
except Exception as e:
    st.error(f"Error: {str(e)}")
    result = "Unable to process question. Please try rephrasing."
```

### 5. Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Processing query: {question}")
```

---

## 🎯 Quick Command Reference

| Task | Command |
|------|---------|
| Create table | `df.write.format("delta").saveAsTable("table")` |
| Query table | `spark.sql("SELECT * FROM table")` |
| AI query | `ai_query('model', 'prompt')` |
| Vector search | `vsc.similarity_search(index, query)` |
| Deploy app | `databricks apps deploy app.py` |
| Run locally | `streamlit run app.py` |

---

## 📚 Useful Links

- [Databricks SQL Reference](https://docs.databricks.com/sql/language-manual/)
- [AI Functions Docs](https://docs.databricks.com/sql/language-manual/sql-ref-functions-ai.html)
- [LangChain Docs](https://python.langchain.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Docs](https://plotly.com/python/)

---

**Keep this file open during the hackathon for quick copy/paste! 🚀**

