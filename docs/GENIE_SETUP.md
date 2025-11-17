# Creating Your Own Genie Space for Hackathon

## ⚠️ Important
The existing Genie spaces in dlk-hackathon workspace belong to other teams:
- **DPI Stats** - Another team's space
- **DPI Service Order Stats** - Another team's space

**DO NOT use these spaces** - create your own for the hackathon!

---

## 🆕 Option 1: Create Your Own Genie Space

### Step 1: Go to Databricks Genie
1. Log into dlk-hackathon workspace: https://dbc-4ee5e339-1e79.cloud.databricks.com
2. Click **Genie** in the left sidebar
3. Click **Create Space** or **New Space**

### Step 2: Configure Your Space
- **Name:** `Hackathon Incentive Calculator` (or similar)
- **Description:** "Temporary space for AI hackathon - incentive data analysis"
- **SQL Warehouse:** Select an available warehouse
- **Tables:** Add your Delta tables (from `incentives` database)
  - `incentives.ae_performance`
  - `incentives.ae_opportunities`
  - `incentives.voice_activations`
  - etc.

### Step 3: Get Your Space ID
Once created:
1. Open your new space
2. Copy the Space ID from the URL or settings
3. Update `streamlit/spiffit-ai-calculator/app.py`:
   ```python
   ai = IncentiveAI(genie_space_id="YOUR_NEW_SPACE_ID")
   ```

### Step 4: Test It
Ask Genie a simple question like:
- "How many records are in the ae_performance table?"
- "Show me the top 5 performers by MRR"

If it works, you're ready!

---

## 🔧 Option 2: Use Foundation Model API (Current Default)

**No Genie space needed!** The app is already configured to use this.

**How it works:**
1. App uses LLM for natural language understanding
2. You connect to Delta Lake separately (in your calculator code)
3. Pass data to LLM for formatting

**Pros:**
- ✅ No Genie space needed
- ✅ Doesn't interfere with other teams
- ✅ Works right now

**Cons:**
- ❌ Need to write data query logic
- ❌ Need Spark/Delta connection

---

## 🎯 Recommended for Hackathon

**Start with Option 2 (Foundation Model)** - it's already set up and working!

**If you have time later**, create your own Genie space (Option 1) for easier data access.

---

## 📊 Checking Existing Spaces

To see all Genie spaces:
```bash
databricks genie list-spaces --profile dlk-hackathon -o json
```

To avoid conflicts, name yours clearly:
- "Hackathon - [Your Team Name]"
- "Temp - Incentive AI Calculator"
- "Spiffit Hackathon Space"

---

## 🧹 Cleanup After Hackathon

Remember to delete your Genie space after the hackathon to keep the workspace clean!

```bash
# Get your space ID first, then:
databricks genie delete-space --space-id YOUR_SPACE_ID --profile dlk-hackathon
```

---

**Current setup:** Using Foundation Model API (safe, no conflicts) ✅

