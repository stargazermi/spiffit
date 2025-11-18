# ⚠️ HACKATHON DEMO WORKAROUND

## 🔴 **Critical: This is a TEMPORARY solution for the hackathon demo only!**

---

## 📋 **The Problem**

We've tried multiple formats for referencing Databricks Secrets in `app.yaml`, but none worked:

1. ❌ `value_from:` with nested object
2. ❌ `valueFrom: "scope/key"` string format
3. ❌ `valueFrom: { secretKeyRef: ... }` Kubernetes-style
4. ❌ `resources:` section with `valueFrom` reference

**All resulted in:**
```
DATABRICKS_TOKEN: NOT SET
Auth Method: OAuth M2M (doesn't support Genie)
```

---

## ✅ **Temporary Solution (Hackathon Only)**

**Hardcode the PAT token directly in `app.yaml`** to prove Genie integration works.

### **Step 1: Copy your PAT token**

From your `.env` file or the test script output, get your PAT token:
```
dapi5e40d9...35c4
```

### **Step 2: Edit `app.yaml`**

Open `streamlit/spiffit-ai-calculator/app.yaml` and replace:
```yaml
- name: DATABRICKS_TOKEN
  value: "YOUR_PAT_TOKEN_HERE"  # ⚠️ Replace with actual token
```

With your actual token:
```yaml
- name: DATABRICKS_TOKEN
  value: "dapi5e40d9abcdefghijklmnopqrstuvwxyz35c4"  # Your actual PAT token
```

### **Step 3: Add to .gitignore (IMPORTANT!)**

**Before committing**, ensure `app.yaml` with the token is in `.gitignore`:

```bash
# Add to .gitignore
streamlit/spiffit-ai-calculator/app.yaml
```

**Or**, create a separate `app.yaml.secret` that's gitignored, and manually update it in Databricks.

### **Step 4: Deploy**

```powershell
# ⚠️ DO NOT commit app.yaml with token to Git!
# Option A: Don't commit app.yaml at all
.\deploy-to-databricks.ps1

# Option B: Manually edit app.yaml in Databricks Git Folder
# 1. Go to /Shared/spiffit-dev in Databricks
# 2. Edit streamlit/spiffit-ai-calculator/app.yaml directly
# 3. Add your token
# 4. Deploy from Databricks UI
```

---

## 🔒 **Security Notes**

### **⚠️ DO NOT:**
- ❌ Commit `app.yaml` with the token to GitHub
- ❌ Share screenshots with the token visible
- ❌ Leave this in place after the hackathon

### **✅ AFTER THE HACKATHON:**
- 🔄 Revert to secret reference approach
- 🔄 Research correct Databricks Apps secret syntax
- 🔄 Remove hardcoded token
- 🔄 Update `app.yaml` back to secure format

---

## 📊 **Expected Result**

After deploying with the hardcoded token, the logs should show:

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

**And the Genie query should work!** 🎉

---

## 🎯 **Why This Works**

When you put the token directly in `app.yaml` as a plain value:
```yaml
- name: DATABRICKS_TOKEN
  value: "dapi..."
```

Databricks Apps loads it as a regular environment variable, and our `ai_helper.py` picks it up:
```python
token = os.getenv("DATABRICKS_TOKEN")  # Gets the value!
if host and token:
    self.workspace = WorkspaceClient(host=host, token=token)  # PAT Token auth!
```

---

## 🔄 **Post-Hackathon TODO**

1. Research official Databricks Apps documentation for secrets
2. Open support ticket if needed
3. Implement correct secret reference syntax
4. Remove hardcoded token
5. Test with proper secret management
6. Update this documentation

---

## 🆘 **Alternatives to Consider**

If you don't want to hardcode the token:

### **Option 1: Use OAuth M2M + Grant SQL Warehouse Permissions**
- Grant the OAuth M2M service principal access to SQL Warehouse
- Might still not work with Genie (limitation)

### **Option 2: Use Foundation Models Only**
- Remove Genie space IDs from `app.yaml`
- Use LLM-based responses instead of Genie
- Less impressive but more reliable

### **Option 3: Demo from Local Streamlit**
- Run `streamlit run app.py` locally with `.env` file
- Uses CLI profile authentication (works)
- No deployment needed

---

## ✅ **Current Status**

- `app.yaml` configured with placeholder token
- Version: `v1.4.5-DEMO`
- Ready to receive actual PAT token

**Replace `YOUR_PAT_TOKEN_HERE` in `app.yaml` with your actual token and deploy!**

