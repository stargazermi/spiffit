# Check if caching is working in deployed app
$appName = "spiffit-mocking-bird"
$profile = "dlk-hackathon"

Write-Host "🔍 Checking cache behavior..." -ForegroundColor Cyan
Write-Host ""

# Get recent logs and filter for cache-related messages
databricks apps logs $appName --profile $profile | Select-String -Pattern "cache|⚡|🔄|⏱️" | Select-Object -Last 30

Write-Host ""
Write-Host "Look for these messages:" -ForegroundColor Yellow
Write-Host "  ✅ '⚡ Using cached Voice Activations results' = Cache HIT (fast!)" -ForegroundColor Green
Write-Host "  ⚠️  '🔄 First run - querying Genie' = Cache MISS (slow)" -ForegroundColor Red

