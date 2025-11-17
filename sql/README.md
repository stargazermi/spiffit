# SPG Demo SQL Scripts

Mock data for Genie space demo using **`hackathon.hackathon_spiffit`** schema.

## 📁 Files

Run these scripts **in order** in Databricks SQL Editor or Notebook:

1. **`01_create_spg_demo_schema.sql`** - Verify `hackathon` schema access
2. **`02_create_sales_performance_table.sql`** - Sales data for spg-mocking-bird-sales space
3. **`03_create_spiff_winners_table.sql`** - Analytics data for spg-mocking-bird-analytics space
4. **`04_create_competitor_spiffs_table.sql`** - Market data for spg-mocking-bird-market space

## 🚀 Quick Start

### Option 1: Run in Databricks SQL Editor

1. Go to **SQL Editor** in Databricks
2. Copy and paste each script in order
3. Click **Run** (or Ctrl+Enter)
4. Verify with the SELECT queries at the end of each script

### Option 2: Run in Databricks Notebook

```python
# Cell 1: Verify schema access
spark.sql("""
-- Paste contents of 01_create_spg_demo_schema.sql here
""")

# Cell 2: Create sales table
spark.sql("""
-- Paste contents of 02_create_sales_performance_table.sql here
""")

# Cell 3: Create winners table
spark.sql("""
-- Paste contents of 03_create_spiff_winners_table.sql here
""")

# Cell 4: Create competitor table
spark.sql("""
-- Paste contents of 04_create_competitor_spiffs_table.sql here
""")

# Verify all tables created
display(spark.sql("SHOW TABLES IN hackathon.hackathon_spiffit LIKE '*'"))
```

### Option 3: Run All at Once

```python
# In Databricks Notebook
import os

# Read and execute all SQL files
sql_files = [
    "01_create_spg_demo_schema.sql",
    "02_create_sales_performance_table.sql", 
    "03_create_spiff_winners_table.sql",
    "04_create_competitor_spiffs_table.sql"
]

for sql_file in sql_files:
    print(f"Executing {sql_file}...")
    with open(f"sql/{sql_file}", 'r') as f:
        sql = f.read()
        spark.sql(sql)
    print(f"✓ {sql_file} complete\n")

# Verify
display(spark.sql("SELECT * FROM hackathon.hackathon_spiffit.sales_performance"))
display(spark.sql("SELECT * FROM hackathon.hackathon_spiffit.spiff_winners"))
display(spark.sql("SELECT * FROM hackathon.hackathon_spiffit.competitor_spiffs"))
```

## ✅ Verification

After running all scripts, verify tables exist:

```sql
-- Show all tables in hackathon_spiffit schema
SHOW TABLES IN hackathon.hackathon_spiffit LIKE '*';

-- Should show:
-- sales_performance
-- spiff_winners
-- competitor_spiffs
```

## 🧹 Cleanup (Optional)

To remove all demo data:

```sql
-- Drop all tables
DROP TABLE IF EXISTS hackathon.hackathon_spiffit.sales_performance;
DROP TABLE IF EXISTS hackathon.hackathon_spiffit.spiff_winners;
DROP TABLE IF EXISTS hackathon.hackathon_spiffit.competitor_spiffs;

-- Note: Don't drop the hackathon_spiffit schema as it's shared by the team
```

---

**Next Step:** Create Genie spaces and connect these tables!
See `CREATE_GENIE_SPACES_GUIDE.md` for instructions.

