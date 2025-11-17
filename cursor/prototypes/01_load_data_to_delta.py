"""
Starter Code: Load Excel Data to Delta Lake
Run this in a Databricks Notebook
"""

# ============================================================================
# STEP 1: Upload Excel Files to Databricks
# ============================================================================
# Before running this code:
# 1. Go to Databricks workspace
# 2. Click "Data" → "Create Table"
# 3. Upload your Excel files OR use dbutils to upload programmatically

# ============================================================================
# STEP 2: Read Excel Files
# ============================================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Spark
spark = SparkSession.builder.appName("IncentiveDataLoader").getOrCreate()

# Option A: If you uploaded to DBFS
ae_ethernet_path = "/FileStore/tables/AE_Ethernet_Incentive_Data.xlsx"
voice_path = "/FileStore/tables/Voice_Incentive_data.xlsx"

# Option B: If you're running locally (for testing)
# ae_ethernet_path = "test-data/AE Ethernet Incentive Data.xlsx"
# voice_path = "test-data/Voice_Incentive_data.xlsx"

# Read Excel files
print("📊 Reading AE Ethernet data...")
ae_sheet1 = spark.read \
    .format("com.crealytics.spark.excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("dataAddress", "'AE Ethernet Incentive Data 1'!A1") \
    .load(ae_ethernet_path)

ae_sheet2 = spark.read \
    .format("com.crealytics.spark.excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("dataAddress", "'AE Ethernet Incentive Data 2'!A1") \
    .load(ae_ethernet_path)

ae_sheet3 = spark.read \
    .format("com.crealytics.spark.excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("dataAddress", "'AE Ethernet Incentive Data 3'!A1") \
    .load(ae_ethernet_path)

print("📊 Reading Voice incentive data...")
voice_sheet1 = spark.read \
    .format("com.crealytics.spark.excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("dataAddress", "'Voice Act. Incentive Data 1'!A1") \
    .load(voice_path)

voice_sheet2 = spark.read \
    .format("com.crealytics.spark.excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("dataAddress", "'Voice Act. Incentive Data 3'!A1") \
    .load(voice_path)

print("✅ Data loaded successfully!")

# ============================================================================
# STEP 3: Clean and Transform Data
# ============================================================================

print("\n🧹 Cleaning AE Ethernet data...")

# Clean Sheet 1 - Performance metrics
ae_performance = ae_sheet1 \
    .withColumn("mrr_budget", col("MRR Budget").cast("double")) \
    .withColumn("mrr_actual", col("MRR Actual").cast("double")) \
    .withColumn("mrr_attainment_pct", 
                regexp_replace(col("MRR Attainment"), "%", "").cast("double") / 100) \
    .withColumn("renewal_budget", col("Renewal Budget").cast("double")) \
    .withColumn("renewal_actual", col("Renewal Actual").cast("double")) \
    .withColumn("renewal_attainment_pct",
                regexp_replace(col("Renewal Attainment"), "%", "").cast("double") / 100) \
    .withColumn("tcv_budget", col("TCV Budget").cast("double")) \
    .withColumn("tcv_actual", col("TCV Actual").cast("double")) \
    .withColumn("tcv_attainment_pct",
                regexp_replace(col("TCV Attainment"), "%", "").cast("double") / 100) \
    .withColumn("ethernet_target", col("Ethernet Target").cast("double")) \
    .withColumn("ethernet_actual", col("Ethernet Actual").cast("double")) \
    .withColumn("ethernet_attainment_pct",
                regexp_replace(col("Ethernet Attainment"), "%", "").cast("double") / 100) \
    .withColumn("lit_target", col("Lit Target").cast("double")) \
    .withColumn("lit_actual", col("Lit Actual").cast("double")) \
    .withColumn("lit_attainment_pct",
                regexp_replace(col("Lit Attainment"), "%", "").cast("double") / 100) \
    .withColumn("spf_projected", col("SPF/PS (Projected)").cast("double")) \
    .withColumn("spf", col("SPF").cast("double")) \
    .select(
        col("Region").alias("region"),
        col("Leader").alias("leader"),
        col("AE").alias("ae_name"),
        col("Deal Loper").alias("deal_loper"),
        col("CRIS ID").alias("cris_id"),
        col("DOH").alias("date_of_hire"),
        "mrr_budget", "mrr_actual", "mrr_attainment_pct",
        "renewal_budget", "renewal_actual", "renewal_attainment_pct",
        "tcv_budget", "tcv_actual", "tcv_attainment_pct",
        "ethernet_target", "ethernet_actual", "ethernet_attainment_pct",
        "lit_target", "lit_actual", "lit_attainment_pct",
        "spf_projected", "spf",
        col("Notes").alias("notes")
    )

# Clean Sheet 2 - Opportunity details
ae_opportunities = ae_sheet2 \
    .withColumnRenamed("18 Digit User ID", "user_id") \
    .withColumnRenamed("Total Name", "total_name") \
    .withColumnRenamed("Net New", "net_new") \
    .withColumnRenamed("Quantity", "quantity") \
    .withColumnRenamed("Opportunity Owner", "opportunity_owner") \
    .withColumnRenamed("Opportunity Owner: Manager", "opportunity_manager") \
    .withColumnRenamed("Close Month", "close_month") \
    .withColumnRenamed("RVP", "rvp") \
    .withColumnRenamed("Close Date", "close_date") \
    .withColumnRenamed("18 Digit Opty ID", "opportunity_id") \
    .withColumnRenamed("Opportunity Name", "opportunity_name") \
    .withColumnRenamed("Account Owner: Manager", "account_manager") \
    .withColumnRenamed("Assigned to", "assigned_to") \
    .withColumnRenamed("Sales Stage", "sales_stage") \
    .withColumnRenamed("Forecast Category", "forecast_category") \
    .withColumnRenamed("Product Name", "product_name")

# Clean Sheet 3 - Lit building data
ae_lit_buildings = ae_sheet3 \
    .withColumnRenamed("18 Digit User ID", "user_id") \
    .withColumnRenamed("Opportunity Owner: Manager", "opportunity_manager") \
    .withColumnRenamed("Opportunity Owner", "opportunity_owner") \
    .withColumnRenamed("Lit Building Count", "lit_building_count") \
    .withColumnRenamed("Net New", "net_new") \
    .withColumnRenamed("Total Name", "total_name") \
    .withColumnRenamed("Close Month", "close_month") \
    .withColumnRenamed("Close Date", "close_date") \
    .withColumnRenamed("18 Digit Opty ID", "opportunity_id") \
    .withColumnRenamed("Opportunity Name", "opportunity_name") \
    .withColumnRenamed("Assigned to", "assigned_to") \
    .withColumnRenamed("Sales Stage", "sales_stage") \
    .withColumnRenamed("Forecast Cat", "forecast_category") \
    .withColumnRenamed("Product Name", "product_name") \
    .withColumnRenamed("Account Owner's Manager", "account_manager") \
    .withColumnRenamed("Quantit", "quantity") \
    .withColumnRenamed("Product ID", "product_id") \
    .withColumnRenamed("RVP", "rvp")

print("🧹 Cleaning Voice data...")

# Clean Voice Sheet 1 - Voice activations
voice_activations = voice_sheet1 \
    .withColumnRenamed("Sales Stage", "sales_stage") \
    .withColumnRenamed("Opportunity Owner: Manager", "opportunity_manager") \
    .withColumnRenamed("Opportunity ID", "opportunity_id") \
    .withColumnRenamed("18 Digit Oppty ID", "opportunity_id_18") \
    .withColumnRenamed("Opportunity Owner", "opportunity_owner") \
    .withColumnRenamed("Account Name", "account_name") \
    .withColumnRenamed("Opportunity Name", "opportunity_name") \
    .withColumnRenamed("Total Net New MRR", "total_net_new_mrr") \
    .withColumnRenamed("New TCV", "new_tcv") \
    .withColumnRenamed("Quantity", "quantity") \
    .withColumnRenamed("Order Count", "order_count") \
    .withColumnRenamed("Order Stages", "order_stages") \
    .withColumnRenamed("Payout", "payout") \
    .withColumnRenamed("Notes", "notes")

# Clean Voice Sheet 2 - Order details
voice_orders = voice_sheet2 \
    .withColumnRenamed("id", "order_id") \
    .withColumnRenamed("OpportunityId", "opportunity_id") \
    .withColumnRenamed("OrderNumber", "order_number") \
    .withColumnRenamed("Order_Stage__c", "order_stage") \
    .withColumnRenamed("OwnerId", "owner_id") \
    .withColumnRenamed("StageOwner", "stage_owner") \
    .withColumnRenamed("Order_Start_Date", "order_start_date")

print("✅ Data cleaned successfully!")

# ============================================================================
# STEP 4: Write to Delta Lake
# ============================================================================

print("\n💾 Writing to Delta Lake...")

# Create database if it doesn't exist
spark.sql("CREATE DATABASE IF NOT EXISTS incentives")

# Write AE Ethernet data
print("Writing ae_performance table...")
ae_performance.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("incentives.ae_performance")

print("Writing ae_opportunities table...")
ae_opportunities.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("incentives.ae_opportunities")

print("Writing ae_lit_buildings table...")
ae_lit_buildings.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("incentives.ae_lit_buildings")

# Write Voice data
print("Writing voice_activations table...")
voice_activations.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("incentives.voice_activations")

print("Writing voice_orders table...")
voice_orders.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("incentives.voice_orders")

print("\n✅ All data written to Delta Lake!")

# ============================================================================
# STEP 5: Verify Data
# ============================================================================

print("\n🔍 Verifying data...")
print("\nTable: incentives.ae_performance")
spark.sql("SELECT COUNT(*) as row_count FROM incentives.ae_performance").show()
spark.sql("SELECT * FROM incentives.ae_performance LIMIT 3").show(truncate=False)

print("\nTable: incentives.voice_activations")
spark.sql("SELECT COUNT(*) as row_count FROM incentives.voice_activations").show()
spark.sql("SELECT * FROM incentives.voice_activations LIMIT 3").show(truncate=False)

print("\n🎉 Setup complete! You're ready to build your AI calculator!")

# ============================================================================
# STEP 6: Create Sample Queries (for testing)
# ============================================================================

print("\n📊 Sample queries you can run:")

print("\n1. Get all AEs with their MRR attainment:")
sample_query_1 = """
SELECT 
    ae_name,
    region,
    mrr_budget,
    mrr_actual,
    mrr_attainment_pct,
    CASE 
        WHEN mrr_attainment_pct >= 1.2 THEN 'Platinum'
        WHEN mrr_attainment_pct >= 1.0 THEN 'Gold'
        WHEN mrr_attainment_pct >= 0.8 THEN 'Silver'
        ELSE 'Bronze'
    END as incentive_tier
FROM incentives.ae_performance
ORDER BY mrr_attainment_pct DESC
LIMIT 10
"""
spark.sql(sample_query_1).show()

print("\n2. Calculate total potential incentive for top performer:")
sample_query_2 = """
SELECT 
    ae_name,
    region,
    mrr_attainment_pct,
    (mrr_budget * 0.15 * CASE WHEN mrr_attainment_pct >= 1.0 THEN 1 ELSE 0 END) as mrr_incentive,
    (renewal_budget * 0.10 * CASE WHEN renewal_attainment_pct >= 1.0 THEN 1 ELSE 0 END) as renewal_incentive,
    (tcv_budget * 0.12 * CASE WHEN tcv_attainment_pct >= 1.0 THEN 1 ELSE 0 END) as tcv_incentive
FROM incentives.ae_performance
WHERE mrr_attainment_pct >= 1.0
ORDER BY mrr_attainment_pct DESC
LIMIT 5
"""
spark.sql(sample_query_2).show()

print("\n3. Voice activations with highest payouts:")
sample_query_3 = """
SELECT 
    opportunity_owner,
    account_name,
    total_net_new_mrr,
    new_tcv,
    quantity,
    payout
FROM incentives.voice_activations
ORDER BY payout DESC
LIMIT 10
"""
spark.sql(sample_query_3).show()

print("\n✅ All done! Next steps:")
print("1. Open cursor/prototypes/02_incentive_calculator.py")
print("2. Build your calculation functions")
print("3. Add AI/LLM integration")
print("4. Create the UI")
print("\n🚀 Good luck with your hackathon!")

