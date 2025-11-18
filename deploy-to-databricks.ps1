# Databricks App Deployment Script
# Restarts Databricks App (pulls latest code from Git automatically)

param(
    [string]$Profile = "dlk-hackathon",
    [string]$AppName = "spiffit-mocking-bird",
    [string]$RepoId = "2435542458835487",
    [string]$RepoBranch = "spiffit-dev"
)

Write-Host "🚀 Databricks App Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Make sure you've pushed your latest changes to GitHub first!" -ForegroundColor Yellow
Write-Host ""

$continue = Read-Host "❓ Ready to redeploy the app? (y/n)"
if ($continue -ne "y") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Step 1: Pull latest code to Databricks Git Folder
Write-Host "`n📥 Step 1: Updating Databricks Git Folder..." -ForegroundColor Green
Write-Host "   Repo ID: $RepoId" -ForegroundColor Cyan
Write-Host "   Branch: $RepoBranch" -ForegroundColor Cyan

# Update repo to latest from GitHub
Write-Host "   🔄 Pulling latest from GitHub..." -ForegroundColor Cyan
databricks repos update $RepoId --branch $RepoBranch --profile $Profile

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to update Git Folder!" -ForegroundColor Red
    Write-Host "   💡 Verify Repo ID and branch name are correct" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git Folder updated with latest code!" -ForegroundColor Green

# Step 2: Get App ID
Write-Host "`n🔍 Finding Databricks App..." -ForegroundColor Green
$appListJson = databricks apps list --profile $Profile --output json 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to list apps. Error:" -ForegroundColor Red
    Write-Host $appListJson
    Write-Host "`n💡 Make sure you're authenticated:" -ForegroundColor Yellow
    Write-Host "   databricks auth login --profile $Profile" -ForegroundColor Cyan
    exit 1
}

$apps = $appListJson | ConvertFrom-Json
$targetApp = $apps | Where-Object { $_.name -eq $AppName }

if (-not $targetApp) {
    Write-Host "❌ App '$AppName' not found!" -ForegroundColor Red
    Write-Host "`n📋 Available apps:" -ForegroundColor Yellow
    $apps | ForEach-Object { Write-Host "   - $($_.name)" -ForegroundColor Cyan }
    exit 1
}

$appId = $targetApp.name
Write-Host "✅ Found app: $AppName" -ForegroundColor Green
Write-Host "   URL: $($targetApp.url)" -ForegroundColor Cyan

# Step 3: Deploy the app (restart to pick up changes from Git Folder)
Write-Host "`n🔄 Step 3: Deploying app..." -ForegroundColor Green
Write-Host "   🔄 Restarting app to pick up latest code..." -ForegroundColor Cyan

databricks apps deploy $appId --profile $Profile

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deploy failed! Trying restart instead..." -ForegroundColor Yellow
    
    # Fallback: restart command
    databricks apps restart $appId --profile $Profile
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Restart also failed!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n✅ App restarted successfully!" -ForegroundColor Green
Write-Host "🌐 URL: $($targetApp.url)" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ Wait ~1-2 minutes for full restart, then:" -ForegroundColor Yellow
Write-Host "   1. Open URL above in your browser" -ForegroundColor Gray
Write-Host "   2. Go to 🔧 Troubleshooting tab" -ForegroundColor Gray
Write-Host "   3. Verify version and timestamp are updated" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 To check status: databricks apps get $appId --profile $Profile" -ForegroundColor Cyan

