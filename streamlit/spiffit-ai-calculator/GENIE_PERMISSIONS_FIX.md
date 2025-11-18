# 🔐 Genie Space Permissions Issue - Fix Guide

## 🔍 Problem
You're seeing this error:
```
Genie error: Unable to get space [01f0c403c3cf184e9b7f1f6c9ee45905]. 
Caused by Node with resource name Some(datarooms/01f0c403...) does not exist.
```

## 🎯 Root Cause
**Databricks Apps use a different authentication context than your CLI.**

- ✅ **Your CLI credentials** → Have access to Genie spaces
- ❌ **Databricks App identity** → Does NOT have access (yet)

## ✅ Solution: Share Genie Spaces with the App

### Step 1: Find Your App's Identity

**Option A: Check in Databricks UI**
1. Go to your deployed app
2. Look for the app's service principal or workspace permissions
3. Note the identity (usually a service principal ID)

**Option B: Use Troubleshooting Tab**
After deployment, the troubleshooting tab will show connection status

---

### Step 2: Grant Permissions to Genie Spaces

For EACH Genie space (`spg-mocking-bird-sales`, `spg-mocking-bird-analytics`, `spg-mocking-bird-market`):

1. **Go to Databricks Workspace** → **Data Intelligence** → **Genie**

2. **Open the Genie space** (e.g., `spg-mocking-bird-sales`)

3. **Click "Share" or "Permissions"** button (top right)

4. **Add permissions:**
   - **If you see "All Workspace Users"**: Add that with **CAN USE** permission
   - **If you see your App's service principal**: Add it with **CAN USE** permission
   - **Alternative**: Add yourself and ensure "Share with workspace" is enabled

5. **Save permissions**

6. **Repeat for all 3 Genie spaces**

---

### Step 3: Restart the App

After granting permissions:
1. Go to Databricks Apps
2. Stop your app
3. Start it again
4. Check the **🔧 Troubleshooting** tab → should show "Genie Connected"

---

## 🧪 Test After Fix

### In Troubleshooting Tab:
- Click **"Test Genie Query"** button
- Should return actual data, not error

### In Chat Tab:
- Ask: "What data do you have?"
- Should query Genie successfully

### In Competitor Intel Tab:
- Click "⚔️ Our SPIFFs vs Competitors"
- Should query both Genie AND web search

---

## 🔄 Alternative: Use Foundation Models Only (Temporary)

If you can't fix permissions immediately, the app will fall back to Foundation Models:
- Chat tab works with GPT/Gemini/Llama
- Competitor Intel tab works (web search + synthesis)
- Just won't query real Genie data until permissions are fixed

---

## 📞 If Still Stuck

**Check these:**

1. **Genie spaces still exist?**
   ```bash
   databricks genie list-spaces --profile dlk-hackathon
   ```

2. **Space IDs match app.yaml?**
   - Sales: `01f0c403c3cf184e9b7f1f6c9ee45905`
   - Analytics: `01f0c404048613b3b494b1a64a1bca84`
   - Market: `01f0c4043acf19dc936c37fd2a8bced3`

3. **Environment variables loading?**
   - Check **🔧 Troubleshooting** tab → "Environment Variables" section
   - Should NOT be `null`

4. **App.yaml committed and pushed?**
   ```bash
   git status
   git diff streamlit/spiffit-ai-calculator/app.yaml
   ```

---

## 💡 Quick Permission Test

Ask your team:
- "Can others in the workspace query these Genie spaces?"
- If no → Genie spaces need workspace-wide permissions
- If yes → App needs specific permission

**Most likely fix:** Add "All Workspace Users" with CAN USE to each Genie space.

---

**Good luck! 🚀 Once permissions are fixed, all three tabs will work perfectly.**

