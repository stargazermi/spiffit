# 🚀 Deploy to Databricks Apps (RECOMMENDED)

## ✅ Why Deploy to Databricks Instead of Local?

### Databricks Apps Advantages:
1. **✅ Automatic Authentication** - No CLI profile needed, just works
2. **✅ Direct Access to Genie** - Same workspace, no network issues
3. **✅ Share with Team** - Everyone can access via URL
4. **✅ Production Ready** - Proper hosting, no "running on my laptop"
5. **✅ All Space IDs Already Configured** - In `app.yaml`

### Local Testing Challenges:
- ❌ Requires Databricks CLI setup and authentication
- ❌ Profile management can be tricky
- ❌ Can't easily share with teammates
- ❌ Environment variable juggling

## 🚢 Quick Deployment Steps

### 1. Push to Git (if not already done)

```bash
cd c:\code\hackathon\spiffit

git add .
git commit -m "Add Spiffit AI Calculator with Genie integration"
git push origin main
```

### 2. Create Databricks App

1. **Go to your Databricks workspace:**  
   https://dbc-4a93b454-f17b.cloud.databricks.com

2. **Click "Apps" in the left sidebar**

3. **Click "Create App"**

4. **Configure:**
   - **Name:** `spiffit-ai-calculator`
   - **Source:** Git repository
   - **Repository URL:** `https://github.com/stargazermi/spiffit`
   - **Path:** `streamlit/spiffit-ai-calculator/`
   - **Branch:** `main`

5. **Click "Create"**

### 3. Wait for Deployment (~2-3 minutes)

The app will:
- ✅ Install dependencies from `requirements.txt`
- ✅ Load environment variables from `app.yaml`
- ✅ Authenticate automatically (no profile needed!)
- ✅ Connect to your Genie spaces

### 4. Access Your App

Once deployed, you'll get a URL like:
```
https://dbc-4a93b454-f17b.cloud.databricks.com/apps/<app-id>
```

**Share this URL with your hackathon team!**

---

## 🔧 Authentication Differences

| Aspect | Local (Your Laptop) | Databricks Apps |
|--------|-------------------|-----------------|
| **Auth Method** | CLI profile (`dlk-hackathon`) | Automatic ✅ |
| **Setup Required** | `databricks auth login` | None ✅ |
| **Env Variables** | `.env` file | `app.yaml` ✅ |
| **Access Control** | Just you | Your team ✅ |
| **Reliability** | Depends on CLI | Production ✅ |

---

## 📝 Your App is Already Configured!

All Genie space IDs are in `app.yaml`:

```yaml
env:
  - name: GENIE_SALES_SPACE_ID
    value: "01f0c403c3cf184e9b7f1f6c9ee45905"
  - name: GENIE_ANALYTICS_SPACE_ID
    value: "01f0c404048613b3b494b1a64a1bca84"
  - name: GENIE_MARKET_SPACE_ID
    value: "01f0c4043acf19dc936c37fd2a8bced3"
  - name: GENIE_SPACE_ID
    value: "01f0c403c3cf184e9b7f1f6c9ee45905"
```

**No manual configuration needed!** 🎉

---

## 🧪 Testing After Deployment

1. Open your app URL
2. You should see: **"✅ Connected to Genie Space: 01f0c403c3cf184e9b7f1f6c9ee45905"**
3. Try asking: *"Who are the top performers?"*
4. Should return data from your `sales_performance` table

---

## 💡 Recommendation

**For the hackathon, deploy to Databricks Apps instead of running locally.**

✅ Easier setup  
✅ Better for demos  
✅ Shareable with judges/team  
✅ No authentication headaches

---

**Ready to deploy! Just push to Git and create the app.** 🚀

