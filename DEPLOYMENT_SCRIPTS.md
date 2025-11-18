# 🚀 Automated Deployment Scripts

These scripts automate the process of deploying your Streamlit app to Databricks Apps.

## 📋 What They Do

1. **Confirm** you're ready to deploy
2. **Pull latest code** from GitHub to your Databricks Git Folder (Repos)
3. **Find** your Databricks App
4. **Deploy** the app (restart to pick up changes from Git Folder)
5. **Monitor** deployment until "RUNNING"

**Note:** You handle Git commits/push separately. These scripts only manage the Databricks side.

## 🪟 Windows (PowerShell)

### Usage:
```powershell
# After you've pushed to Git, run:
.\deploy-to-databricks.ps1

# With different profile, app name, repo ID, or branch
.\deploy-to-databricks.ps1 -Profile "my-profile" -AppName "my-app" -RepoId "1234567890" -RepoBranch "main"
```

### First Time Setup:
```powershell
# Make sure you're authenticated
databricks auth login --profile dlk-hackathon

# Set execution policy if needed (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🍎 Mac/Linux (Bash)

### Usage:
```bash
# Make script executable (first time only)
chmod +x deploy-to-databricks.sh

# After you've pushed to Git, run:
./deploy-to-databricks.sh

# With different profile, app name, repo ID, or branch
./deploy-to-databricks.sh "my-profile" "my-app" "1234567890" "main"
```

### First Time Setup:
```bash
# Make sure you're authenticated
databricks auth login --profile dlk-hackathon
```

---

## ⚙️ Configuration

### Default Values:
- **Profile**: `dlk-hackathon`
- **App Name**: `spiffit-mocking-bird`
- **Repo ID**: `2435542458835487` (spiffit-dev Git folder)
- **Repo Branch**: `spiffit-dev`

### To Change Defaults:
Edit the script parameters at the top of the file.

---

## 📊 What You'll See

### Successful Deployment:
```
🚀 Databricks App Deployment Script
=====================================

⚠️  Make sure you've pushed your latest changes to GitHub first!

❓ Ready to redeploy the app? (y/n): y

📥 Step 1: Updating Databricks Git Folder...
   Path: /Shared/spiffit-dev
✅ Found Git Folder (ID: 2435542458835487)
   🔄 Pulling latest from GitHub...
✅ Git Folder updated with latest code!

🔍 Step 2: Finding Databricks App...
✅ Found app: spiffit-mocking-bird
   URL: https://spiffit-mocking-bird-1978110925405963.aws.databricksapps.com

🔄 Step 3: Deploying app...
   🔄 Restarting app to pick up latest code...

⏳ Step 4: Monitoring deployment (this takes ~2-3 minutes)...
   Press Ctrl+C to stop monitoring (app will continue deploying)

   [1/40] State: STARTING
   [2/40] State: STARTING
   [3/40] State: STARTING
   ...
   [15/40] State: RUNNING

✅ App is RUNNING!
🌐 URL: https://spiffit-mocking-bird-1978110925405963.aws.databricksapps.com

🔧 Verify deployment:
   1. Open the app in your browser
   2. Go to 🔧 Troubleshooting tab
   3. Check version (should be v1.3.2)
   4. Check timestamp (should be recent)
```

---

## 🔧 Troubleshooting

### "Failed to list apps"
**Problem**: Not authenticated with Databricks CLI

**Fix**:
```bash
databricks auth login --profile dlk-hackathon
# Follow prompts to authenticate
```

---

### "App 'spiffit-mocking-bird' not found"
**Problem**: Wrong app name or profile

**Fix**:
1. List available apps:
   ```bash
   databricks apps list --profile dlk-hackathon
   ```
2. Use the correct app name from the list
3. Or update the script's default app name

---

### "Deployment is taking longer than expected"
**Problem**: App is still deploying (normal for complex apps)

**What to do**:
- The app continues deploying in the background
- Check status in Databricks UI:
  - Go to **Compute** > **Apps**
  - Find your app
  - Check **Deployments** tab for progress
- Or wait a few more minutes and check the app URL

---

## 🎯 Quick Reference

### Full Workflow (PowerShell):
```powershell
# 1. Make your code changes

# 2. Commit and push to GitHub (you handle this)
git add .
git commit -m "Fix Genie API (v1.3.2)"
git push origin main

# 3. Run deployment script
.\deploy-to-databricks.ps1

# 4. Wait for "App is RUNNING!"
# 5. Open app URL in browser
# 6. Verify version in Troubleshooting tab
```

### Full Workflow (Bash):
```bash
# 1. Make your code changes

# 2. Commit and push to GitHub (you handle this)
git add .
git commit -m "Fix Genie API (v1.3.2)"
git push origin main

# 3. Run deployment script
./deploy-to-databricks.sh

# 4. Wait for "App is RUNNING!"
# 5. Open app URL in browser
# 6. Verify version in Troubleshooting tab
```

---

## 🚨 Important Notes

1. **Push to GitHub first** - Script pulls from GitHub, so commit/push before running
2. **App restarts automatically** - Your app will be briefly unavailable (2-3 minutes)
3. **Can't cancel deployment** - Once started, let it finish or stop manually in UI
4. **Monitoring is optional** - Press Ctrl+C to stop watching (app continues deploying)

---

## 📚 Related Documentation

- **Manual Deployment**: `streamlit/spiffit-ai-calculator/DEPLOYMENT_CHECKLIST.md`
- **Genie Permissions**: `streamlit/spiffit-ai-calculator/GENIE_PERMISSIONS_FIX.md`
- **App Configuration**: `streamlit/spiffit-ai-calculator/app.yaml`
- **Changelog**: `streamlit/spiffit-ai-calculator/CHANGELOG.md`

---

**Happy deploying! 🎉**

