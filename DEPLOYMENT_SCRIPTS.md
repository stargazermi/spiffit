# 🚀 Automated Deployment Scripts

These scripts automate the process of deploying your Streamlit app to Databricks Apps.

## 📋 What They Do

1. **Show Git status** and confirm changes
2. **Stage and commit** files to Git
3. **Push to GitHub** (origin/main)
4. **Wait** for GitHub to sync
5. **Stop** the Databricks App
6. **Start** the app (pulls latest code from Git)
7. **Monitor** deployment until "RUNNING"

## 🪟 Windows (PowerShell)

### Usage:
```powershell
# Simple usage (uses default commit message)
.\deploy-to-databricks.ps1

# With custom commit message
.\deploy-to-databricks.ps1 -CommitMessage "Fix Genie API (v1.3.2)"

# With different profile or app name
.\deploy-to-databricks.ps1 -CommitMessage "Update" -Profile "my-profile" -AppName "my-app"
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

# Simple usage
./deploy-to-databricks.sh

# With custom commit message
./deploy-to-databricks.sh "Fix Genie API (v1.3.2)"

# With different profile or app name
./deploy-to-databricks.sh "Update" "my-profile" "my-app"
```

### First Time Setup:
```bash
# Make sure you're authenticated
databricks auth login --profile dlk-hackathon
```

---

## ⚙️ Configuration

### Default Values:
- **Commit Message**: "Update app"
- **Profile**: `dlk-hackathon`
- **App Name**: `spiffit-mocking-bird`

### To Change Defaults:
Edit the script parameters at the top of the file.

---

## 📊 What You'll See

### Successful Deployment:
```
🚀 Databricks App Deployment Script
=====================================

📊 Checking Git status...
M  streamlit/spiffit-ai-calculator/ai_helper.py
M  streamlit/spiffit-ai-calculator/app.py

❓ Do you want to commit and push these changes? (y/n): y

📦 Staging files...
💾 Committing changes...
⬆️  Pushing to GitHub...
✅ Successfully pushed to GitHub!

⏳ Waiting 5 seconds for GitHub to sync...

🔍 Finding Databricks App...
✅ Found app: spiffit-mocking-bird
   URL: https://spiffit-mocking-bird-1978110925405963.aws.databricksapps.com

⏸️  Stopping app...
⏳ Waiting 3 seconds...

▶️  Starting app (this will pull latest code from Git)...

⏳ Monitoring deployment (this takes ~2-3 minutes)...
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

### "Git push failed"
**Problem**: Not authenticated with GitHub or conflicts

**Fix**:
```bash
# Check if you're signed in
git remote -v

# Pull latest first if there are conflicts
git pull origin main

# Then run the script again
```

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
# 2. Run deployment script
.\deploy-to-databricks.ps1 -CommitMessage "Fix Genie API (v1.3.2)"

# 3. Wait for "App is RUNNING!"
# 4. Open app URL in browser
# 5. Verify version in Troubleshooting tab
```

### Full Workflow (Bash):
```bash
# 1. Make your code changes
# 2. Run deployment script
./deploy-to-databricks.sh "Fix Genie API (v1.3.2)"

# 3. Wait for "App is RUNNING!"
# 4. Open app URL in browser
# 5. Verify version in Troubleshooting tab
```

---

## 🚨 Important Notes

1. **Script stops the app** - Your app will be briefly unavailable (2-3 minutes)
2. **Commits are automatic** - Review `git status` before confirming
3. **Can't cancel deployment** - Once started, let it finish or stop manually in UI
4. **Monitoring is optional** - Press Ctrl+C to stop watching (app continues)

---

## 📚 Related Documentation

- **Manual Deployment**: `streamlit/spiffit-ai-calculator/DEPLOYMENT_CHECKLIST.md`
- **Genie Permissions**: `streamlit/spiffit-ai-calculator/GENIE_PERMISSIONS_FIX.md`
- **App Configuration**: `streamlit/spiffit-ai-calculator/app.yaml`
- **Changelog**: `streamlit/spiffit-ai-calculator/CHANGELOG.md`

---

**Happy deploying! 🎉**

