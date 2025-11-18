# Migrating Logic to Working Genie Space

## Overview

Switching from NEW space (broken): `0110c4ae99271d64835d414b8d43ddfb`  
To OLD space (working): `01f0c4ae99271d64835d414b8d43ddfb`

## What Needs to be Migrated

### 1. Genie Space Instructions

**From NEW Space:**
Copy the "Instructions" you configured for Voice Activations incentive calculations.

**To OLD Space:**
1. Go to: https://dbc-4a93b454-f17b.cloud.databricks.com/genie/rooms/01f0c4ae99271d64835d414b8d43ddfb
2. Click **"Configure"** (gear icon)
3. Click **"Instructions"** tab
4. Paste the Voice Activations instructions:

```
This Genie space provides SPIFF (Sales Performance Incentive Fund) analysis for Frontier sales agents.

Key Data Sources:
- voice_opps: Voice opportunity data with MRR and opportunity owners
- voice_orders: Voice order data with order stage information

Voice Activations Incentive Rules:
- Designed to encourage sellers to drive incremental VOIP sales
- Based on Opportunity Level
- Applies to any NEW incremental VOIP MRR (Renewals are excluded)
- Payout tiers:
  * Min. $250 MRR = $300 payout
  * $1000+ MRR = $1000 payout
- Exclude opportunities where order stage = "Cancelled"
- Group results by 18-digit opportunity ID
- Sum MRR by opportunity owner
- Calculate incentive payout based on the rules above

When asked about Voice Activations:
1. Query voice_opps and voice_orders tables
2. Join on opportunity_id_18 (18-digit)
3. Filter out cancelled orders
4. Sum MRR by opportunity owner
5. Apply incentive calculation rules
6. Return: opportunity owner, sum MRR, calculated incentive payout
```

### 2. Data Tables

**Check Data Connection:**
1. In OLD Genie space, click **"Configure"** → **"Data"** tab
2. Ensure these tables are connected:
   - `hackathon.hackathon_spiffit.voice_opps`
   - `hackathon.hackathon_spiffit.voice_orders`
3. If not connected, click **"Add Data"** and select them

**Verify Data Exists:**
Run this in Databricks SQL Editor to confirm:

```sql
-- Check voice_opps
SELECT COUNT(*), SUM(mrr) as total_mrr 
FROM hackathon.hackathon_spiffit.voice_opps;

-- Check voice_orders
SELECT COUNT(*), 
       SUM(CASE WHEN order_stage = 'Cancelled' THEN 1 ELSE 0 END) as cancelled_count
FROM hackathon.hackathon_spiffit.voice_orders;
```

### 3. Test Prompts

After migrating, test these prompts in the OLD Genie space:

**Test 1: Basic Query**
```
Show me voice opportunities with their MRR
```

**Test 2: Voice Activations Incentive (Full)**
```
For Voice Opportunities, sum MRR by 18 digit opportunity ID and calculate the incentive payout for that opportunity using the following rules return all applicable columns and rows (exclude opportunities where the order stage = Cancelled): Voice Activations Incentive: (Payout Min. $250 MRR = $300 |$1000+ MRR = $1000)
```

## Updating App Configuration

### Already Done:
✅ `app.yaml` updated to use OLD space ID  
✅ Script created to update `.env` file

### To Do:
1. Run the migration script:
   ```powershell
   pwsh switch-to-old-space.ps1
   ```

2. Redeploy the app:
   ```powershell
   pwsh deploy-app.ps1
   ```

3. Test locally:
   ```powershell
   streamlit run app.py
   ```

## Troubleshooting

### If OLD space still doesn't work:

1. **Check Permissions:**
   - OLD space must be shared with your user (`spg1461@ftr.com`)
   - Or enable "All workspace users" access

2. **Check SQL Warehouse:**
   - Warehouse `0962fa4cf0922125` must be running
   - You must have "Can Use" permission on the warehouse

3. **Check PAT Token:**
   - Token in `app.yaml` must have access to OLD space
   - Generate new token if needed

4. **Test with CLI:**
   ```powershell
   databricks api get /api/2.0/genie/spaces/01f0c4ae99271d64835d414b8d43ddfb --profile dlk-hackathon
   ```

## Why the NEW Space Failed

The NEW space `0110c4ae99271d64835d414b8d43ddfb` had permission issues:
- Could not be accessed via CLI
- Could not be accessed via PAT token
- Not visible in Genie space list
- Likely a permissions configuration issue at creation time

The OLD space `01f0c4ae99271d64835d414b8d43ddfb` works correctly with proper permissions.

---

**Status:** Ready to migrate! 🎸

