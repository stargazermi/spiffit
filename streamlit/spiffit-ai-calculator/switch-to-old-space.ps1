# Switch .env file to use the OLD working Genie space

$envFile = ".env"
$oldSpaceId = "0110c4ae99271d64835d414b8d43ddfb"  # NEW broken space
$workingSpaceId = "01f0c4ae99271d64835d414b8d43ddfb"  # OLD working space

Write-Host "Switching .env to use working Genie space..." -ForegroundColor Cyan
Write-Host ""

if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    
    if ($content -match $oldSpaceId) {
        $newContent = $content -replace $oldSpaceId, $workingSpaceId
        $newContent | Set-Content $envFile -NoNewline
        Write-Host "✅ Updated .env to use WORKING Genie space" -ForegroundColor Green
        Write-Host "   Old (broken): $oldSpaceId" -ForegroundColor Red
        Write-Host "   New (working): $workingSpaceId" -ForegroundColor Green
    } elseif ($content -match $workingSpaceId) {
        Write-Host "✅ .env already uses the working Genie space!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env doesn't contain either space ID. Please update manually:" -ForegroundColor Yellow
        Write-Host "   GENIE_SPACE_ID=$workingSpaceId" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ No .env file found! Creating one..." -ForegroundColor Red
    
    $envTemplate = @"
# Databricks Authentication (for local testing)
DATABRICKS_PROFILE=dlk-hackathon
DATABRICKS_HOST=https://dbc-4a93b454-f17b.cloud.databricks.com

# SQL Warehouse ID
SQL_WAREHOUSE_ID=0962fa4cf0922125

# Working Genie Space ID (all agents point here)
GENIE_SPACE_ID=$workingSpaceId
GENIE_SALES_SPACE_ID=$workingSpaceId
GENIE_ANALYTICS_SPACE_ID=$workingSpaceId
GENIE_MARKET_SPACE_ID=$workingSpaceId
GENIE_VOICE_ACTIVATIONS_SPACE_ID=$workingSpaceId
"@
    
    $envTemplate | Set-Content $envFile -NoNewline
    Write-Host "✅ Created .env with working Genie space!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Copy Instructions from NEW space to OLD space in Databricks UI" -ForegroundColor Gray
Write-Host "2. Ensure voice_opps and voice_orders tables are connected to OLD space" -ForegroundColor Gray
Write-Host "3. Test the app locally: streamlit run app.py" -ForegroundColor Gray

