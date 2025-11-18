# Databricks Authentication for Local Testing

## ✅ How It Works

The app uses the Databricks CLI profile for local authentication.

### Your Configuration:

**Profile:** `dlk-hackathon`  
**Host:** https://dbc-4a93b454-f17b.cloud.databricks.com  
**Status:** ✅ Valid

### Files:

1. **`.env`** - Contains `DATABRICKS_PROFILE=dlk-hackathon`
2. **`ai_helper.py`** - Reads profile from environment and connects to Databricks
3. **`app.py`** - Loads `.env` file at startup using `python-dotenv`

## 🚀 To Run the App:

```bash
cd streamlit/spiffit-ai-calculator
streamlit run app.py --server.port 8000
```

The app will:
1. Load `.env` file → Sets `DATABRICKS_PROFILE=dlk-hackathon`
2. Initialize `WorkspaceClient(profile="dlk-hackathon")`
3. Connect to your Genie spaces using your authenticated session

## 🔧 Troubleshooting

**If you get auth errors:**

1. Verify profile is valid:
```bash
databricks auth profiles
```

2. Re-authenticate if needed:
```bash
databricks auth login --host https://dbc-4a93b454-f17b.cloud.databricks.com --profile dlk-hackathon
```

3. Check `.env` file has:
```
DATABRICKS_PROFILE=dlk-hackathon
GENIE_SPACE_ID=01f0c403c3cf184e9b7f1f6c9ee45905
```

## 🚢 For Databricks Deployment

When deploying to Databricks Apps, authentication is automatic (no profile needed).  
The `app.yaml` already has all Genie space IDs configured.

---

**Your authentication is configured and ready!** 🎉

