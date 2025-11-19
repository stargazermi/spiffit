# 🎸 Spiffit - Quick Genie Space Check for Demo
# Shows the Genie space configuration and recent activity

Write-Host "🎸 Spiffit Genie Space Check" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Set the profile
$env:DATABRICKS_CONFIG_PROFILE = "dlk-hackathon"

# The Genie Space we're using
$GENIE_SPACE_ID = "01f0c4ae99271d64835d414b8d43ddfb"

Write-Host "📊 Checking Genie Space: $GENIE_SPACE_ID" -ForegroundColor Yellow
Write-Host ""

# Get Genie Space details
Write-Host "🔍 Fetching Genie Space details..." -ForegroundColor Green
databricks api get /api/2.0/genie/spaces/$GENIE_SPACE_ID

Write-Host ""
Write-Host "✅ Genie Space Check Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎸 When a problem comes along... you must Spiff It! 🎸" -ForegroundColor Magenta

