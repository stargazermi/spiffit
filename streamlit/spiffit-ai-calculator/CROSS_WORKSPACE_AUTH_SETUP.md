# 🔐 Cross-Workspace Authentication Setup

## Problem
You need to access a Genie space (`01f0c3e4c6751989828598c96ee0debf`) in a **different workspace** than the main app workspace (`dlk-hackathon`).

PAT tokens are workspace-specific, so you need a separate token for the other workspace.

---

## ✅ Solution Implemented

The app now supports **separate PAT tokens** for cross-workspace Genie access!

**What changed:**
- `ai_helper.py` - Added `alt_workspace_token` parameter
- `multi_tool_agent.py` - Voice Activations Genie uses `DATABRICKS_VOICE_WORKSPACE_TOKEN`
- `app.yaml` - Added new environment variable for alternate token

---

## 🎯 Setup Steps

### **Step 1: Get PAT Token from Other Workspace**

1. **Log into the workspace where Voice Activations Genie lives**
   - Ask your data analyst for the workspace URL
   - Or check where space `01f0c3e4c6751989828598c96ee0debf` is located

2. **Generate a PAT Token:**
   - Click your user icon (top right)
   - **User Settings** → **Developer** → **Access Tokens**
   - Click **"Generate New Token"**
   - **Comment:** "Spiffit cross-workspace access - Voice Activations Genie"
   - **Lifetime:** 90 days (or as needed)
   - **Click "Generate"**
   - **⚠️ COPY THE TOKEN IMMEDIATELY** (you can't see it again!)

3. **Save the token:**
   ```
   dapi_YOUR_NEW_TOKEN_FROM_OTHER_WORKSPACE
   ```

---

### **Step 2: Update app.yaml**

**Edit:** `streamlit/spiffit-ai-calculator/app.yaml`

**Find this line:**
```yaml
- name: DATABRICKS_VOICE_WORKSPACE_TOKEN
  value: "YOUR_OTHER_WORKSPACE_PAT_TOKEN_HERE"  # ⚠️ REQUIRED
```

**Replace with your actual token:**
```yaml
- name: DATABRICKS_VOICE_WORKSPACE_TOKEN
  value: "dapi_YOUR_NEW_TOKEN_FROM_OTHER_WORKSPACE"
```

**Example:**
```yaml
- name: DATABRICKS_VOICE_WORKSPACE_TOKEN
  value: "dapi_abc123def456ghi789jkl012mno345"
```

---

### **Step 3: Deploy**

```powershell
.\deploy-to-databricks.ps1
```

**The deployment script will:**
1. Git pull latest changes in Databricks
2. Restart the app with new environment variable
3. Voice Activations Genie will now use the alternate token!

---

## 🧪 Testing

### **Check Logs (Troubleshooting Tab):**

After deployment, click the Voice Activations button and check the logs. You should see:

```
✅ Using ALTERNATE PAT Token authentication (cross-workspace)
   Host: https://dbc-4a93b454-f17b.cloud.databricks.com
   Alt Token: ***5c4
Auth Method: PAT Token (Cross-Workspace)
```

### **Test the Button:**

**Sidebar → "📞 Voice Activations (Cross-Workspace)" → "🎤 Voice Incentive Calc"**

**Expected behavior:**
- ✅ Query succeeds
- ✅ Shows Voice Activations data
- ✅ Calculates VOIP MRR payouts

**Previous error (should NOT appear):**
```
❌ You need "Can View" permission to perform this action
```

---

## 📊 How It Works

### **Authentication Flow:**

```
Voice Activations Genie Query
      ↓
Check: Is DATABRICKS_VOICE_WORKSPACE_TOKEN set?
      ↓
   YES → Use alternate token for authentication
      ↓
Connect to other workspace with that token
      ↓
Access Voice Activations Genie (01f0c3e4c6751989828598c96ee0debf)
      ↓
Return results! ✅
```

### **Other Genies (Sales, Analytics, Market):**

Still use the main `DATABRICKS_TOKEN` since they're in the `dlk-hackathon` workspace.

---

## 🔧 Troubleshooting

### **Error: "You need Can View permission"**

**Cause:** Token is from wrong workspace or doesn't have permissions.

**Fix:**
1. Verify you generated the PAT from the **correct workspace**
2. Check the Genie space exists in that workspace
3. Verify your user has "Can View" (or "Can Edit") on that Genie space

---

### **Error: "Token is invalid"**

**Cause:** PAT token expired or was revoked.

**Fix:**
1. Generate a new PAT token from the other workspace
2. Update `app.yaml` with new token
3. Redeploy

---

### **Logs show: "DATABRICKS_TOKEN: (overridden by alt token)"**

**Good!** This means the alternate token is being used correctly for Voice Activations.

---

### **Logs show: "DATABRICKS_TOKEN: ✅ SET (***5c4)"**

**Bad!** This means the alternate token is NOT being used. Check:
1. Is `DATABRICKS_VOICE_WORKSPACE_TOKEN` set in `app.yaml`?
2. Did you deploy after updating `app.yaml`?
3. Check the Troubleshooting tab for environment variables

---

## 💡 Alternative: Migrate Genie Space

**If you can't get a PAT from the other workspace:**

Ask the data analyst to:
1. **Share the Genie space** to your user in `dlk-hackathon` workspace
2. **Or recreate the Genie** in `dlk-hackathon` workspace
3. **Then update** `GENIE_VOICE_ACTIVATIONS_SPACE_ID` in `app.yaml`
4. **Remove** the `DATABRICKS_VOICE_WORKSPACE_TOKEN` line (not needed)

**Advantage:** No cross-workspace complexity, all Genies in one place!

---

## 📝 Local Testing

**For local testing, create `.env` file:**

```bash
# Main workspace token
DATABRICKS_HOST=https://dbc-4a93b454-f17b.cloud.databricks.com
DATABRICKS_TOKEN=dapi5e40d9eb65d1af6c91866e0a35c4

# Alternate workspace token for Voice Activations
DATABRICKS_VOICE_WORKSPACE_TOKEN=dapi_YOUR_OTHER_WORKSPACE_TOKEN_HERE

# Genie Space IDs
GENIE_SALES_SPACE_ID=01f0c403c3cf184e9b7f1f6c9ee45905
GENIE_ANALYTICS_SPACE_ID=01f0c404048613b3b494b1a64a1bca84
GENIE_MARKET_SPACE_ID=01f0c4043acf19dc936c37fd2a8bced3
GENIE_VOICE_ACTIVATIONS_SPACE_ID=01f0c3e4c6751989828598c96ee0debf

# SQL Warehouse
SQL_WAREHOUSE_ID=0962fa4cf0922125
```

**Then run locally:**
```bash
cd C:\code\hackathon\spiffit\streamlit\spiffit-ai-calculator
streamlit run app.py --server.port 8501
```

---

## 🎯 Version

**Added in:** v2.7.1-SPIFFIT  
**Files Modified:**
- `ai_helper.py` - Added `alt_workspace_token` parameter
- `multi_tool_agent.py` - Voice Activations uses `DATABRICKS_VOICE_WORKSPACE_TOKEN`
- `app.yaml` - Added new environment variable
- `CROSS_WORKSPACE_AUTH_SETUP.md` - This guide

---

**🎸 Cross-workspace auth problems? You must Spiff It! 🎸**

