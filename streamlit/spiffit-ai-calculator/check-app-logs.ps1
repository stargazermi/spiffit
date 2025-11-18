# Check Databricks App Logs for Genie Performance
# Run this to see the latest logs from the deployed app

$appName = "spiffit-mocking-bird"
$profile = "dlk-hackathon"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Checking logs for app: $appName" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get app logs (last 100 lines)
Write-Host "📋 Fetching last 100 log lines..." -ForegroundColor Yellow
databricks apps logs $appName --profile $profile

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔍 Filtering for Genie-related logs..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Filter for Genie-specific logs
databricks apps logs $appName --profile $profile | Select-String -Pattern "Genie|⏱️|ERROR|WARNING"

Write-Host ""
Write-Host "✅ Done! Check above for:" -ForegroundColor Green
Write-Host "   - ⏱️ Timing logs (START/END)" -ForegroundColor White
Write-Host "   - Genie API calls" -ForegroundColor White
Write-Host "   - Errors/Warnings" -ForegroundColor White

