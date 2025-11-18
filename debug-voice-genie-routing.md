# 🐛 Debugging Voice Activations Genie Routing

## Problem
The Voice Activations query is returning data about "employee sales performance" instead of VOIP/MRR data. This means:
- ❌ Query is hitting the WRONG Genie space
- ❌ Likely hitting Sales Genie (mock data in dlk-hackathon)
- ✅ Need to verify routing logic and space IDs

---

## 🔍 Diagnostic Steps

### **Step 1: Check Which Genie Was Called**

Look at the **Intelligence Tab** (not Chat tab) after running the query.

**What to look for:**
```
🤖 Tools Called:
├─ Genie: Voice Activations*  ← Should show this!
└─ Results: [...]
```

**If you see:**
- `Genie: Sales` → Wrong Genie! Routing issue
- `Genie: Analytics` → Wrong Genie! Routing issue
- `Genie: Market` → Wrong Genie! Routing issue
- `Genie: Voice Activations*` → Correct Genie, but wrong data/workspace

---

### **Step 2: Check Environment Variables in Troubleshooting Tab**

**Look for:**
```
📋 Environment Variables:
  GENIE_SALES_SPACE_ID: 01f0c403...
  GENIE_ANALYTICS_SPACE_ID: 01f0c404...
  GENIE_MARKET_SPACE_ID: 01f0c4043...
  GENIE_VOICE_ACTIVATIONS_SPACE_ID: 01f0c3e4...  ← Should be set!
  
  DATABRICKS_VOICE_WORKSPACE_HOST: https://dbc-xxxx...  ← Should be alternate workspace!
  DATABRICKS_VOICE_WORKSPACE_TOKEN: dapi_***5c4  ← Should be set!
```

**If Voice Activations variables are NOT SET:**
- App didn't pick up the new environment variables
- Redeploy needed

---

### **Step 3: Check Logs for Voice Activations Initialization**

**In Troubleshooting tab logs, search for:**
```
🔄 ALTERNATE WORKSPACE (Cross-workspace access):
   Host: https://dbc-xxxxx-yyyy.cloud.databricks.com  ← Should be OTHER workspace!
   Token: ✅ SET (***...)
```

**If you see:**
```
DATABRICKS_HOST: https://dbc-4a93b454-f17b.cloud.databricks.com  ← dlk-hackathon
```
Then it's NOT using the alternate workspace credentials!

---

### **Step 4: Verify Space IDs**

**In the OTHER workspace (where Voice Activations lives):**

1. Open the Voice Activations Genie space
2. Look at the URL: `https://dbc-xxxx.../genie/rooms/[SPACE_ID]`
3. Verify the space ID matches `app.yaml`:
   ```yaml
   - name: GENIE_VOICE_ACTIVATIONS_SPACE_ID
     value: "01f0c3e4c6751989828598c96ee0debf"  ← Must match!
   ```

**To verify via CLI:**
```powershell
# Use the alternate workspace credentials
$env:DATABRICKS_HOST = "https://dbc-xxxxx-yyyy.cloud.databricks.com"
$env:DATABRICKS_TOKEN = "dapi_YOUR_OTHER_WORKSPACE_TOKEN"

# Try to get the Genie space
databricks api GET /api/2.0/preview/genie/spaces/01f0c3e4c6751989828598c96ee0debf
```

**Expected:**
```json
{
  "id": "01f0c3e4c6751989828598c96ee0debf",
  "name": "SPIFF Analyzer- TEST" (or whatever the real name is),
  ...
}
```

**If 404 or "does not exist":**
- ❌ Space ID is wrong
- ❌ Or space is in yet another workspace

---

### **Step 5: Check the Data in Voice Activations Genie**

**If routing is correct but data is wrong:**

1. Open the Voice Activations Genie space in the OTHER workspace
2. Ask it a test query: "Show me VOIP MRR by opportunity owner"
3. **Check the response:**
   - Does it have VOIP/MRR columns?
   - Or does it have "employee_name", "deals_closed", etc. (Sales data)?

**If it shows Sales data:**
- ❌ The Voice Activations Genie is pointing to the wrong tables!
- Ask data analyst to verify the Genie's data connection

