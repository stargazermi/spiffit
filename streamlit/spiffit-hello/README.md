# Streamlit Hello World App for Databricks

## 🎯 Purpose
Simple "Hello World" app to test Databricks Apps deployment workflow.

## 📁 Files
- `app.py` - Main Streamlit application
- `app.yaml` - Databricks App configuration (port 8000)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🚀 Quick Start

### Option 1: Test Locally (Before Databricks)
```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py --server.port 8000
```
Then open: http://localhost:8000

### Option 2: Deploy to Databricks Apps

#### Step 1: Push to Git
```bash
git add streamlit/
git commit -m "Add hello world Streamlit app"
git push origin main
```

#### Step 2: Set up Databricks Workspace
1. Go to your Databricks workspace
2. Click **Repos** in the left sidebar
3. Click **Add Repo**
4. Enter your GitHub URL: `https://github.com/stargazermi/spiffit`
5. Click **Create Repo**

#### Step 3: Deploy the App
1. In Databricks, go to **Apps** (or **Serverless Apps**)
2. Click **Create App**
3. Configure:
   - **Name:** `hello-world-test`
   - **Source:** Select your repo (`spiffit`)
   - **Path:** `streamlit/`
   - **Compute:** Select a cluster or use serverless
4. Click **Create**
5. Wait for deployment (2-3 minutes)
6. Click the app URL to view!

## 🔧 Troubleshooting

### App won't start?
- Check that `app.yaml` is in the same folder as `app.py`
- Verify port 8000 is specified
- Check Databricks logs for errors

### Dependencies not installing?
- Make sure `requirements.txt` is present
- Try adding `--upgrade pip` to requirements

### Can't access the app?
- Verify your Databricks workspace permissions
- Check that the app status shows "Running"
- Try refreshing the page

## 📝 Next Steps

Once this works, you can:
1. Replace `app.py` with your real hackathon app
2. Add Delta Lake connections
3. Add LLM/AI integrations
4. Connect to your incentive data

## 🎉 Success Criteria

You'll know it's working when:
- ✅ App deploys without errors
- ✅ You can access the URL
- ✅ You see "Hello World!" message
- ✅ Interactive elements work (text input, button)

**Good luck! 🚀**

