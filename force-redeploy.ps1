#!/usr/bin/env pwsh
# Force full redeployment to ensure environment variables are loaded

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔄 Force Full Redeployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$appName = "spiffit-mocking-bird"
$profile = "dlk-hackathon"
$gitFolder = "/Repos/spg1461@ftr.com/spiffit"

# Set profile
$env:DATABRICKS_CONFIG_PROFILE = $profile

Write-Host "Step 1: Stop the app (if running)..." -ForegroundColor Yellow
databricks apps stop $appName 2>&1 | Out-Null
Start-Sleep -Seconds 3

Write-Host "Step 2: Pull latest from Git..." -ForegroundColor Yellow
Write-Host "Git folder: $gitFolder" -ForegroundColor Gray
databricks workspace export $gitFolder/streamlit/spiffit-ai-calculator/app.yaml app_backup.yaml --format AUTO 2>&1 | Out-Null

Write-Host "Step 3: Restart app with fresh environment..." -ForegroundColor Yellow
databricks apps start $appName

Write-Host ""
Write-Host "⏳ Waiting for deployment..." -ForegroundColor Cyan
$maxWait = 60
$waited = 0
$deployed = $false

while ($waited -lt $maxWait -and !$deployed) {
    Start-Sleep -Seconds 3
    $waited += 3
    
    $status = databricks apps get $appName --output json 2>&1 | ConvertFrom-Json
    
    if ($status.status.state -eq "RUNNING") {
        $deployed = $true
        Write-Host "✅ App is RUNNING!" -ForegroundColor Green
    } elseif ($status.status.state -eq "ERROR") {
        Write-Host "❌ Deployment failed!" -ForegroundColor Red
        Write-Host "Error: $($status.status.message)" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "   [$waited/$maxWait] State: $($status.status.state)..." -ForegroundColor Gray
    }
}

if (!$deployed) {
    Write-Host "⚠️  Deployment taking longer than expected" -ForegroundColor Yellow
    Write-Host "Check app status in Databricks UI" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ Redeployment Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Next: Run test to verify environment variables loaded:" -ForegroundColor Yellow
Write-Host "  .\test-voice-genie-env.ps1" -ForegroundColor White
Write-Host ""

# Cleanup
Remove-Item Env:\DATABRICKS_CONFIG_PROFILE -ErrorAction SilentlyContinue

