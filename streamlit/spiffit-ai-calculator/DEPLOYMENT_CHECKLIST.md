# 🚀 Deployment Checklist for v1.3.0

## Before You Push

- [x] All files created:
  - `web_search_tool.py`
  - `multi_tool_agent.py`
  - `COMPETITOR_INTEL_DEMO.md`
  - `GENIE_PERMISSIONS_FIX.md`
  - `DEPLOYMENT_CHECKLIST.md` (this file)

- [x] Updated files:
  - `app.py` (v1.3.0, 3 tabs)
  - `CHANGELOG.md` (documented v1.3.0)
  - `README.md` (new features listed)

- [ ] Review changes:
```bash
git status
git diff streamlit/spiffit-ai-calculator/
```

---

## Step 1: Push to Git

```bash
cd C:\code\hackathon\spiffit
git add streamlit/spiffit-ai-calculator/
git commit -m "Add competitor intelligence multi-tool agent (v1.3.0) with graceful error handling"
git push origin main
```

**✅ Checkpoint:** Verify push succeeded on GitHub

---

## Step 2: Redeploy Databricks App

### Option A: Auto-Update (if configured)
- Wait 2-3 minutes for auto-pull from Git

### Option B: Manual Restart
1. Go to Databricks workspace
2. Navigate to **Apps** (left sidebar)
3. Find your app: `spiffit-ai-calculator`
4. Click **Stop**
5. Click **Start** (or **Restart**)
6. Wait ~2-3 minutes for deployment

**✅ Checkpoint:** App shows "Running" status

---

## Step 3: Verify Deployment Version

1. Open the app URL
2. Go to **🔧 Troubleshooting** tab
3. Check **📦 Deployment Info**:
   - Version should be **v1.3.0**
   - Timestamp should be recent (today's date)

**✅ Checkpoint:** Correct version and fresh timestamp

---

## Step 4: Check Environment Variables

Still in **🔧 Troubleshooting** tab:

### 🔍 Environment Variables Section
Should show (not `null`):
```json
{
  "GENIE_SPACE_ID": "01f0c403c3cf184e9b7f1f6c9ee45905",
  "GENIE_SALES_SPACE_ID": "01f0c403c3cf184e9b7f1f6c9ee45905",
  "GENIE_ANALYTICS_SPACE_ID": "01f0c404048613b3b494b1a64a1bca84",
  "GENIE_MARKET_SPACE_ID": "01f0c4043acf19dc936c37fd2a8bced3",
  "DATABRICKS_PROFILE": null (expected for Databricks Apps)
}
```

**✅ Checkpoint:** All Genie space IDs are loaded

**❌ If all null:** 
- `app.yaml` wasn't deployed
- Stop app, verify `app.yaml` is in repo, restart

---

## Step 5: Test Genie Connection

### In Troubleshooting Tab:
1. Scroll to **🔄 Quick Actions**
2. Click **"Test Genie Query"** button

### Expected Results:

#### ❌ Likely Result (Permissions Issue):
```
✅ Genie query successful!
Response: Genie error: Unable to get space...
```

**→ Go to Step 6 (Fix Permissions)**

#### ✅ Success Result:
```
✅ Genie query successful!
Response: [Actual data from Genie space]
```

**→ Skip to Step 7 (Test New Features)**

---

## Step 6: Fix Genie Permissions (If Needed)

**See `GENIE_PERMISSIONS_FIX.md` for detailed instructions.**

### Quick Steps:
1. Open Databricks → **Data Intelligence** → **Genie**
2. For each space (`spg-mocking-bird-sales`, `analytics`, `market`):
   - Click **Share/Permissions**
   - Add **"All Workspace Users"** with **CAN USE**
   - Or add the app's service principal
   - Save
3. Restart the app in Databricks Apps
4. Re-test Genie connection (Step 5)

**✅ Checkpoint:** Test Genie Query returns data, not error

---

## Step 7: Test New Competitor Intelligence Tab

### Go to **🌐 Competitor Intel** tab

### Test 1: Web Search Only (Should Always Work)
1. Click **"🔍 Search AT&T Programs"** button
2. Should return competitor data
3. Expand **"🧠 AI Reasoning & Tools"**
4. Should show: `tools_used: ["web_search"]`

**✅ Checkpoint:** Returns AT&T SPIFF data

---

### Test 2: Internal Data (Requires Genie Permissions)
1. Type: "Who are our top performers?"
2. Should query `genie_analytics`
3. If Genie works: Returns internal data
4. If Genie broken: Shows helpful error + falls back gracefully

**✅ Checkpoint:** Either returns data OR shows clear error message

---

### Test 3: Multi-Tool (The Demo Wow Moment!)
1. Click **"⚔️ Our SPIFFs vs Competitors"** button
2. Agent routes to BOTH `genie_analytics` + `web_search`
3. GPT-5.1 synthesizes results
4. Shows comprehensive comparison

**Possible outcomes:**
- **Best case:** Both work, see full synthesis ✅
- **Genie broken:** Web search works, Genie error shown, but competitor data still displayed ⚠️
- **Foundation model issue:** Shows error with troubleshooting tips ❌

**✅ Checkpoint:** At least web search works, error handling is graceful

---

## Step 8: Test Chat Tab (Original Feature)

1. Go to **💬 Chat** tab
2. Type: "What data do you have?"
3. Should query Genie or fall back to Foundation Model

**✅ Checkpoint:** Gets some response (even if error, should be helpful)

---

## Status Summary

After completing all steps, you should have:

### ✅ Working Right Away:
- **Competitor Intel Tab → Web Search** (mock competitor data)
- **Foundation Models** (GPT-5.1, Gemini, etc.)
- **Smart routing** (decides which tools to use)
- **Error handling** (graceful fallbacks with helpful messages)

### ⚠️ May Need Permissions Fix:
- **Genie space queries** (internal data)
- **Multi-tool synthesis** with real internal data

### 🎯 Hackathon Demo Recommendations:

**If Genie is working:**
- Show full multi-tool demo (internal + external data)
- Highlight smart routing
- Emphasize transparency (show tools used)

**If Genie has permissions issues:**
- Focus on web search + Foundation Models
- Explain the architecture (show error handling)
- Mention Genie as "ready to connect" once permissions are granted
- **Still impressive:** Shows multi-tool pattern, smart routing, and graceful error handling

---

## 📞 Quick Reference

**Key Files:**
- Deployment version: Check `app.py` line 19 (`APP_VERSION`)
- Permissions guide: `GENIE_PERMISSIONS_FIX.md`
- Demo script: `COMPETITOR_INTEL_DEMO.md`

**Databricks CLI Quick Tests:**
```bash
# List Genie spaces
databricks genie list-spaces --profile dlk-hackathon

# Check serving endpoints
databricks serving-endpoints list --profile dlk-hackathon
```

**Environment Check in App:**
- **🔧 Troubleshooting** tab → All sections
- Green = working, Red = needs attention

---

**Good luck with deployment! 🚀**

