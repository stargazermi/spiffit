# 🔐 Genie Access with PAT Token

## Problem
Databricks Apps use OAuth M2M authentication, which **doesn't work with Genie spaces**.

## Solution
Use a **Personal Access Token (PAT)** for authentication instead.

---

## ✅ Setup Steps

### **Step 1: Generate PAT Token**

1. In Databricks, go to **Settings** (top right gear icon)
2. Click **Developer** → **Access Tokens**
3. Click **Generate New Token**
4. **Name**: `spiffit-genie-access`
5. **Lifetime**: Choose appropriate duration (90 days for hackathon)
6. **Click "Generate"**
7. **⚠️ COPY THE TOKEN IMMEDIATELY** - you won't see it again!

---

### **Step 2: Store Token in Databricks Secrets**

**Option A: Use the setup script (easiest):**
```powershell
.\setup-genie-secrets.ps1
```

**Option B: Manual setup:**
```bash
# Create secret scope
databricks secrets create-scope spiffit-secrets --profile dlk-hackathon

# Store token (opens editor)
databricks secrets put-secret spiffit-secrets databricks-pat-token --profile dlk-hackathon
# Paste your token, save, and close
```

The `app.yaml` is already configured to use this secret:
```yaml
# Define the secret as a resource
resources:
  - name: databricks-pat
    secret:
      scope: spiffit-secrets
      key: databricks-pat-token

# Reference the resource in environment variables
env:
  - name: DATABRICKS_TOKEN
    valueFrom: databricks-pat
```

✅ **Safe to commit - no token in Git!**

**Note:** Secrets must be defined as resources first, then referenced by resource name in env vars!

---

### **Step 3: Deploy**

```powershell
git add streamlit/spiffit-ai-calculator/app.yaml streamlit/spiffit-ai-calculator/ai_helper.py
git commit -m "Add PAT token auth for Genie access"
git push origin spiffit-dev
.\deploy-to-databricks.ps1
```

---

### **Step 4: Test**

1. Wait ~1-2 minutes for app to restart
2. Open app URL
3. Go to **🔧 Troubleshooting** tab
4. Click **"Test Genie Query"**
5. Should see: **"✅ Genie query successful!"** with actual data!

---

## 🔍 How It Works

The `ai_helper.py` now checks for authentication in this order:

1. **`DATABRICKS_HOST` + `DATABRICKS_TOKEN`** → Uses PAT token (✅ supports Genie)
2. **`DATABRICKS_PROFILE`** → Uses CLI profile (✅ local dev only)
3. **Automatic OAuth** → Databricks Apps default (❌ doesn't support Genie)

By setting the token environment variables, we force PAT token authentication.

---

## 🚨 Troubleshooting

### **Token still not working?**
1. Verify token is correct (no extra spaces)
2. Check token hasn't expired
3. Ensure user who created token has access to Genie spaces
4. Restart app after updating `app.yaml`

### **Still getting "does not exist" error?**
The PAT token user might not have Genie space access. Share the spaces:
1. Go to **Genie** in Databricks
2. Open each space: `spg-mocking-bird-sales`, `spg-mocking-bird-analytics`, `spg-mocking-bird-market`
3. Click **Share** → Add your user → **"Can Run"** permission

---

## 📚 Related Docs
- `GENIE_PERMISSIONS_FIX.md` - SQL warehouse permissions
- `AUTHENTICATION.md` - Local development auth
- `DEPLOY_TO_DATABRICKS.md` - Deployment guide

