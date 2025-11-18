# Quick Guide: Create Mock Genie Spaces for Demo

## 🎯 Goal
Create 3 Genie spaces with mock data to demonstrate smart routing and AI reasoning.

---

## 📋 Spaces to Create

1. **spg-mocking-bird-sales** - Sales performance data
2. **spg-mocking-bird-analytics** - SPIFF winners and analysis
3. **spg-mocking-bird-market** - Competitor intelligence

---

## ⚠️ IMPORTANT: Create Data FIRST!

**Genie spaces require data to connect when you create them.**

You must run SQL scripts to create sample data **BEFORE** creating Genie spaces.

---

## 🗄️ STEP 1: Create Mock Data Tables

### Run the SQL Scripts

All SQL scripts are in `sql/` directory (root level).

**Quick Setup (5 minutes):**

1. Go to **SQL Editor** in Databricks workspace
2. Run each script in order:
   - `01_create_spg_demo_schema.sql` - Verify `hackathon` schema access
   - `02_create_sales_performance_table.sql` - Sales data
   - `03_create_spiff_winners_table.sql` - Analytics data  
   - `04_create_competitor_spiffs_table.sql` - Market data

3. Verify tables created:
```sql
SHOW TABLES IN hackathon.hackathon_spiffit LIKE '*';
-- Should show: sales_performance, spiff_winners, competitor_spiffs
```

📄 **See `sql/README.md` for detailed instructions and alternative methods**

---

## 🚀 STEP 2: Create Genie Spaces

### Step 2.1: Go to Genie in Databricks

1. Open your Databricks workspace: https://dbc-4ee5e339-1e79.cloud.databricks.com
2. Click **"Genie"** in the left sidebar
3. Click **"Create Space"** or **"New Space"**

---

### Step 2.2: Create Space 1 - Sales Data

**Space Configuration:**
- **Name:** `spg-mocking-bird-sales`
- **Description:** `Mock sales performance data for SPIFF agent demo - AE performance, deals, quotas`
- **SQL Warehouse:** Select any available warehouse

**Connect Your Data:**

When Genie asks "What data do you want to use?":
1. Click **"Add Tables"** or **"Connect Data"**
2. Search for: `hackathon.hackathon_spiffit.sales_performance`
3. Select the table and click **Add**

✅ **Data Source:** `sql/02_create_sales_performance_table.sql`

**Optional Instructions:**

You can add instructions to guide Genie's responses:

```
This space contains sales performance data. When asked:
- Calculate attainment % as (mrr_actual / mrr_quota) * 100
- Show top performers based on MRR
- Identify who exceeded quota
- Provide deal counts and new logo metrics
```

**Click "Create" to finish!**

---

### Step 2.3: Create Space 2 - Analytics

**Space Configuration:**
- **Name:** `spg-mocking-bird-analytics`
- **Description:** `Mock analytics data - SPIFF winners, leaderboards, trend analysis`
- **SQL Warehouse:** Same as above

**Connect Your Data:**

1. Click **"Add Tables"**
2. Search for: `hackathon.hackathon_spiffit.spiff_winners`
3. Select and add the table

✅ **Data Source:** `sql/03_create_spiff_winners_table.sql`

**Optional Instructions:**

```
This space tracks SPIFF winners and rankings. When asked:
- Show top earners by total amount
- List winners by program type
- Calculate total earnings per person
- Show rankings and leaderboards
```

**Click "Create"!**

---

### Step 2.4: Create Space 3 - Market Intelligence

**Space Configuration:**
- **Name:** `spg-mocking-bird-market`
- **Description:** `Mock competitor data and market intelligence for SPIFF planning`
- **SQL Warehouse:** Same as above

**Connect Your Data:**

1. Click **"Add Tables"**
2. Search for: `hackathon.hackathon_spiffit.competitor_spiffs`
3. Select and add the table

✅ **Data Source:** `sql/04_create_competitor_spiffs_table.sql`

**Optional Instructions:**

```
This space contains competitor SPIFF programs. When asked:
- Compare our SPIFFs vs competitor offers
- Show highest paying competitor programs
- Identify gaps in our incentive strategy
- Recommend competitive counters
```

**Click "Create"!**

---

## 🆔 STEP 3: Get Your Space IDs

After creating all 3 spaces, you need their Space IDs for the agent.

