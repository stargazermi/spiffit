# Databricks App Deployment Script
# Pushes latest code to Git and restarts Databricks App

param(
    [string]$CommitMessage = "Update app",
    [string]$Profile = "dlk-hackathon",
    [string]$AppName = "spiffit-mocking-bird"
)

Write-Host "🚀 Databricks App Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Change to the correct directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "📂 Current directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Step 1: Git Status
Write-Host "📊 Checking Git status..." -ForegroundColor Green
git status --short

$continue = Read-Host "`n❓ Do you want to commit and push these changes? (y/n)"
if ($continue -ne "y") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Step 2: Git Add
Write-Host "`n📦 Staging files..." -ForegroundColor Green
git add streamlit/spiffit-ai-calculator/

# Step 3: Git Commit
Write-Host "`n💾 Committing changes..." -ForegroundColor Green
git commit -m $CommitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  No changes to commit or commit failed" -ForegroundColor Yellow
    $skipPush = Read-Host "Continue anyway? (y/n)"
    if ($skipPush -ne "y") {
        exit 1
    }
}

# Step 4: Git Push
Write-Host "`n⬆️  Pushing to GitHub..." -ForegroundColor Green
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green

# Step 5: Wait for GitHub sync
Write-Host "`n⏳ Waiting 5 seconds for GitHub to sync..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 6: Get App ID
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
$targetApp = $apps.apps | Where-Object { $_.name -eq $AppName }

if (-not $targetApp) {
    Write-Host "❌ App '$AppName' not found!" -ForegroundColor Red
    Write-Host "`n📋 Available apps:" -ForegroundColor Yellow
    $apps.apps | ForEach-Object { Write-Host "   - $($_.name)" -ForegroundColor Cyan }
    exit 1
}

$appId = $targetApp.name
Write-Host "✅ Found app: $AppName" -ForegroundColor Green
Write-Host "   URL: $($targetApp.url)" -ForegroundColor Cyan

# Step 7: Stop the app
Write-Host "`n⏸️  Stopping app..." -ForegroundColor Green
databricks apps stop $appId --profile $Profile

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Stop command failed (app might already be stopped)" -ForegroundColor Yellow
}

Write-Host "⏳ Waiting 3 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Step 8: Start the app (this will pull latest code from Git)
Write-Host "`n▶️  Starting app (this will pull latest code from Git)..." -ForegroundColor Green
databricks apps start $appId --profile $Profile

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start app!" -ForegroundColor Red
    exit 1
}

# Step 9: Monitor deployment
Write-Host "`n⏳ Monitoring deployment (this takes ~2-3 minutes)..." -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop monitoring (app will continue deploying)" -ForegroundColor Gray
Write-Host ""

$maxAttempts = 40  # ~2 minutes (3s per attempt)
$attempt = 0

while ($attempt -lt $maxAttempts) {
    $attempt++
    Start-Sleep -Seconds 3
    
    $appStatus = databricks apps get $appId --profile $Profile --output json 2>&1
    if ($LASTEXITCODE -eq 0) {
        $app = $appStatus | ConvertFrom-Json
        $state = $app.state.value
        
        Write-Host "   [$attempt/$maxAttempts] State: $state" -ForegroundColor Cyan
        
        if ($state -eq "RUNNING") {
            Write-Host "`n✅ App is RUNNING!" -ForegroundColor Green
            Write-Host "🌐 URL: $($app.url)" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "🔧 Verify deployment:" -ForegroundColor Yellow
            Write-Host "   1. Open the app in your browser" -ForegroundColor Gray
            Write-Host "   2. Go to 🔧 Troubleshooting tab" -ForegroundColor Gray
            Write-Host "   3. Check version (should be v1.3.2)" -ForegroundColor Gray
            Write-Host "   4. Check timestamp (should be recent)" -ForegroundColor Gray
            Write-Host ""
            exit 0
        }
        
        if ($state -eq "ERROR" -or $state -eq "CRASHED") {
            Write-Host "`n❌ App deployment failed!" -ForegroundColor Red
            Write-Host "🔍 Check logs in Databricks UI:" -ForegroundColor Yellow
            Write-Host "   Compute > Apps > $AppName > Logs" -ForegroundColor Cyan
            exit 1
        }
    }
}

Write-Host "`n⚠️  Deployment is taking longer than expected" -ForegroundColor Yellow
Write-Host "   The app is still deploying in the background." -ForegroundColor Gray
Write-Host "   Check status in Databricks UI: Compute > Apps > $AppName" -ForegroundColor Cyan