---

## 🎯 Most Likely Issues

### **Issue 1: Routing Logic (Most Common)**

**Symptom:** Intelligence tab shows `Genie: Sales` or `Genie: Analytics`

**Cause:** LLM routing is picking the wrong Genie based on keywords

**Fix:** Use the **"🎤 Voice Incentive Calc" button** in the sidebar
- This button explicitly uses Voice Activations Genie
- Bypasses the routing logic
- Should show `Voice Activations*` in Intelligence tab

**Alternative:** Update the routing prompt in `multi_tool_agent.py` to be more explicit:
```python
4. Voice Activations/VOIP incentives/MRR payouts/opportunity owner → genie_voice_activations (CROSS-WORKSPACE)
```

---

### **Issue 2: Space ID is Wrong**

**Symptom:** Error "Unable to get space" or 404

**Cause:** Space ID doesn't exist in the alternate workspace

**Fix:**
1. Get the correct space ID from the data analyst
2. Update `app.yaml`:
   ```yaml
   - name: GENIE_VOICE_ACTIVATIONS_SPACE_ID
     value: "CORRECT_SPACE_ID_HERE"
   ```
3. Redeploy

---

### **Issue 3: Wrong Workspace Credentials**

**Symptom:** Logs show dlk-hackathon host instead of alternate workspace

**Cause:** `DATABRICKS_VOICE_WORKSPACE_HOST` not set or wrong

**Fix:**
1. Verify data analyst gave you the correct workspace URL
2. Update `app.yaml` with BOTH host + token
3. Redeploy
4. Check logs for "ALTERNATE WORKSPACE" message

---

### **Issue 4: Voice Activations Genie Has Wrong Data**

**Symptom:** Routing is correct, but Genie says "no VOIP columns"

**Cause:** The Genie space in the other workspace is connected to the wrong tables

**Fix:**
1. Ask data analyst to check the Genie's data source
2. Should be connected to tables with:
   - `opportunity_owner` column
   - `voip_mrr` or similar MRR columns
   - `product_type` (to filter VOIP products)
3. Data analyst needs to reconfigure the Genie space

---

## 🧪 Quick Test

**Run this PowerShell command to test if you can access the space:**

```powershell
# Set alternate workspace credentials
$env:DATABRICKS_HOST = "YOUR_OTHER_WORKSPACE_URL"
$env:DATABRICKS_TOKEN = "YOUR_OTHER_WORKSPACE_PAT"

# Try to access the Genie space
$headers = @{ "Authorization" = "Bearer $env:DATABRICKS_TOKEN" }
$url = "$env:DATABRICKS_HOST/api/2.0/preview/genie/spaces/01f0c3e4c6751989828598c96ee0debf"

Invoke-RestMethod -Uri $url -Headers $headers -Method Get | ConvertTo-Json
```

**Expected output:**
```json
{
  "id": "01f0c3e4c6751989828598c96ee0debf",
  "name": "Voice Activations Genie" (or similar),
  "description": "...",
  ...
}
```

**If error:**
- Check workspace URL is correct
- Check PAT token is correct
- Check space ID is correct

---

## 📋 Checklist

Before continuing, verify:
- [ ] Environment variables are set in app.yaml (HOST + TOKEN)
- [ ] App was redeployed after updating app.yaml
- [ ] Troubleshooting tab shows alternate workspace credentials
- [ ] Intelligence tab shows which Genie was called
- [ ] Voice Activations Genie exists in the other workspace
- [ ] Voice Activations Genie has VOIP/MRR data (test directly in that workspace)
- [ ] Using the sidebar button (not free-form query) to test

---

## 🎯 Next Steps

1. **Check Intelligence Tab** - Which Genie was actually called?
2. **Check Troubleshooting Tab** - Are alternate workspace credentials being used?
3. **Use the Sidebar Button** - "🎤 Voice Incentive Calc" to bypass routing
4. **Run Quick Test Script** - Verify you can access the space via API
5. **Ask Data Analyst** - Confirm space ID, workspace URL, and data source

**Once you confirm which issue it is, we can fix it!** 🎯