**Option 1: From Genie UI**
1. Go to each space
2. Look at the URL: `https://...databricks.com/genie/spaces/{space_id}`
3. Copy the `space_id` portion
4. Save it: 
   - Sales space → `GENIE_SALES_SPACE_ID`
   - Analytics space → `GENIE_ANALYTICS_SPACE_ID`
   - Market space → `GENIE_MARKET_SPACE_ID`

**Option 2: Via CLI**
```bash
databricks genie list-spaces --profile dlk-hackathon -o json | grep -i "spg-mocking-bird"
```

Look for the `space_id` field in each space object.

---

## 🧪 STEP 4: Test Each Space

Before using with the agent, verify each space works:

**Test Sales Space:**
- Go to `spg-mocking-bird-sales`
- Ask: "Who are the top performers?"
- Ask: "What's John Smith's attainment?"

**Test Analytics Space:**
- Go to `spg-mocking-bird-analytics`
- Ask: "Who won the most SPIFFs?"
- Ask: "Show me total earnings by person"

**Test Market Space:**
- Go to `spg-mocking-bird-market`
- Ask: "What are competitors offering?"
- Ask: "Show the highest paying programs"

---

## ⚙️ STEP 5: Configure Environment Variables

Update your local environment or Databricks App config:

**For Local Testing:**
```bash
# In your terminal
export GENIE_SALES_SPACE_ID="your-sales-space-id"
export GENIE_ANALYTICS_SPACE_ID="your-analytics-space-id"
export GENIE_MARKET_SPACE_ID="your-market-space-id"

# Then run the agent
cd streamlit/spiffit-ai-calculator
streamlit run spiff_agent_app.py --server.port 8000
```

**For Databricks Deployment:**

Update `app.yaml`:
```yaml
env:
  - name: GENIE_SALES_SPACE_ID
    value: "your-sales-space-id"
  - name: GENIE_ANALYTICS_SPACE_ID
    value: "your-analytics-space-id"
  - name: GENIE_MARKET_SPACE_ID
    value: "your-market-space-id"
```

---

## 🎯 STEP 6: Run the Agent

Now you're ready to test the autonomous SPIFF agent!

```bash
cd streamlit/spiffit-ai-calculator
streamlit run spiff_agent_app.py --server.port 8000
```

**Try these scenarios:**

1. **Manual Investigation (Mid-Month):**
   - Click "Run Investigation Now"
   - Watch it query all 3 spaces
   - Review recommendations

2. **View History:**
   - Check previous investigations
   - See how it routed queries
   - Review AI reasoning

3. **Configure Schedule:**
   - Set investigation triggers
   - Define email recipients
   - Adjust thresholds

---

## 📊 Expected Timeline

- **Creating SQL tables:** 5 minutes
- **Creating 3 Genie spaces:** 5 minutes each = 15 minutes
- **Testing spaces:** 5 minutes
- **Configuring agent:** 5 minutes
- **Total:** ~30 minutes to be demo-ready!

---

## 🧹 Cleanup (Optional)

**Remove Genie Spaces:**
1. Go to Genie in Databricks
2. For each space: Click **⋮ → Delete Space**

**Remove Mock Data:**
```sql
-- Run in Databricks SQL Editor
DROP TABLE IF EXISTS hackathon.hackathon_spiffit.sales_performance;
DROP TABLE IF EXISTS hackathon.hackathon_spiffit.spiff_winners;
DROP TABLE IF EXISTS hackathon.hackathon_spiffit.competitor_spiffs;

-- Note: Don't drop hackathon_spiffit schema - it's shared by the team!
```

---

## 🆘 Troubleshooting

**"Can't find table hackathon.hackathon_spiffit.*"**
→ Run the SQL scripts in Step 1 first!

**"No tables available in Genie"**
→ Make sure you selected a SQL warehouse when creating the space

**"Agent can't connect to spaces"**
→ Verify your space IDs are correct and env variables are set

**"Genie returns empty results"**
→ Check that your tables have data by running SELECT queries

---

## 📚 Related Docs

- `sql/README.md` - Detailed SQL setup instructions
- `docs/AUTONOMOUS_SPIFF_AGENT.md` - Agent architecture details
- `docs/SMART_GENIE_ROUTING.md` - Routing strategies
- `docs/MULTI_GENIE_WORKFLOWS.md` - Workflow patterns

---

**✅ You're all set! Time to demo some AI-powered SPIFF recommendations!** 🚀
