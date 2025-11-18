# 📜 Authentication Logging Guide

**Version 1.4.2** adds comprehensive authentication logging to help diagnose Genie connection issues.

---

## 🎯 What's New

### **1. Detailed Authentication Logs**

The app now logs:
- ✅ Which authentication method is being used
- ✅ Which environment variables are set
- ✅ Every Genie API call attempt
- ✅ Detailed error information

### **2. Real-Time Log Viewer**

Go to **🔧 Troubleshooting** tab → scroll down to **📜 Authentication & API Logs**

---

## 📊 How to Use

### **Step 1: Deploy the App**

```powershell
git add .
git commit -m "v1.4.2: Add authentication logging"
git push origin spiffit-dev
.\deploy-to-databricks.ps1
```

### **Step 2: Open Troubleshooting Tab**

1. Go to your Databricks App
2. Click **🔧 Troubleshooting** tab
3. Scroll down to **📜 Authentication & API Logs**

### **Step 3: Test Genie**

Click **"Test Genie Query"** button

### **Step 4: Check the Logs**

Look for these key log entries:

---

## 🔍 What to Look For

### **✅ Successful PAT Token Auth**

```
🔐 IncentiveAI Authentication Debug
============================================================
📋 Environment Variables:
  DATABRICKS_HOST: https://dbc-4a93b454-f17b.cloud.databricks.com
  DATABRICKS_TOKEN: ✅ SET (***35c4)
  DATABRICKS_PROFILE: ❌ NOT SET
  GENIE_SPACE_ID (param): 01f0c403c3cf184e9b7f1f6c9ee45905

✅ Using PAT Token authentication (host + token)
   Host: https://dbc-4a93b454-f17b.cloud.databricks.com
   Token: ***35c4
🔑 Auth Method: PAT Token
============================================================

💬 Calling Genie API
============================================================
Space ID: 01f0c403c3cf184e9b7f1f6c9ee45905
Question: Show me the top performers
Auth Method: PAT Token
⏳ Initiating conversation (async)...
⏳ Waiting for Genie response...
✅ Received response from Genie
```

**This is GOOD!** ✅

---

### **❌ OAuth M2M Auth (Won't Work with Genie)**

```
🔐 IncentiveAI Authentication Debug
============================================================
📋 Environment Variables:
  DATABRICKS_HOST: ❌ NOT SET
  DATABRICKS_TOKEN: ❌ NOT SET
  DATABRICKS_PROFILE: ❌ NOT SET
  GENIE_SPACE_ID (param): 01f0c403c3cf184e9b7f1f6c9ee45905

⚠️ Using automatic OAuth M2M authentication
   This authentication method does NOT support Genie!
🔑 Auth Method: OAuth M2M (default)
============================================================

💬 Calling Genie API
============================================================
Space ID: 01f0c403c3cf184e9b7f1f6c9ee45905
Question: Show me the top performers
Auth Method: OAuth M2M (default)
⏳ Initiating conversation (async)...

❌ Genie API call failed!
Error: Unable to get space [01f0c403c3cf184e9b7f1f6c9ee45905]...
```

**This is the PROBLEM!** ❌

---

## 🛠️ Troubleshooting

### **Problem: OAuth M2M being used instead of PAT token**

**Symptoms:**
```
DATABRICKS_HOST: ❌ NOT SET
DATABRICKS_TOKEN: ❌ NOT SET
Auth Method: OAuth M2M (default)
```

**Cause:** Environment variables from `app.yaml` are not loading.

**Fix:**

1. **Verify `app.yaml` has the env section:**
   ```yaml
   env:
     - name: DATABRICKS_HOST
       value: "https://dbc-4a93b454-f17b.cloud.databricks.com"
     - name: DATABRICKS_TOKEN
       value_from:
         secret_scope: spiffit-secrets
         secret_key: databricks-pat-token
   ```

2. **Check Databricks Secrets exist:**
   ```powershell
   databricks secrets list-scopes --profile dlk-hackathon
   databricks secrets list --scope spiffit-secrets --profile dlk-hackathon
   ```

3. **Redeploy the app:**
   ```powershell
   .\deploy-to-databricks.ps1
   ```

---

### **Problem: PAT token set but Genie still fails**

**Symptoms:**
```
✅ Using PAT Token authentication
❌ Genie API call failed!
Error: Unable to get space [...]
```

**Possible Causes:**

1. **SQL Warehouse stopped** → Start it in Databricks UI
2. **Genie space not shared with you** → Share with your user account
3. **Wrong Genie space ID** → Verify in Troubleshooting tab

---

### **Problem: Token shows as "NOT SET"**

**Symptoms:**
```
DATABRICKS_TOKEN: ❌ NOT SET
```

**Fix:**

1. Run `setup-genie-secrets.ps1` again:
   ```powershell
   .\setup-genie-secrets.ps1
   ```

2. Verify secret was created:
   ```powershell
   databricks secrets list --scope spiffit-secrets --profile dlk-hackathon
   ```
   Should show: `databricks-pat-token`

3. Redeploy

---

## 📋 Quick Checklist

After deploying v1.4.2, verify these in the logs:

- [ ] `DATABRICKS_HOST` is ✅ SET
- [ ] `DATABRICKS_TOKEN` is ✅ SET (shows last 4 chars)
- [ ] `Auth Method: PAT Token` (not OAuth M2M)
- [ ] `GENIE_SPACE_ID` is ✅ SET
- [ ] Genie API call shows "⏳ Initiating conversation"
- [ ] Shows "✅ Received response from Genie"

**If any are ❌, see troubleshooting above!**

---

## 🎉 Success Output

When everything is working, you should see:

```
============================================================
🔐 IncentiveAI Authentication Debug
============================================================
📋 Environment Variables:
  DATABRICKS_HOST: https://dbc-4a93b454-f17b.cloud.databricks.com
  DATABRICKS_TOKEN: ✅ SET (***35c4)
  DATABRICKS_PROFILE: ❌ NOT SET
  GENIE_SPACE_ID (param): 01f0c403c3cf184e9b7f1f6c9ee45905

✅ Using PAT Token authentication (host + token)
   Host: https://dbc-4a93b454-f17b.cloud.databricks.com
   Token: ***35c4
🔑 Auth Method: PAT Token
============================================================

💬 Calling Genie API
============================================================
Space ID: 01f0c403c3cf184e9b7f1f6c9ee45905
Question: Show me the top performers
Auth Method: PAT Token
⏳ Initiating conversation (async)...
⏳ Waiting for Genie response...
✅ Received response from Genie
```

**This means Genie is working!** 🎉

---

## 📞 Need Help?

If logs still show issues:

1. Copy the full log output from the Troubleshooting tab
2. Check which auth method is being used
3. Verify all ✅ markers are present
4. Compare against the success output above

